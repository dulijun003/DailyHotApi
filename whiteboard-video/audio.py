"""Synthesise background music + SFX for the whiteboard sample.

usage: python3 audio.py events.json out.wav [duration]
events.json = pencil stroke [start, end] pairs exported by `node render.js events`.
"""
import json, sys
import numpy as np

SR = 48000
events = json.load(open(sys.argv[1]))
out = sys.argv[2]
DUR = float(sys.argv[3]) if len(sys.argv) > 3 else 33.2
N = int(DUR * SR) + SR
rs = np.random.default_rng(3)

def mtof(m): return 440.0 * 2 ** ((m - 69) / 12)
def env_adsr(n, a=0.005, d=0.3, s=0.0, r=0.2):
    t = np.arange(n) / SR
    e = np.where(t < a, t / a, s + (1 - s) * np.exp(-(t - a) / d))
    tail = int(r * SR)
    if tail and n > tail: e[-tail:] *= np.linspace(1, 0, tail)
    return e
def add(buf, x, at, gain=1.0, pan=0.0):
    i = int(at * SR)
    if i >= len(buf): return
    x = x[: len(buf) - i]
    l, r = np.cos((pan + 1) * np.pi / 4), np.sin((pan + 1) * np.pi / 4)
    buf[i:i + len(x), 0] += x * gain * l
    buf[i:i + len(x), 1] += x * gain * r
def bandpass(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    X[(f < lo) | (f > hi)] = 0
    return np.fft.irfft(X, len(x))

def pluck(freq, dur=0.9, bright=1.0):
    n = int(dur * SR); t = np.arange(n) / SR
    y = sum((0.6 ** k) * bright ** k * np.sin(2 * np.pi * freq * (k + 1) * t + k) * np.exp(-t * (3 + 2.5 * k)) for k in range(6))
    return y * env_adsr(n, 0.004, 0.5, 0, 0.05)
def piano(freq, dur=1.6):
    n = int(dur * SR); t = np.arange(n) / SR
    det = [1, 1.0015, 0.9985]
    y = sum(sum((0.5 ** k) * np.sin(2 * np.pi * freq * d * (k + 1) * t) * np.exp(-t * (1.6 + 1.4 * k)) for k in range(5)) for d in det) / 3
    return y * env_adsr(n, 0.006, 1.2, 0, 0.1)
def pad(freqs, dur):
    n = int(dur * SR); t = np.arange(n) / SR
    y = sum(np.sin(2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 0.2 * t)) + 0.3 * np.sin(2 * np.pi * 2 * f * 1.003 * t) for f in freqs) / len(freqs)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (dur - t) / 0.6)
    return y * a
def bell(freq, dur=2.0):
    n = int(dur * SR); t = np.arange(n) / SR
    y = np.sin(2 * np.pi * freq * t) * np.exp(-t * 2.2) + 0.4 * np.sin(2 * np.pi * freq * 2.76 * t) * np.exp(-t * 4) + 0.2 * np.sin(2 * np.pi * freq * 5.4 * t) * np.exp(-t * 7)
    return y * env_adsr(n, 0.002, 5, 0, 0.1)
def kick():
    n = int(0.35 * SR); t = np.arange(n) / SR
    f = 50 + 80 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def shaker():
    n = int(0.08 * SR)
    return bandpass(rs.standard_normal(n), 5000, 14000) * np.exp(-np.arange(n) / SR * 60)
def snap():
    n = int(0.18 * SR)
    return bandpass(rs.standard_normal(n), 1200, 7000) * np.exp(-np.arange(n) / SR * 28)

