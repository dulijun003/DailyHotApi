# 热榜60秒 · 10.22 — a vertical Caption News film from DailyHotApi data

`hot60.mp4` (1080×1920, 30 fps, 61 s, −14 LUFS) · `hot60.srt` · `poster.jpg`.
Made with the Lemo-Opuscar "Caption News · 字幕新闻" style from this repo's own API output
(`data/`, a snapshot of 7 lists at 2026-10-23 00:47 Beijing time).

- `FACTS.md`: every claim in the film, with the list entry it comes from.
- `TREATMENT.md`: structure, shots, cue map, sound design.
- `CREDITS`, `SOURCES.md`: third-party material and licences (NASA public domain, Natural Earth, OFL fonts, CC0/CC BY samples).
- Source: `index.html` + `main.js` (the page, `render(t)`), `timeline.json` (one timeline for picture, subtitles and mix),
  `audio/mix.py`, `tools/`, `build.sh`.

To rebuild: clone github.com/lemomo-ai/lemo-opuscar, run `sh plugin/skills/lemo-opuscar/scripts/setup.sh deps voice music`,
copy this folder to `films/hot60/` in that clone, add `fonts/NotoSansSC.ttf` and `fonts/InterTight.ttf` (google/fonts, OFL),
fetch `raw/` (NASA + Natural Earth, see SOURCES.md), then `sh build.sh`.
