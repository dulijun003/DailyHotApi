"""ReelScene: base class every topic video inherits from.

A video is a list of "beats" (short methods). `construct()` runs them in
order, so reordering, cutting or adding a beat is a one-line change.

Narrated videos are voice-driven:

    with self.voice("host.1") as v:      # starts speaking NARRATION["host.1"]
        self.set_header(...)             # plays while the line is spoken
        v.until("山羊")                   # wait until the word "山羊" is said
        self.play(door.open())           # ...so the door opens on that word

The block lasts exactly as long as the line (plus a short breath), so the
voice never stops for dead air. Without NARRATION the same code runs silent
and `self.wait()` keeps its normal pacing.
"""

import json
from contextlib import contextmanager
from pathlib import Path

from manim import (
    DOWN, UP, AnimationGroup, FadeIn, FadeOut, Scene, ValueTracker, config, linear,
)

from . import audio
from . import components as C
from . import style as S


class _Cue:
    """Handle yielded by ReelScene.voice() to sync animations to words."""

    def __init__(self, scene, narration=None, start=0.0):
        self.scene, self.n, self.start, self.pos = scene, narration, start, 0

    def until(self, phrase, lead=0.0):
        """Wait until `phrase` starts being spoken (minus `lead` seconds)."""
        if self.n is None:
            return
        t, self.pos = self.n.time_of(phrase, self.pos)
        remaining = self.start + t - lead - self.scene.renderer.time
        if remaining > 1 / config.frame_rate:
            Scene.wait(self.scene, remaining)

    def time_left(self):
        if self.n is None:
            return 0.0
        return self.start + self.n.duration - self.scene.renderer.time


