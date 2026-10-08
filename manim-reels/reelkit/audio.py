"""Procedural audio: sound effects and background music, synthesised with numpy.

Everything is generated from code, so there are no licensing issues and the
output is identical on every machine. Files are cached under reelkit/assets/.

    python -m reelkit.audio music 52 out.wav [cues.json]   # 52 s music bed
    python -m reelkit.audio sfx                  # (re)build all sound effects
"""

import sys
import wave
from pathlib import Path

import numpy as np
from scipy.signal import lfilter

SR = 44100
ASSETS = Path(__file__).resolve().parent / "assets"
SFX_DIR = ASSETS / "sfx"
RNG = np.random.default_rng(7)


# ---- Primitives ------------------------------------------------------------

def t_axis(dur):
    return np.arange(int(dur * SR)) / SR


def note_hz(midi):
    return 440.0 * 2 ** ((midi - 69) / 12)


def env_exp(dur, decay, attack=0.004):
    t = t_axis(dur)
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    return a * np.exp(-t / decay)


def sine(freq, dur, phase=0.0):
    t = t_axis(dur)
    if callable(freq):
        f = freq(t)
        return np.sin(2 * np.pi * np.cumsum(f) / SR + phase)
    return np.sin(2 * np.pi * freq * t + phase)


def lowpass(x, cutoff):
    """One-pole low-pass. `cutoff` may be a scalar or a per-sample array."""
    if np.isscalar(cutoff):
        a = 1 - np.exp(-2 * np.pi * cutoff / SR)
        return lfilter([a], [1, a - 1], x)
    cutoff = np.broadcast_to(np.asarray(cutoff, dtype=float), x.shape)
    a = 1 - np.exp(-2 * np.pi * cutoff / SR)
    y = np.empty_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a[i] * (x[i] - acc)
        y[i] = acc
    return y


def highpass(x, cutoff):
    return x - lowpass(x, cutoff)


def noise(dur):
    return RNG.uniform(-1, 1, int(dur * SR))


def place(buf, clip, start):
    i = int(start * SR)
    if i < 0:
        clip, i = clip[-i:], 0
    j = min(len(buf), i + len(clip))
    if j > i:
        buf[i:j] += clip[: j - i]


def reverb(x, mix=0.25, delays=(0.031, 0.047, 0.067, 0.089), fb=0.45):
    """Cheap Schroeder-style reverb: parallel feedback combs, low-passed."""
    out = np.zeros(len(x) + int(1.5 * SR))
    out[: len(x)] += x
    wet = np.zeros_like(out)
    for d in delays:
        n = int(d * SR)
        comb = np.zeros_like(out)
        comb[: len(x)] = x
        for k in range(n, len(comb), n):
            comb[k:k + n] += fb * comb[k - n:k][: len(comb[k:k + n])]
        wet += comb
    wet = lowpass(wet / len(delays), 3500)
    return (1 - mix) * out + mix * wet


def normalize(x, peak=0.9):
    m = np.max(np.abs(x)) or 1.0
    return x * (peak / m)


def write_wav(path, x, stereo_width=0.0):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    x = np.clip(x, -1, 1)
    if stereo_width:
        # Tiny Haas delay on the right channel for width.
        d = int(0.012 * SR)
        r = np.concatenate([np.zeros(d), x[:-d]])
        l = x
        r = (1 - stereo_width) * x + stereo_width * r
        data = np.stack([l, r], axis=1)
    else:
        data = np.stack([x, x], axis=1)
    pcm = (data * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())
    return path


# ---- Sound effects ---------------------------------------------------------

def sfx_pop():
    d = 0.09
    s = sine(lambda t: 900 - 5000 * t, d) * env_exp(d, 0.025)
    return normalize(s, 0.7)


def sfx_click():
    d = 0.04
    s = highpass(noise(d), 2500) * env_exp(d, 0.004) + 0.5 * sine(1800, d) * env_exp(d, 0.008)
    return normalize(s, 0.6)


def sfx_tick():
    d = 0.03
    return normalize(sine(3200, d) * env_exp(d, 0.006), 0.35)


def sfx_whoosh():
    d = 0.45
    t = t_axis(d)
    env = np.sin(np.pi * np.clip(t / d, 0, 1)) ** 2
    s = lowpass(noise(d), 300 + 3500 * env) * env
    return normalize(s, 0.45)


