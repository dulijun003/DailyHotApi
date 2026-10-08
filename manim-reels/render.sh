#!/usr/bin/env bash
# Render a reel.
#
#   ./render.sh topics/brachistochrone.py Brachistochrone          # final 1080x1350
#   ./render.sh topics/brachistochrone.py Brachistochrone preview  # fast 432x540 draft
#   MUSIC=bgm.mp3 ./render.sh topics/...py Scene                   # add background music
#
# Output: out/<Scene>.mp4
set -euo pipefail
cd "$(dirname "$0")"

FILE=$1
SCENE=$2
MODE=${3:-final}
MANIM=${MANIM:-manim}

if [[ $MODE == preview ]]; then
  "$MANIM" -ql --resolution 432,540 "$FILE" "$SCENE"
  QDIR=540p15
else
  "$MANIM" -qh --resolution 1080,1350 --frame_rate 30 "$FILE" "$SCENE"
  QDIR=1350p30
fi

mkdir -p out
SRC="media/videos/$(basename "$FILE" .py)/$QDIR/$SCENE.mp4"
DST="out/$SCENE.mp4"

if [[ -n ${MUSIC:-} ]]; then
  # Loop/trim the music to the video length, fade it out over the last 2 s.
  DUR=$(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SRC")
  FADE_AT=$(python3 -c "print(max(0, $DUR - 2))")
  ffmpeg -y -v error -i "$SRC" -stream_loop -1 -i "$MUSIC" \
    -filter_complex "[1:a]volume=0.6,afade=t=out:st=$FADE_AT:d=2[a]" \
    -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 192k -shortest "$DST"
else
  cp "$SRC" "$DST"
fi
echo "✓ $DST"
