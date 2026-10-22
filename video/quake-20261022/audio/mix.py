"""Quake film. Score + foley + voice + wind -> out/mix.wav and audio/stems/*.wav (48 kHz stereo). Loudness is set by core/render/mux.sh.
Reads: ../timeline.json (voice starts, music marks), ../events.json (every on-screen action, from events.mjs), audio/vo/*.wav (edge-tts).
Score: 120 BPM (beat 0.5 s, bar 2 s). D minor news groove (Dm–Bb–F–C) for the lists; a snare build under the scroll;
a hard stop into silence at the freeze; the quake answers on timpani in half time over low strings (no brass);
strings out, half a second of wind alone, then soft vibraphone and bells for the verdict (F major, no brass, no crash)."""
import json, os, sys
import numpy as np, soundfile as sf, soxr
H = os.path.dirname(os.path.abspath(__file__)); D = os.path.dirname(H)
LIB = os.environ.get('LIB', os.path.abspath(os.path.join(D, '..', '..')))
sys.path.insert(0, LIB); sys.path.insert(0, os.path.join(LIB, 'core', 'audio'))
from core.audio import sampler as S
import sfx
from sfx import SR, t_, bp, lp, hp, noise, norm

TL = json.load(open(os.path.join(D, 'timeline.json')))
EV = json.load(open(os.path.join(D, 'events.json')))['ev']
DUR = TL['dur']; N = int(DUR * SR); S16 = .125; M = TL['music']
S.seed(11)

def buf(): return np.zeros((N, 2), np.float32)
def put(b, x, at, g=1.0, pan=0.0):
    i = int(round(at * SR)); x = np.asarray(x, np.float32)
    if i < 0: x = x[-i:]; i = 0
    if i >= N: return
    if x.ndim == 2: x = x[:max(0, N - i)]; b[i:i + len(x)] += x * g; return
    x = x[:max(0, N - i)]; l, r = np.sqrt(.5 * (1 - pan)), np.sqrt(.5 * (1 + pan))
    b[i:i + len(x), 0] += x * g * l * 1.414; b[i:i + len(x), 1] += x * g * r * 1.414