def sfx_door():
    """Door swinging open: soft creak + low thud."""
    d = 0.55
    t = t_axis(d)
    creak = sine(lambda t: 520 + 180 * np.sin(2 * np.pi * 7 * t) + 300 * t, d)
    creak = lowpass(creak * (0.6 + 0.4 * np.sign(np.sin(2 * np.pi * 38 * t))), 1800)
    creak *= np.clip(t / 0.05, 0, 1) * np.exp(-t / 0.18) * 0.35
    thud = sine(lambda t: 95 - 40 * t, d) * env_exp(d, 0.09)
    thud = np.roll(thud, int(0.18 * SR))
    thud[: int(0.18 * SR)] = 0
    return normalize(reverb(creak + thud, 0.2)[: int(0.9 * SR)], 0.75)


def sfx_goat():
    """Playful 'wah-wah' fail sound."""
    out = np.zeros(int(0.7 * SR))
    for k, (m, start) in enumerate([(62, 0.0), (58, 0.22)]):
        d = 0.32 if k == 1 else 0.2
        f = note_hz(m)
        tone = sum(sine(f * h, d) / h for h in (1, 2, 3))
        tone = lowpass(tone, 1400) * env_exp(d, 0.12 if k else 0.08, 0.01)
        if k == 1:
            tone *= 1 + 0.25 * np.sin(2 * np.pi * 6 * t_axis(d))
        place(out, tone, start)
    return normalize(out, 0.55)


def sfx_chime():
    """Bright 'win' arpeggio (car reveal)."""
    out = np.zeros(int(1.4 * SR))
    for i, m in enumerate([72, 76, 79, 84]):
        d = 1.0
        f = note_hz(m)
        tone = sine(f, d) + 0.3 * sine(2 * f, d) + 0.08 * sine(3.01 * f, d)
        place(out, tone * env_exp(d, 0.35), i * 0.07)
    return normalize(reverb(out, 0.3)[: int(1.6 * SR)], 0.6)


def sfx_ding():
    d = 1.0
    f = note_hz(84)
    tone = sine(f, d) + 0.4 * sine(2.76 * f, d) * env_exp(d, 0.08)
    return normalize(reverb(tone * env_exp(d, 0.3), 0.25)[: int(1.2 * SR)], 0.45)


def sfx_rise():
    """Short upward sweep, for a reveal / 'aha'."""
    d = 0.6
    t = t_axis(d)
    s = sine(lambda t: 300 + 900 * (t / d) ** 2, d) * np.clip(t / d, 0, 1) ** 1.5
    s = lowpass(s, 2500) * np.exp(-np.maximum(t - 0.5, 0) / 0.03)
    w = np.zeros_like(s)
    place(w, sfx_whoosh(), 0.15)
    return normalize(s + 0.3 * w, 0.4)


SFX = {
    "pop": sfx_pop, "click": sfx_click, "tick": sfx_tick, "whoosh": sfx_whoosh,
    "door": sfx_door, "goat": sfx_goat, "chime": sfx_chime, "ding": sfx_ding,
    "rise": sfx_rise,
}


def sfx_path(name):
    p = SFX_DIR / f"{name}.wav"
    if not p.exists():
        write_wav(p, SFX[name]())
    return str(p)


# ---- Background music ------------------------------------------------------
#
# "Curious explainer" bed: pizzicato strings + glockenspiel + soft pad, light
# shaker and finger snaps, no heavy drums. Chords follow the "royal road"
# progression (IVmaj7 - V6 - iii7 - vi7 in C), bright but thoughtful.
#
# The arrangement follows the video: scenes drop cues (ReelScene.music*),
# saved to media/cues/<Scene>.json:
#   section intro   - pad + bells only
#   section main    - everything
#   section tension - pad + muted pizz + heartbeat pulse (bass/percussion out)
#   section outro   - everything, bells brighter
#   hit             - reverse swell into a soft boom + bell chord, on the cue
#   final           - loops stop, a C major chord rings to the end

BPM = 100
PROGRESSION = [            # (bass root, chord tones as MIDI in the middle register)
    (41, [53, 57, 60, 64]),    # Fmaj7
    (43, [55, 59, 62, 64]),    # G6
    (40, [52, 55, 59, 62]),    # Em7
    (45, [57, 60, 64, 67]),    # Am7
]
FINAL_CHORD = (36, [48, 55, 60, 64, 67, 74])     # Cadd9, wide voicing

