"""Score + foley + voice + wind -> out/mix.wav and audio/stems/*.wav (48 kHz stereo). Loudness is set by core/render/mux.sh.
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
STOP, HIT, SOUT, VERD = M['stop'], M['hit'], M['strings_out'], M['verdict']
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
NOTE = {'D': 50, 'Bb': 46, 'F': 53, 'C': 48, 'G': 55, 'A': 57}
PROG = [('D', 'm'), ('Bb', ''), ('F', ''), ('C', '')]          # one chord per bar in the groove
def chord_at(t):
    if t < STOP: return PROG[int(t // 2) % 4]
    if t < SOUT: return [('D', 'm'), ('D', 'm'), ('Bb', ''), ('A', '')][int((t - HIT) // 4) % 4]
    return [('F', ''), ('Bb', ''), ('F', ''), ('C', ''), ('F', '')][min(4, int((t - 55.0) // 1.5))]
def tones(r, q, base=60):
    pc = NOTE[r] % 12; third = 3 if q == 'm' else 4
    return sorted(base + ((p - base) % 12) for p in (pc, pc + third, pc + 7))
def section(t):
    if t < 3.0: return 'open'        # kick, hats, marimba only: the question
    if t < 7.5: return 'wall'        # bass joins
    if t < 29.0: return 'groove'     # full groove, vibes off-beats
    if t < STOP: return 'build'      # snare eighths → sixteenths under the scroll
    if t < HIT: return 'sil'         # silence 1: voice only
    if t < SOUT: return 'quake'      # half time, low strings
    if t < 55.0: return 'sil'        # silence 2: wind only
    return 'end'

KIT = 'drum_kit'
t = 0.0
while t < DUR - 1e-6:
    sec = section(t); b16 = int(round(t / S16)); beat = b16 // 4; sub = b16 % 4; bb = beat % 4; ch = chord_at(t)
    if sec in ('open', 'wall', 'groove', 'build'):
        if sub == 0: n(t, KIT, 'kick_drum_left', None, .78 if bb in (0, 2) else .6, 0, .9)
        if sub == 2: n(t, KIT, 'hi_hat_closed', None, .5, .25, .42)
        if sec == 'groove' and sub in (1, 3): n(t, KIT, 'hi_hat_closed', None, .28, .25, .28)
        if sec in ('groove',) and sub == 0 and bb in (1, 3): n(t, KIT, 'snare_1', None, .6, .05, .6)
        if sec != 'open' and sub in (0, 2):
            r, q = ch; m = NOTE[r] - 24 + (12 if (b16 // 2) % 4 == 3 else 0); n(t, 'electric_bass', m, .22, .7, 0, .95)
        if sec != 'build':
            tn = tones(*ch, base=69); m = tn[[0, 1, 2, 1][sub]] + (12 if (beat % 2 and sub == 2) else 0)
            n(t, 'marimba', m, .12, .4 if sub == 0 else .28, .35, .34)
        if sec == 'groove' and sub == 2 and bb in (0, 2):
            for m in tones(*ch, base=64): n(t, 'vibraphone', m, .4, .36, -.3, .34)
        if sec == 'build':
            rate = 2 if t < 30.5 else 1
            if b16 % rate == 0: n(t, 'snare', 'on', None, .3 + .5 * (t - 29.0) / 2.5, .05, .5)
    elif sec == 'quake':
        r, q = ch
        if sub == 0 and bb == 0: n(t, KIT, 'kick_drum_left', None, .8, 0, .9)
        if sub == 0 and bb == 2 and t >= 37.0: n(t, KIT, 'snare_1', None, .45, .05, .45)
        if sub == 2 and bb in (1, 3): n(t, KIT, 'hi_hat_closed', None, .25, .25, .22)
        if sub == 0 and bb in (0, 2) and t < 51.5: n(t, 'cellos_spic', NOTE[r] - 12, .25, .5, -.25, .5)
        if abs((t - HIT) % 4) < 1e-6:   # held low strings, one chord per two bars
            for m in tones(r, q, base=50): n(t, 'cellos', m, 4.0, .45, -.2, .42)
            n(t, 'contrabass', NOTE[r] - 12 if NOTE[r] - 12 >= 30 else NOTE[r], 4.0, .5, 0, .5)
        if t < 51.5 and sub == 0 and bb == 1: n(t, 'marimba', tones(r, q, 74)[0], .2, .25, .35, .22)
    elif sec == 'end':
        if abs(((t - 55.0) / 1.5) - round((t - 55.0) / 1.5)) < 1e-6 and t < VERD:
            for m in tones(*ch, base=60): n(t, 'vibraphone', m, 1.4, .32, -.2, .38)
    t = round(t + S16, 6)

# structural hits
n(.13, KIT, 'crash_left', None, .5, .3, .35); n(.13, 'glockenspiel', 86, .4, .45, .3, .3)              # frame-4 highlighter
n(.6, 'trumpet_stac', 74, .25, .7, .2, .4); n(.6, 'trombone_stac', 50, .3, .7, -.2, .45)                # 478万
for m in (74, 77, 81): n(5.55, 'trumpet_stac', m, .3, .8, .2, .5)                                       # 378 lands
n(5.55, 'trombone_stac', 50, .35, .8, -.2, .55); n(5.55, KIT, 'crash_right', None, .7, -.3, .45)
for i, tt in enumerate((11.25, 11.4, 11.55, 11.7)): n(tt, 'glockenspiel', (81, 84, 86, 89)[i], .3, .5, .3, .32)   # panels light
n(12.05, 'trumpet_stac', 77, .3, .75, .2, .45); n(12.05, 'trombone_stac', 53, .35, .75, -.2, .5)      # 合计 10
n(16.85, 'trombone_stac', 46, .35, .85, -.2, .55); n(16.85, 'timpani', 'D2', 1.0, .7, 0, .6)          # the "3"
n(17.6, 'glockenspiel', 81, .4, .4, .3, .28)
for i in range(7): n(25.0 + i * .2, 'glockenspiel', 74 + (0, 2, 5, 7, 9, 12, 14)[i], .2, .38, .3, .26)  # seven No.1s
n(29.0, 'sus_cymbal', 'cresc', 2.5, .55, .2, .5)
# silence 1 is broken by the most important sound: the quake, low
n(HIT, 'timpani', 'D2', 2.0, 1.0, 0, 1.0); n(HIT, 'bass_drum', None, None, .95, 0, .9)
n(37.35, 'timpani', 'A1', 1.5, .8, 0, .75); n(37.35, 'bass_drum', None, None, .7, 0, .6)               # 7.0
n(47.5, 'sus_cymbal', 'cresc', 1.5, .45, .2, .4); n(49.0, 'timpani', 'D2', 1.2, .7, 0, .6)            # 双榜第一
# verdict: bells and glockenspiel, F major, soft
n(VERD, 'tubular_bells', 65, 3.0, .45, .2, .4); n(VERD, 'vibraphone', 57, 3.0, .35, -.2, .35)
for m in (60, 65, 69): n(VERD, 'vibraphone', m, 2.8, .32, -.2, .32)
for i, m in enumerate((77, 81, 84, 89)): n(VERD + .25 + i * .5, 'glockenspiel', m, .8, .35, .3, .26)
n(VERD, 'contrabass', 41, 3.0, .4, 0, .4)

def silent(t): return STOP - 1e-6 <= t < HIT or SOUT - 1e-6 <= t < 55.0
E = [e for e in E if not silent(e[0]) or e[1] == 'sus_cymbal']
mus = S.render(E, dur=DUR, master=False).astype(np.float32)
mus = S.room(mus, size=.34, mix=.13)
g = np.ones(N, np.float32)
i0, i1 = int(STOP * SR), int(HIT * SR); g[i0:i1] = 0; g[i0:i0 + int(.012 * SR)] = np.linspace(1, 0, int(.012 * SR))   # hard stop
j0, j1 = int((SOUT - 1.0) * SR), int(SOUT * SR); g[j0:j1] = np.minimum(g[j0:j1], np.linspace(1, 0, j1 - j0)); g[j1:int(55.0 * SR)] = 0   # strings out
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
    elif ty == 'cut' and e.get('k') in ('grid', 'score', 'map', 'split'): put(fx, paper(.25), t, .25, .2)

# ----------------------------------------------------------------- wind on the plateau (synthesised): low under the quake, J-cut into the photo, alone in silence 2
amb = buf()
def wind(d, seed):
    r = np.random.default_rng(seed); x = r.standard_normal(int(d * SR)).astype(np.float32)
    tt = np.arange(len(x)) / SR; gust = .55 + .45 * np.sin(2 * np.pi * .23 * tt + 1.3) * np.sin(2 * np.pi * .071 * tt)
    return norm(lp(bp(x, 120, 900), 700) * gust)
def bed(at, d, gain, fi, fo, seed):
    x = wind(d, seed); tt = np.arange(len(x)) / SR; x *= np.minimum(1, tt / fi) * np.minimum(1, (d - tt) / fo)
    put(amb, np.stack([x, np.roll(x, 900)], 1) * .5, at, gain)
bed(HIT, SOUT - HIT, .04, 1.0, .6, 1)
bed(51.2, DUR - 51.2, .14, .3, 1.4, 2)   # J-cut 0.3 s before the photo, carries over silence 2 and the ending

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
