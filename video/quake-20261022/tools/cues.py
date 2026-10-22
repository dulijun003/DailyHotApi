"""timeline.json -> audio/cues.json for core/render/srt.py (one Chinese line + one English line per cue),
and checks the subtitle timing rules: every cue >= 1.8 s and >= its spoken line + 0.6 s."""
import json, os, re
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tl = json.load(open(os.path.join(D, 'timeline.json'))); dur = json.load(open(os.path.join(D, 'audio', 'vo', 'dur.json')))
clean = lambda s: re.sub(r'[|{}]', '', s)
cues = [{'t0': c['t0'], 't1': c['t1'], 'text': clean(c['zh']) + '\n' + c['en']} for c in tl['caps']]
json.dump(cues, open(os.path.join(D, 'audio', 'cues.json'), 'w'), ensure_ascii=False, indent=1)
spans = sorted((st, st + dur[k]) for k, st in tl['vo'].items()); bad = 0
for c in cues:
    d = c['t1'] - c['t0']; spoken = sum(max(0, min(b, c['t1']) - max(a, c['t0'])) for a, b in spans)
    ok = d >= 1.8 - 1e-6 and (spoken < .3 or d >= spoken + .6 - 1e-6); bad += not ok
    print(f"{'OK ' if ok else 'BAD'} {c['t0']:5.2f}-{c['t1']:5.2f} {d:4.2f}s spoken {spoken:4.2f}s  {c['text'].splitlines()[0]}")
# a voice line that runs past the end of every caption covering it
for k, st in tl['vo'].items():
    e = st + dur[k]; cov = [c for c in cues if c['t0'] - .35 <= st < c['t1']]
    if not cov or max(c['t1'] for c in cues if c['t0'] < e) < e - .05: bad += 1; print('BAD voice uncovered', k, st, e)
print('cues', len(cues), 'bad', bad)