class ReelScene(Scene):
    BEATS: list[str] = []      # method names, run in order
    PACE = 1.0                 # <1 = snappier: scales every fade/pause (not races)

    # Narration (optional): NARRATION maps a key to the text spoken there.
    NARRATION: dict[str, str] = {}
    VOICE = "zh-CN-YunxiNeural"
    VOICE_RATE = "+20%"
    VOICE_GAIN = 2.0           # dB
    VOICE_BREATH = 0.22        # pause between narration blocks (s)
    SUBTITLES = True           # write .srt/.ass; render.sh burns the .ass in

    def setup(self):
        self.camera.background_color = S.BG
        self.header_mob = None
        self._subs = []        # (t_start, t_end, text)
        self._cues = []        # music cues: (time, kind, value)
        self._in_voice = 0

    def construct(self):
        for name in self.BEATS:
            start = self.renderer.time
            getattr(self, name)()
            print(f"[beat] {name:<14} {start:6.1f}s -> {self.renderer.time:6.1f}s")
        self._write_sidecars()

    # ---- Tempo ----------------------------------------------------------------
    def play(self, *anims, run_time=None, paced=True, **kw):
        if paced:
            if run_time is None:
                run_time = max(getattr(a, "run_time", 1.0) for a in anims)
            run_time *= self.PACE
        if run_time is not None:
            kw["run_time"] = run_time
        super().play(*anims, **kw)

    def wait(self, duration=1.0, **kw):
        # Inside a narration block the voice sets the pace: pauses are skipped
        # and the block waits for the line to finish instead.
        if self._in_voice:
            return
        super().wait(duration * self.PACE, **kw)

    def hold(self, duration):
        """A real pause, even inside a narration block (unlike wait())."""
        Scene.wait(self, duration)

    # ---- Sound ----------------------------------------------------------------
    SFX_GAIN = -4.0            # dB applied to every effect, so music + sfx sit together

    def sfx(self, name, delay=0.0, gain=0.0):
        """Play a sound effect `delay` seconds from now (see reelkit/audio.py)."""
        self.add_sound(audio.sfx_path(name), time_offset=delay, gain=self.SFX_GAIN + gain)

    def music(self, section):
        """Switch the music to `section` (intro/main/tension/outro) from here on."""
        self._cues.append((self.renderer.time, "section", section))

    def music_hit(self, delay=0.0):
        """A musical accent (swell + hit) landing `delay` seconds from now."""
        self._cues.append((self.renderer.time + delay, "hit", None))

    def music_end(self):
        """Land the music's final chord now; it rings until the video ends."""
        self._cues.append((self.renderer.time, "final", None))

    def wait_for_downbeat(self, min_wait=0.6):
        """Wait until the music's next bar line (so an ending lands on the beat)."""
        bar = 4 * 60 / audio.BPM
        t = self.renderer.time + min_wait
        target = -(-t // bar) * bar
        Scene.wait(self, target - self.renderer.time)

    # ---- Narration ------------------------------------------------------------
    @contextmanager
    def voice(self, key):
        text = self.NARRATION.get(key)
        if not text:
            yield _Cue(self)
            return
        from . import voice as V

        n = V.tts(text, self.VOICE, self.VOICE_RATE)
        start = self.renderer.time
        self.add_sound(n.path, gain=self.VOICE_GAIN)
        for a, b, clause in n.clauses():
            self._subs.append((start + a, start + b, clause))
        cue = _Cue(self, n, start)
        self._in_voice += 1
        try:
            yield cue
        finally:
            self._in_voice -= 1
        left = cue.time_left()
        if left > 0:
            Scene.wait(self, left + self.VOICE_BREATH)
        else:
            if left < -0.25:
                print(f"[voice] '{key}': animations overran the line by {-left:.2f}s")
            Scene.wait(self, max(0.05, self.VOICE_BREATH + left))

    def _write_sidecars(self):
        """Subtitles (.srt/.ass) and music cues (.json) for render.sh."""
        name = type(self).__name__
        media = Path(config.media_dir)
        if self._subs and self.SUBTITLES:
            from . import subtitles
            out = media / "subtitles"
            out.mkdir(parents=True, exist_ok=True)
            subtitles.write_srt(self._subs, out / f"{name}.srt")
            subtitles.write_ass(self._subs, out / f"{name}.ass")
        cues = media / "cues"
        cues.mkdir(parents=True, exist_ok=True)
        (cues / f"{name}.json").write_text(json.dumps(
            {"duration": self.renderer.time, "cues": self._cues}, indent=1))

    # ---- Header -------------------------------------------------------------
    def set_header(self, title, sub=None, run_time=0.6, **kw):
        """Replace the current title/subtitle with a cross-fade."""
        new = C.header(title, sub, **kw)
        anims = [FadeIn(new, shift=DOWN * 0.15)]
        if self.header_mob is not None:
            anims.insert(0, FadeOut(self.header_mob, shift=UP * 0.15))
        self.play(AnimationGroup(*anims, lag_ratio=0.3), run_time=run_time)
        self.header_mob = new
        return new

    def clear_stage(self, *keep, run_time=0.5):
        """Fade out everything except `keep` (the header goes too)."""
        keep_set = set(keep)
        gone = [m for m in self.mobjects if m not in keep_set]
        if gone:
            self.play(*[FadeOut(m) for m in gone], run_time=run_time)
        if self.header_mob not in keep_set:
            self.header_mob = None

    # ---- Physics races ------------------------------------------------------
    def race(self, runners, world, t_end=None, speed=1.0, timer_num=None,
             extra_updaters=(), hold=0.4):
        """Animate beads sliding down their tracks in real (or scaled) time.

        runners: list of (Track, bead_mobject)
        t_end:   stop at this simulated time (default: slowest track finishes)
        speed:   playback speed; 0.5 = slow motion
        timer_num: a DecimalNumber that shows the simulated time
        extra_updaters: callables f(t) run every frame (labels, trails, ...)
        Returns the ValueTracker so callers can keep using simulated time.
        """
        if t_end is None:
            t_end = max(tr.total_time for tr, _ in runners)
        t = ValueTracker(0)

        def place(tr, b):
            return lambda m: m.move_to(world.to_scene(*tr.pos_at_time(t.get_value())))

        for tr, b in runners:
            b.add_updater(place(tr, b))
        if timer_num is not None:
            timer_num.add_updater(lambda m: m.set_value(t.get_value()))
        # Extra per-frame callbacks ride on the first bead, so they are
        # cleared together with the bead updaters below.
        for f in extra_updaters:
            runners[0][1].add_updater((lambda f: lambda m: f(t.get_value()))(f))

        self.play(t.animate.set_value(t_end), run_time=t_end / speed, rate_func=linear,
                  paced=False)

        for tr, b in runners:
            b.clear_updaters()
        if timer_num is not None:
            timer_num.clear_updaters()
            timer_num.set_value(t_end)
        if hold:
            self.wait(hold)
        return t
