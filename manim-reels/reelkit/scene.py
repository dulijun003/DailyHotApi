"""ReelScene: base class every topic video inherits from.

A video is a list of "beats" (short methods, ~3-6 s each). `construct()` runs
them in order, so reordering, cutting or adding a beat is a one-line change.
"""

from contextlib import contextmanager
from pathlib import Path

from manim import (
    DOWN, UP, AnimationGroup, FadeIn, FadeOut, Scene, ValueTracker, config, linear,
)

from . import audio
from . import components as C
from . import style as S


class ReelScene(Scene):
    BEATS: list[str] = []      # method names, run in order
    PACE = 1.0                 # <1 = snappier: scales every fade/pause (not races)

    # Narration (optional). NARRATION maps a key to the text spoken there;
    # beats wrap animations in `with self.voice("key"):`. No entry = silent.
    NARRATION: dict[str, str] = {}
    VOICE = "zh-CN-YunxiNeural"
    VOICE_RATE = "+15%"
    VOICE_GAIN = 2.0           # dB
    VOICE_GAP = 0.22           # pause between sentences (s)
    SUBTITLES = True           # write .srt/.ass next to the video; render.sh burns the .ass in

    def setup(self):
        self.camera.background_color = S.BG
        self.header_mob = None
        self._subs = []        # (t_start, t_end, text)

    def construct(self):
        for name in self.BEATS:
            start = self.renderer.time
            getattr(self, name)()
            print(f"[beat] {name:<14} {start:6.1f}s -> {self.renderer.time:6.1f}s")
        if self._subs and self.SUBTITLES:
            self._write_subtitles()

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
        super().wait(duration * self.PACE, **kw)

    # ---- Sound ----------------------------------------------------------------
    SFX_GAIN = -4.0            # dB applied to every effect, so music + sfx sit together

    def sfx(self, name, delay=0.0, gain=0.0):
        """Play a sound effect `delay` seconds from now (see reelkit/audio.py)."""
        self.add_sound(audio.sfx_path(name), time_offset=delay, gain=self.SFX_GAIN + gain)

    # ---- Narration ------------------------------------------------------------
    @contextmanager
    def voice(self, key):
        """Speak NARRATION[key] starting now; the block lasts at least as long.

        Animations inside the block play while the line is spoken. If they
        finish early, the scene waits for the voice; if they run longer, the
        next line simply starts later.
        """
        text = self.NARRATION.get(key)
        if not text:
            yield
            return
        from . import voice as V

        start = self.renderer.time
        offset = 0.0
        for sentence in V.split_sentences(text):
            path, dur = V.tts(sentence, self.VOICE, self.VOICE_RATE)
            self.add_sound(path, time_offset=offset, gain=self.VOICE_GAIN)
            clauses = V.split_clauses(sentence)
            weights = [max(len(c), 1) for c in clauses]
            t = start + offset
            for c, w in zip(clauses, weights):
                d = dur * w / sum(weights)
                self._subs.append((t, t + d, c))
                t += d
            offset += dur + self.VOICE_GAP
        yield
        remaining = start + offset - self.renderer.time
        if remaining > 0.02:
            Scene.wait(self, remaining)

    def _write_subtitles(self):
        """Write <media>/subtitles/<Scene>.srt and .ass (styled to match the reel)."""
        from . import subtitles
        out = Path(config.media_dir) / "subtitles"
        out.mkdir(parents=True, exist_ok=True)
        name = type(self).__name__
        subtitles.write_srt(self._subs, out / f"{name}.srt")
        subtitles.write_ass(self._subs, out / f"{name}.ass")

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
