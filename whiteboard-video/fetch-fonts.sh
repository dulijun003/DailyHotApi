#!/usr/bin/env bash
# Downloads the fonts used by the renderer into ./fonts
#   Xiaolai (CJK handwriting) from the @excalidraw/excalidraw npm package
#   Klee One (Latin handwriting) + Noto Sans SC (subtitles) from Google Fonts
set -euo pipefail
cd "$(dirname "$0")"
pip install -q fonttools brotli >/dev/null
tmp=$(mktemp -d)
(cd "$tmp" && npm init -y >/dev/null && npm i --silent --ignore-scripts @excalidraw/excalidraw@0.18.1)
mkdir -p fonts/g
cp -r "$tmp/node_modules/@excalidraw/excalidraw/dist/prod/fonts/Xiaolai" fonts/
rm -rf "$tmp"
python3 - <<'PY'
import glob, re, os, hashlib, subprocess
from fontTools.ttLib import TTFont
def ranges(cps):
    cps = sorted(cps); out = []; s = p = cps[0]
    for c in cps[1:]:
        if c == p + 1: p = c; continue
        out.append((s, p)); s = p = c
    out.append((s, p))
    return ','.join(f'U+{a:X}' if a == b else f'U+{a:X}-{b:X}' for a, b in out)
css = []
for f in sorted(glob.glob('fonts/Xiaolai/*.woff2')):
    cps = list(TTFont(f).getBestCmap().keys())
    css.append(f"@font-face{{font-family:'Xiaolai';src:url('{f[6:]}') format('woff2');unicode-range:{ranges(cps)};font-display:block}}")
open('fonts/fonts.css', 'w').write('\n'.join(css))
UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120 Safari/537.36'
def gcss(spec):
    s = subprocess.run(['curl', '-s', '-A', UA, f'https://fonts.googleapis.com/css2?family={spec}&display=block'], capture_output=True, text=True).stdout
    def rep(m):
        u = m.group(1); fn = 'g/' + hashlib.md5(u.encode()).hexdigest()[:12] + '.woff2'
        if not os.path.exists('fonts/' + fn): subprocess.run(['curl', '-s', '-o', 'fonts/' + fn, u])
        return f"url('{fn}')"
    return re.sub(r"url\((https://[^)]+)\)", rep, s)
open('fonts/g_NotoSansSC.css', 'w').write(gcss('Noto+Sans+SC:wght@700'))
klee = gcss('Klee+One:wght@600')
blocks = re.findall(r'/\* ([\w-]+) \*/\s*(@font-face\s*\{[^}]*\})', klee)
open('fonts/klee-latin.css', 'w').write('\n'.join(b.replace("'Klee One'", "'KleeLatin'") for n, b in blocks if n in ('latin', 'latin-ext')))
print('fonts ready')
PY