# ----------------------------------------------------------------- score
E = []
def n(t, inst, p, d, v, pan=0, g=1.0): E.append((t, inst, p, d, v, pan, g))
NOTE = {'D': 50, 'Bb': 46, 'F': 53, 'C': 48, 'A': 45, 'G': 43}
PROG = [('D', 'm'), ('D', 'm'), ('Bb', ''), ('A', '')]          # a grave D minor, one chord per bar
def chord_at(t): return PROG[int(t // 2) % 4]
def tones(r, q, base=60):
    pc = NOTE[r] % 12; third = 3 if q == 'm' else 4
    return sorted(base + ((p - base) % 12) for p in (pc, pc + third, pc + 7))
SIL = [tuple(M['sil1']), tuple(M['sil2'])]; VERD = M['verdict']
def silent(t): return any(a - 1e-6 <= t < b for a, b in SIL)
KIT = 'drum_kit'
t = 0.0
while t < VERD - 1e-6:
    b16 = int(round(t / S16)); beat = b16 // 4; sub = b16 % 4; bb = beat % 4; r, q = chord_at(t)
    half = t >= 42.5                     # after the numbers: half time
    if t >= .5:
        if sub == 0 and (bb in (0, 2) if not half else bb == 0): n(t, KIT, 'kick_drum_left', None, .75, 0, .85)
        if sub == 2 and t >= 5.0: n(t, KIT, 'hi_hat_closed', None, .38, .25, .3)
        if not half and sub == 0 and bb == 2 and t >= 9.5: n(t, KIT, 'snare_1', None, .45, .05, .4)
        if half and sub == 0 and bb == 2: n(t, KIT, 'snare_1', None, .5, .05, .45)
        if t >= 5.0 and sub in (0, 2): n(t, 'electric_bass', NOTE[r] - 12 + (12 if (b16 // 2) % 4 == 3 else 0), .22, .62, 0, .85)
        if sub in (0, 2) and 9.5 <= t < 42.5: n(t, 'cellos_spic', NOTE[r], .2, .45, -.25, .42)
        if abs(t % 4) < 1e-6 and t < 61.3:     # held low strings
            for m in tones(r, q, base=50): n(t, 'cellos', m, 4.0, .4, -.2, .36)
            n(t, 'contrabass', NOTE[r] - 12 if NOTE[r] - 12 >= 30 else NOTE[r], 4.0, .45, 0, .45)
        if 5.0 <= t < 35.0 and sub == 0 and bb in (1, 3): n(t, 'marimba', tones(r, q, 74)[[0, 2][bb // 2]], .2, .3, .35, .26)
    t = round(t + S16, 6)
# hits
n(.13, 'timpani', 'D2', 2.0, .95, 0, .95); n(.13, 'bass_drum', None, None, .9, 0, .85); n(.13, KIT, 'crash_left', None, .5, .3, .35)
n(6.6, 'glockenspiel', 86, .5, .4, .3, .26)                                                    # lock
n(11.2, 'timpani', 'D2', 1.2, .75, 0, .65)                                                     # 10 km
for tt, m in ((17.1, 81), (19.1, 76)): n(tt, 'glockenspiel', m, .4, .38, .3, .24)              # rings
for i, tt in enumerate((22.6, 23.6, 24.1, 24.5, 24.9, 25.3, 25.8)): n(tt, 'marimba', 69 + (0, 2, 3, 5, 7, 8, 12)[i], .25, .4, .35, .3)
n(30.9, 'timpani', 'A1', 1.2, .7, 0, .6)                                                       # altitude
n(34.6, 'sus_cymbal', 'cresc', .85, .45, .2, .4)                                               # into silence 1
n(39.6, 'timpani', 'D2', 1.5, .85, 0, .8); n(39.6, 'bass_drum', None, None, .8, 0, .7)        # 7.0
n(44.4, 'timpani', 'A1', 1.2, .7, 0, .6)                                                       # the 4.2
n(50.4, 'timpani', 'D2', 1.0, .6, 0, .5)                                                       # 2 injured
n(61.0, 'sus_cymbal', 'cresc', 1.2, .35, .2, .3)
# verdict: soft bells and vibraphone, F major, no brass, no crash
n(VERD, 'tubular_bells', 65, 3.0, .42, .2, .38)
for m in (57, 60, 65, 69): n(VERD, 'vibraphone', m, 2.8, .32, -.2, .32)
for i, m in enumerate((77, 81, 84, 89)): n(VERD + .25 + i * .5, 'glockenspiel', m, .8, .33, .3, .24)
n(VERD, 'contrabass', 41, 3.0, .38, 0, .38)
E = [e for e in E if not silent(e[0]) or e[1] == 'sus_cymbal']
mus = S.render(E, dur=DUR, master=False).astype(np.float32)
mus = S.room(mus, size=.36, mix=.14)
g = np.ones(N, np.float32)
for a0, b0 in SIL:
    i0, i1 = int(a0 * SR), int(b0 * SR); g[i0:i1] = 0; g[i0:i0 + int(.012 * SR)] = np.linspace(1, 0, int(.012 * SR))
j0, j1 = int(61.3 * SR), int(SIL[1][0] * SR); g[j0:j1] = np.minimum(g[j0:j1], np.linspace(1, 0, j1 - j0) ** 1.5)
f0 = int((DUR - 1.2) * SR); g[f0:] *= np.linspace(1, 0, N - f0) ** 1.5
mus *= g[:, None]

# ----------------------------------------------------------------- voice
vo = buf()
for k, st in TL['vo'].items():
    x, sr = sf.read(os.path.join(H, 'vo', k + '.wav'), dtype='float32')
    if x.ndim > 1: x = x.mean(1)
    x = soxr.resample(x, sr, SR); x = hp(x, 90)
    x = sfx.compress(x, thr=.18, ratio=3.0); x = x / (np.sqrt(np.mean(x[np.abs(x) > .01] ** 2)) + 1e-9) * .12
    put(vo, x, st, 1.0, 0)

# ----------------------------------------------------------------- foley from the page's events
fx = buf(); rng = np.random.default_rng(5)
def tick(p=1.0, v=1.0): return sfx.click(p, v) * .6
def squeak(d):
    tt = t_(d); x = bp(noise(d), 1800, 5200) * (.6 + .4 * np.sin(2 * np.pi * 9 * tt)) * np.minimum(1, tt / .02) * np.minimum(1, (d - tt) / .03 + .01)
    return norm(x) * .5
def paper(d=.45): tt = t_(d); return norm(bp(noise(d), 500, 6000) * np.exp(-tt / .12) * (1 + .6 * np.sin(2 * np.pi * 23 * tt))) * .6
def riser(d):
    tt = t_(d); x = noise(d); y = np.zeros_like(x)
    for i in range(8):
        a, b = int(i * len(x) / 8), int((i + 1) * len(x) / 8); f = 400 * 2 ** (i * .6); y[a:b] = bp(x, f, f * 2.2)[a:b]
    return norm(y * (tt / d) ** 2) * .7
def shutter(): return norm(np.concatenate([sfx.click(.7, 1), np.zeros(int(.045 * SR)), sfx.click(.55, .8)])) * .8
def scroll(d):   # the list racing past: a dense paper flutter that slows to a stop
    tt = t_(d); rate = 60 * (1 - tt / d) ** 1.5 + 4; ph = np.cumsum(rate) / SR
    x = bp(noise(d), 1500, 7000) * (.5 + .5 * np.sign(np.sin(2 * np.pi * ph))) * (1 - .7 * tt / d)
    return norm(x) * .5
def ring(): tt = t_(1.2); return norm(np.sin(2 * np.pi * 52 * tt) * np.exp(-tt / .35) + .3 * np.sin(2 * np.pi * 104 * tt) * np.exp(-tt / .2)) * .8
for e in EV:
    t, ty = e['t'], e['type']
    if ty == 'slam': put(fx, sfx.click(.8, .7) * .3, t, .5 * e.get('big', 1)); put(fx, sfx.thump(.6, 90), t, .32 * e.get('big', 1))
    elif ty == 'rattle':
        k = 0
        while k * .045 < e['d']: put(fx, tick(1.2 + .3 * rng.random(), .6), t + k * .045, .22, rng.uniform(-.3, .3)); k += 1
    elif ty == 'whoosh': put(fx, sfx.whoosh(.32), t - .24, .42, rng.uniform(-.4, .4))
    elif ty == 'tick': put(fx, tick(1.4, .8), t, .4, .2)
    elif ty == 'marker': put(fx, squeak(e.get('d', .4)), t, .45, .15)
    elif ty == 'shutter': put(fx, shutter(), t - .02, .75)
    elif ty == 'hit': put(fx, sfx.thump(1.0, 50), t, .8)
    elif ty == 'stamp': put(fx, sfx.thump(.9, 80), t, .6); put(fx, sfx.click(.6, .8), t, .3)
    elif ty == 'pop': put(fx, sfx.pop(.8), t, .4, rng.uniform(-.3, .3))
    elif ty == 'paper': put(fx, paper(), t, .55, -.1)
    elif ty == 'punch': put(fx, sfx.whoosh(.25), t - .2, .5); put(fx, sfx.thump(1.0, 55), t, .7)
    elif ty == 'riser': put(fx, riser(e['d']), t, .32)
    elif ty == 'scroll': put(fx, scroll(e['d']), t, .55)
    elif ty == 'ring': put(fx, ring(), t, .45)
    elif ty == 'lock': put(fx, tick(1.6, .9), t, .45); put(fx, tick(1.3, .8), t + .08, .35)
    elif ty == 'drop': put(fx, sfx.whoosh(e['d']), t, .3)
    elif ty == 'draw': put(fx, squeak(e['d']) * .5, t, .3, .2)
    elif ty == 'grow': put(fx, squeak(e['d']) * .35, t, .25, .15)
    elif ty == 'strike': put(fx, squeak(.3), t, .5, -.1); put(fx, sfx.thump(.7, 70), t + .25, .4)
    elif ty == 'cut' and e.get('k') in ('depth', 'dist', 'two', 'resp'): put(fx, paper(.25), t, .25, .2)

# ----------------------------------------------------------------- wind (synthesised): the plateau shot and the ending
amb = buf()
def wind(d, seed):
    r = np.random.default_rng(seed); x = r.standard_normal(int(d * SR)).astype(np.float32)
    tt = np.arange(len(x)) / SR; gust = .55 + .45 * np.sin(2 * np.pi * .23 * tt + 1.3) * np.sin(2 * np.pi * .071 * tt)
    return norm(lp(bp(x, 120, 900), 700) * gust)
def bed(at, d, gain, fi, fo, seed):
    x = wind(d, seed); tt = np.arange(len(x)) / SR; x *= np.minimum(1, tt / fi) * np.minimum(1, (d - tt) / fo)
    put(amb, np.stack([x, np.roll(x, 900)], 1) * .5, at, gain)
bed(28.7, 7.4, .12, .3, .8, 1)   # the plateau: J-cut 0.3 s before the photo, alone in silence 1
bed(58.0, DUR - 58.0, .1, 1.0, 1.4, 2)   # under the ending and silence 2

# ----------------------------------------------------------------- mix
env = np.abs(vo[:, 0]); k = int(.08 * SR); env = np.convolve(env, np.ones(k) / k, 'same')
vk = np.clip(env / .03, 0, 1)
duck = 1 - .66 * vk
mus = mus - np.stack([bp(mus[:, c], 1200, 5000) for c in (0, 1)], 1) * .55 * vk[:, None]   # carve the consonant band under speech
mus_r = np.sqrt(np.mean(mus[np.abs(mus).max(1) > 1e-4] ** 2)) + 1e-9; mus *= .04 / mus_r
fxduck = 1 - .5 * vk
mix = mus * duck[:, None] + fx * fxduck[:, None] * .5 + vo + amb
mix = np.stack([sfx.limit(mix[:, c], .95) for c in (0, 1)], 1)
os.makedirs(os.path.join(D, 'out'), exist_ok=True); os.makedirs(os.path.join(H, 'stems'), exist_ok=True)
sf.write(os.path.join(D, 'out', 'mix.wav'), mix.astype(np.float32), SR)
for name, x in (('music', mus * duck[:, None]), ('fx', fx * fxduck[:, None] * .5), ('vo', vo), ('amb', amb)): sf.write(os.path.join(H, 'stems', name + '.wav'), x.astype(np.float32), SR)
print('mix', DUR, 's  peak', float(np.abs(mix).max()), ' music events', len(E))
