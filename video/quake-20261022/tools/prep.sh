#!/bin/sh
# Material → display-size assets. Night globe: NASA Black Marble (13.0–17.6 s, centre crop 748×1080 → 1080×1560, 1.44×).
# Ground: NASA GIBS MODIS Terra true colour, 2026-10-22 (EPSG:4326): region 89.8–97.8°E 29.4–35.4°N, detail 92.8–94.8°E 31.4–33.4°N.
# Shaking: USGS ShakeMap us6000u43g intensity_overlay.png (91.5167°E 34.3167°N origin, 0.0106° × 0.009° cells).
set -e
cd "$(dirname "$0")/.."
mkdir -p assets/fr assets/img
ffmpeg -v error -y -ss 13.0 -t 4.6 -i raw/night.mp4 -vf "fps=30,crop=748:1080:586:0,scale=1080:1560:flags=lanczos,unsharp=5:5:0.45" -q:v 3 assets/fr/gl_%03d.jpg
ffmpeg -v error -y -i raw/himalaya.jpg -vf "crop=3600:5200:200:150,scale=1200:1733:flags=lanczos" -q:v 2 assets/img/plateau.jpg
cp raw/d22_MODIS_Terra_CorrectedReflectance_TrueColor.jpg assets/img/terra.jpg
cp raw/terra_detail.jpg assets/img/terra_d.jpg
cp raw/sm_intensity_overlay.png assets/img/shake.png
