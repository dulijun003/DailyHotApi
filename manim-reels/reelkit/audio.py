"""Procedural audio: sound effects and background music, synthesised with numpy.

Everything is generated from code, so there are no licensing issues and the
output is identical on every machine. Files are cached under reelkit/assets/.

    python -m reelkit.audio music 52 out.wav     # 52 s music bed
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

# Calm, curious lo-fi loop in A minor: Am9 - Fmaj7 - C(add9) - G6, 84 BPM.
PROGRESSION = [
    (57, [0, 3, 7, 10, 14]),   # Am9
    (53, [0, 4, 7, 11, 14]),   # Fmaj9
    (48, [0, 4, 7, 14, 16]),   # Cadd9
    (55, [0, 4, 7, 9, 14]),    # G6/9
]
BPM = 84


def _pad(root, intervals, dur):
    t = t_axis(dur)
    x = np.zeros_like(t)
    for iv in intervals[:4]:
        f = note_hz(root + 12 + iv)
        for det in (-0.12, 0.12):                       # detuned pair = warmth
            x += sine(f * 2 ** (det / 12), dur, phase=RNG.uniform(0, 6.28))
    att = np.clip(t / 0.8, 0, 1)
    rel = np.clip((dur - t) / 0.6, 0, 1)
    return lowpass(x * att * rel, 900) * 0.07


def _pluck(midi, dur=0.6):
    f = note_hz(midi)
    x = sine(f, dur) + 0.35 * sine(2 * f, dur) + 0.1 * sine(3 * f, dur)
    return lowpass(x * env_exp(dur, 0.22), 2600) * 0.09


def _bass(midi, dur):
    t = t_axis(dur)
    x = sine(note_hz(midi - 12), dur) + 0.25 * sine(note_hz(midi), dur)
    return x * np.clip(t / 0.02, 0, 1) * np.exp(-t / 0.9) * 0.16


def _kick():
    d = 0.35
    return sine(lambda t: 48 + 110 * np.exp(-t / 0.03), d) * env_exp(d, 0.11) * 0.28


def _hat(open_=False):
    d = 0.12 if open_ else 0.04
    return highpass(noise(d), 6000) * env_exp(d, 0.04 if open_ else 0.012) * 0.05


def _snare():
    d = 0.2
    x = lowpass(highpass(noise(d), 1200), 5000) * env_exp(d, 0.05) * 0.09
    return x + sine(190, d) * env_exp(d, 0.04) * 0.05


def music(duration, out_path, intro_bars=1):
    """Render a music bed of exactly `duration` seconds to `out_path`."""
    beat = 60 / BPM
    bar = 4 * beat
    n = int((duration + 2) * SR)
    pads = np.zeros(n)
    keys = np.zeros(n)
    low = np.zeros(n)
    drums = np.zeros(n)

    # Arpeggio pattern (eighth notes) through each chord's tones.
    arp = [0, 2, 4, 3, 1, 3, 4, 2]
    kick_c, hat_c, hat_o, snare_c = _kick(), _hat(), _hat(True), _snare()

    bars = int(np.ceil(duration / bar)) + 1
    for b in range(bars):
        root, ivs = PROGRESSION[b % len(PROGRESSION)]
        t0 = b * bar
        place(pads, _pad(root, ivs, bar + 0.6), t0)
        place(low, _bass(root, bar), t0)
        place(low, _bass(root + 7, beat * 1.5), t0 + beat * 2.5)
        for k, step in enumerate(arp):
            jitter = RNG.normal(0, 0.006)
            midi = root + 24 + ivs[step]
            place(keys, _pluck(midi) * RNG.uniform(0.7, 1.0), t0 + k * beat / 2 + jitter)
        if b >= intro_bars:                       # drums enter after the intro
            for k in range(4):                    # kick on 1 & 3, snare on 2 & 4
                place(drums, kick_c if k % 2 == 0 else snare_c, t0 + k * beat)
            place(drums, kick_c * 0.6, t0 + 2.5 * beat)
            for k in range(8):
                swing = 0.03 if k % 2 else 0.0
                clip = hat_o if k == 7 else hat_c
                place(drums, clip * (1.0 if k % 2 == 0 else 0.7), t0 + k * beat / 2 + swing)

    keys = reverb(keys, 0.35)[:n]
    pads = reverb(pads, 0.3)[:n]
    mix = pads + keys + low + drums

    # Lo-fi colour: gentle low-pass and a little vinyl noise.
    mix = lowpass(mix, 6000) + lowpass(noise(len(mix) / SR), 3000) * 0.004

    mix = mix[: int(duration * SR)]
    t = t_axis(duration)
    fade = np.clip(t / 1.5, 0, 1) * np.clip((duration - t) / 2.5, 0, 1)
    mix = normalize(mix * fade, 0.8)
    return write_wav(out_path, mix, stereo_width=0.35)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "sfx"
    if cmd == "music":
        print(music(float(sys.argv[2]), sys.argv[3]))
    else:
        for name in SFX:
            p = SFX_DIR / f"{name}.wav"
            write_wav(p, SFX[name]())
            print(p)