SECTION_GAINS = {          # layer -> gain per section
    "intro":   dict(pad=1.0, pizz=0.0, bass=0.0, bell=0.9, shaker=0.0, snap=0.0, pulse=0.0),
    "main":    dict(pad=0.7, pizz=1.0, bass=1.0, bell=0.5, shaker=0.8, snap=0.7, pulse=0.0),
    "tension": dict(pad=1.0, pizz=0.55, bass=0.0, bell=0.0, shaker=0.0, snap=0.0, pulse=1.0),
    "outro":   dict(pad=0.8, pizz=1.0, bass=1.0, bell=1.0, shaker=0.9, snap=0.8, pulse=0.0),
}
LAYER_LEVEL_DB = dict(pad=-25, pizz=-19, bass=-21, bell=-27, shaker=-33, snap=-31, pulse=-24)


def pluck(midi, dur, brightness=0.5, decay=0.996):
    """Karplus-Strong plucked string (vectorised with lfilter)."""
    f = note_hz(midi)
    n_delay = max(2, int(round(SR / f)))
    n = int(dur * SR)
    x = np.zeros(n)
    burst = RNG.uniform(-1, 1, n_delay)
    burst = lfilter([brightness], [1, brightness - 1], burst)   # soften the attack
    x[:n_delay] = burst
    a = np.zeros(n_delay + 2)
    a[0] = 1.0
    a[n_delay] = a[n_delay + 1] = -0.5 * decay
    y = lfilter([1.0], a, x)
    return y * np.clip((dur - t_axis(dur)) / 0.03, 0, 1)


def glock(midi, dur=1.6):
    f = note_hz(midi)
    t = t_axis(dur)
    x = (np.sin(2 * np.pi * f * t) * np.exp(-t / 0.7)
         + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t / 0.18)
         + 0.12 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t / 0.07))
    return x * np.clip(t / 0.002, 0, 1)


def soft_pad(tones, dur, cutoff=1300):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for m in tones:
        f = note_hz(m)
        for det in (-0.08, 0.08):
            ph = RNG.uniform(0, 6.28)
            x += np.sin(2 * np.pi * f * 2 ** (det / 12) * t + ph)
            x += 0.25 * np.sin(2 * np.pi * 2 * f * 2 ** (det / 12) * t + ph)
    env = np.clip(t / 0.6, 0, 1) * np.clip((dur - t) / 0.5, 0, 1)
    return lowpass(x * env, cutoff)


def shaker(dur=0.09):
    return highpass(noise(dur), 5000) * env_exp(dur, 0.025, 0.006)


def snap():
    d = 0.12
    x = lowpass(highpass(noise(d), 1800), 6000) * env_exp(d, 0.018, 0.001)
    return x + 0.3 * sine(1300, d) * env_exp(d, 0.01)


def pulse(midi):
    """Soft heartbeat-like low tone for the tension section."""
    d = 0.5
    return sine(note_hz(midi), d) * env_exp(d, 0.12, 0.01)


def boom():
    d = 2.5
    return (sine(lambda t: 45 + 30 * np.exp(-t / 0.05), d) * env_exp(d, 0.6, 0.005)
            + 0.3 * lowpass(noise(d), 200) * env_exp(d, 0.3))


def reverse_swell(dur):
    """Reverse-cymbal style swell that ends exactly at its last sample."""
    t = t_axis(dur)
    x = highpass(noise(dur), 3000) * (t / dur) ** 3
    return lowpass(x, 9000)


def _rms_db(x):
    r = np.sqrt(np.mean(x ** 2)) if len(x) else 0
    return 20 * np.log10(r) if r > 0 else -120


def _level(x, target_db):
    cur = _rms_db(x[np.abs(x) > 1e-6]) if np.any(np.abs(x) > 1e-6) else -120
    return x * 10 ** ((target_db - cur) / 20) if cur > -100 else x