mus = np.zeros((N, 2))
BPM = 100; beat = 60 / BPM; bar = 4 * beat
chords = [  # (bass, chord tones)
    (41, [53, 57, 60, 64]),  # Fmaj7
    (43, [55, 59, 62, 64]),  # G6
    (40, [52, 55, 59, 62]),  # Em7
    (45, [57, 60, 64, 67]),  # Am7
]
nbars = int(np.ceil(DUR / bar)) + 1
arp = [0, 1, 2, 3, 2, 1, 2, 3]
motif = [(0, 76), (1.5, 74), (2, 72), (3, 74), (4, 76), (6, 79), (6.5, 76)]  # beats within 2 bars
for b in range(nbars):
    t0 = b * bar
    bass, ch = chords[b % 4]
    add(mus, pad([mtof(m) for m in ch], bar + 0.5), t0, 0.05)
    for k, idx in enumerate(arp):
        add(mus, pluck(mtof(ch[idx] + 12), 0.8, 0.9), t0 + k * beat / 2, 0.075, pan=-0.25 + 0.5 * (k % 2))
    add(mus, piano(mtof(bass + 12), 2.4), t0, 0.12)
    if t0 >= 2.4:
        add(mus, piano(mtof(bass), 1.2), t0 + 2 * beat, 0.07)
    if t0 >= 4.8:  # groove enters after the first "success"
        for k in range(4):
            if k % 2 == 0: add(mus, kick(), t0 + k * beat, 0.28)
            else: add(mus, snap(), t0 + k * beat, 0.05)
        for k in range(8): add(mus, shaker(), t0 + k * beat / 2 + 0.01, 0.03 if k % 2 else 0.018, pan=0.3)
    if b % 2 == 0 and t0 >= 9.6:
        for off, m in motif: add(mus, bell(mtof(m)), t0 + off * beat, 0.035, pan=0.15)

# simple reverb
ir_n = int(1.2 * SR); ir = rs.standard_normal(ir_n) * np.exp(-np.arange(ir_n) / SR * 4.5); ir[0] = 0
for c in range(2):
    wet = np.fft.irfft(np.fft.rfft(mus[:, c], N + ir_n) * np.fft.rfft(ir * 0.03, N + ir_n), N + ir_n)[:N]
    mus[:, c] += wet

# ---- SFX ----
sfx = np.zeros((N, 2))
# pencil scratch following stroke events
for a, b in events:
    if b <= 0 or a >= DUR: continue
    a = max(a, 0); n = int((b - a) * SR) + int(0.03 * SR)
    if n < 200: continue
    x = bandpass(rs.standard_normal(n), 2500, 9000)
    t = np.arange(n) / SR
    am = 0.55 + 0.45 * np.abs(np.sin(2 * np.pi * (7 + rs.random() * 6) * t + rs.random() * 6))
    e = np.minimum(1, t / 0.015) * np.minimum(1, (t[-1] - t) / 0.03 + 1e-3)
    add(sfx, x * am * e, a, 0.022, pan=rs.uniform(-0.2, 0.2))
# whoosh on the whip transition
n = int(0.75 * SR); t = np.arange(n) / SR
wh = rs.standard_normal(n)
segs = np.array_split(wh, 30)
wh = np.concatenate([bandpass(s, 300 + 3000 * (i / 30), 1200 + 6000 * (i / 30)) for i, s in enumerate(segs)])
wh *= np.sin(np.pi * t / t[-1]) ** 2
add(sfx, wh, 18.95, 0.5)
# soft thumps for failed launches
for tb in (22.42, 24.62, 26.3):
    n = int(0.5 * SR); t = np.arange(n) / SR
    th = np.sin(2 * np.pi * np.cumsum(70 + 60 * np.exp(-t * 20)) / SR) * np.exp(-t * 7) + 0.3 * bandpass(rs.standard_normal(n), 100, 900) * np.exp(-t * 10)
    add(sfx, th, tb, 0.25)
# success chimes
for ts in (6.45, 28.5):
    for k, m in enumerate([79, 84, 88]):
        add(sfx, bell(mtof(m), 1.8), ts + k * 0.07, 0.06, pan=0.2)

mix = mus * 0.9 + sfx
# fade in/out
t = np.arange(N) / SR
mix *= np.clip(t / 0.05, 0, 1)[:, None] * np.clip((DUR - t) / 1.6, 0, 1)[:, None]
mix = mix[: int(DUR * SR)]
rms = np.sqrt(np.mean(mix ** 2)); mix *= 10 ** (-17 / 20) / rms
peak = np.abs(mix).max()
if peak > 0.89: mix *= 0.89 / peak
import wave
with wave.open(out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(mix, -1, 1) * 32767).astype('<i2').tobytes())
print('wrote', out, f'{len(mix)/SR:.2f}s', 'rms dBFS', round(20 * np.log10(np.sqrt(np.mean(mix**2))), 1))
