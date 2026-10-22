#!/bin/sh
# Footage → display-size frames for the vertical 1080×1560 band (≤ 1.5× for video), photos ≤ 1:1 of the source.
set -e
cd "$(dirname "$0")/.."
# Black Marble globe over Asia, source 13.0–17.6 s: centre crop 748×1080 (no NASA bug, no burned-in text) → 1080×1560 (1.44×)
ffmpeg -v error -y -ss 13.0 -t 4.6 -i raw/night.mp4 -vf "fps=30,crop=748:1080:586:0,scale=1080:1560:flags=lanczos,unsharp=5:5:0.45" -q:v 3 assets/fr/gl_%03d.jpg
# ISS photo of the Tibetan Plateau (iss072e397138): plateau side only, the station's arm cropped out
ffmpeg -v error -y -i raw/himalaya.jpg -vf "crop=3600:5200:200:150,scale=1200:1733:flags=lanczos" -q:v 2 assets/img/plateau.jpg
ls assets/fr | wc -l