def music(duration, out_path, cues=()):
    """Render a music bed of exactly `duration` seconds that follows `cues`.

    cues: iterable of (time, kind, value) with kind in {"section", "hit", "final"}.
    """
    beat = 60 / BPM
    bar = 4 * beat
    n = int(duration * SR) + SR
    cues = sorted(cues, key=lambda c: c[0])
    sections = [(0.0, "main")] + [(t, v) for t, k, v in cues if k == "section"]
    hits = [t for t, k, _ in cues if k == "hit"]
    finals = [t for t, k, _ in cues if k == "final"]
    t_final = finals[0] if finals else max(0.0, duration - 3.0)

    def section_at(t):
        cur = sections[0][1]
        for ts, name in sections:
            # Changes take effect on the nearest bar line.
            if round(ts / bar) * bar <= t + 1e-6:
                cur = name
        return cur

    layers = {k: np.zeros(n) for k in LAYER_LEVEL_DB}
    bars = int(np.ceil(t_final / bar)) + 1
    pizz_pattern = [0, 2, 1, 3, 2, 1, 3, 2]          # chord-tone index per 8th note
    for b in range(bars):
        t0 = b * bar
        root, tones = PROGRESSION[b % len(PROGRESSION)]
        place(layers["pad"], soft_pad(tones, bar + 0.5), t0)
        for k, idx in enumerate(pizz_pattern):
            m = tones[idx] + (12 if k in (3, 7) else 0)
            vel = 1.0 if k % 2 == 0 else 0.7
            place(layers["pizz"], pluck(m, 0.45, 0.45) * vel, t0 + k * beat / 2)
        place(layers["bass"], pluck(root, 1.1, 0.3, 0.998), t0)
        place(layers["bass"], pluck(root + 7, 0.9, 0.3, 0.998) * 0.8, t0 + 2.5 * beat)
        place(layers["bell"], glock(tones[3] + 12), t0)
        place(layers["bell"], glock(tones[1] + 24) * 0.6, t0 + 2.5 * beat)
        for k in range(16):
            vel = (1.0, 0.45, 0.7, 0.45)[k % 4]
            place(layers["shaker"], shaker() * vel, t0 + k * beat / 4 + (0.012 if k % 2 else 0))
        for k in (1, 3):
            place(layers["snap"], snap(), t0 + k * beat)
        for k in range(4):
            place(layers["pulse"], pulse(root + 12) * (1.0 if k % 2 == 0 else 0.6), t0 + k * beat)

    # Bring every layer to its reference loudness, then apply section gains.
    for k in layers:
        layers[k] = _level(layers[k], LAYER_LEVEL_DB[k])
    ramp = int(0.08 * SR)
    for k in layers:
        g = np.zeros(n)
        for b in range(bars):
            i0, i1 = int(b * bar * SR), min(n, int((b + 1) * bar * SR))
            g[i0:i1] = SECTION_GAINS[section_at(b * bar)][k]
        g = np.convolve(g, np.ones(ramp) / ramp, mode="same")      # click-free changes
        layers[k] *= g

    mix = (reverb(layers["pizz"] + layers["bell"], 0.28)[:n] + reverb(layers["pad"], 0.35)[:n]
           + layers["bass"] + layers["shaker"] + layers["snap"] + layers["pulse"])

    # Stop the loop at the final cue; the closing chord rings on.
    i_final = int(t_final * SR)
    cut = np.ones(n)
    fade = int(0.12 * SR)
    cut[i_final:i_final + fade] = np.linspace(1, 0, len(cut[i_final:i_final + fade]))
    cut[i_final + fade:] = 0
    mix *= cut
    end = np.zeros(n)
    froot, ftones = FINAL_CHORD
    tail = duration - t_final + 0.5
    place(end, _level(soft_pad(ftones[:4], tail, 1600), LAYER_LEVEL_DB["pad"] + 3), t_final)
    for i, m in enumerate(ftones):
        place(end, _level(pluck(m, 2.5, 0.5, 0.998), LAYER_LEVEL_DB["pizz"]) * 0.8,
              t_final + i * 0.035)
    place(end, _level(glock(ftones[-1] + 12, 3.0), LAYER_LEVEL_DB["bell"] + 4), t_final)
    place(end, _level(pluck(froot, 3.0, 0.3, 0.999), LAYER_LEVEL_DB["bass"]), t_final)
    mix += reverb(end, 0.35)[:n]

    # Hits: reverse swell into a soft boom and a bell chord.
    fx = np.zeros(n)
    for th in hits + finals:
        sw = reverse_swell(bar / 2)
        place(fx, _level(sw, -30), th - len(sw) / SR)
        place(fx, _level(boom(), -24), th)
        root, tones = PROGRESSION[int(th // bar) % len(PROGRESSION)]
        for m in tones:
            place(fx, _level(glock(m + 12, 2.0), -33), th)
    mix += reverb(fx, 0.3)[:n]

    mix = mix[: int(duration * SR)]
    t = t_axis(duration)
    mix *= np.clip(t / 0.4, 0, 1) * np.clip((duration - t) / 0.4, 0, 1)
    mix = normalize(mix, 0.85)
    return write_wav(out_path, mix, stereo_width=0.3)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sfx"
    if cmd == "music":
        # python -m reelkit.audio music <duration> <out.wav> [cues.json]
        cues = ()
        if len(sys.argv) > 4:
            import json
            cues = [tuple(c) for c in json.loads(Path(sys.argv[4]).read_text())["cues"]]
        print(music(float(sys.argv[2]), sys.argv[3], cues))
    else:
        for name in SFX:
            p = SFX_DIR / f"{name}.wav"
            write_wav(p, SFX[name]())
            print(p)
