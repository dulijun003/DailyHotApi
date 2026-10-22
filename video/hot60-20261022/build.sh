#!/bin/sh
# 热榜60秒 · 10.22 (Caption News, vertical 1080×1920, 30 fps): one-command build.
# data snapshot → lists → frames → voice (+ speech check) → cues → reading check → events → picture → mix → .srt → master → poster
# Needs the library set up with `setup.sh deps voice music` and the freepats / vsco2ce / vcsl sample packs.
# Behind a TLS-intercepting proxy, edge-tts needs its CA: TTS=tools/tts_ca.py (certifi pointed at the proxy bundle).
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
LIB=${LIB:-$(cd "$HERE/../.." && pwd)}
export LIB
[ -f "$LIB/core/render/video.mjs" ] || { echo "set LIB to the library folder"; exit 1; }
PY="$LIB/.venv/bin/python"; NAME=hot60; SIZE=1080x1920
cd "$HERE"
python3 tools/lists.py                                                     # data/*.json (DailyHotApi) → assets/lists.json
[ -s assets/map.json ] || python3 tools/map_prep.py raw/ne_10m_lakes.geojson raw/ne_10m_rivers_lake_centerlines.geojson assets/map.json
[ -s assets/fr/gl_138.jpg ] && [ -s assets/img/plateau.jpg ] || sh tools/prep.sh
for l in freepats vsco2ce vcsl; do [ -d "$LIB/core/audio/instruments/$l" ] || (cd "$LIB" && sh tools/fetch.sh instruments $l); done
[ -f audio/vo/L14.wav ] || $PY ${TTS:-} "$LIB/core/tts/tts_zh.py" audio/lines.json audio/vo --voice zh-CN-YunxiNeural --rate +12%
"$PY" "$LIB/core/tts/asr_check.py" audio/lines.json audio/vo --lang zh
python3 tools/cues.py                                                      # timeline.json → audio/cues.json (+ timing check)
cd "$LIB"
node core/render/readcheck.mjs "$HERE" --size $SIZE --step 0.05
node core/render/events.mjs "$HERE" --size $SIZE
node core/render/video.mjs "$HERE" --fps 30 --workers ${WORKERS:-4} --size $SIZE --out "$HERE/out/video.mp4"
"$PY" "$HERE/audio/mix.py"
"$PY" core/render/srt.py "$HERE/audio/cues.json" "$HERE/$NAME.srt"
sh core/render/mux.sh "$HERE/out/video.mp4" "$HERE/out/mix.wav" "$HERE/$NAME.mp4" 30 1
node core/render/still.mjs "$HERE" 32.6 --size $SIZE --prefix poster_ --out "$HERE/stills"
cp "$HERE/stills/poster_32.6.jpg" "$HERE/poster.jpg"
echo "done: $HERE/$NAME.mp4"
