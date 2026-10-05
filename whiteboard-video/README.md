# Whiteboard video (SpaceX sample)

A hand-drawn whiteboard explainer: HTML/SVG animation captured frame by frame with headless Chromium, plus synthesised background music and sound effects.

```bash
npm install            # playwright-core
./fetch-fonts.sh       # Xiaolai + Klee One + Noto Sans SC -> ./fonts
node render.js events out/events.json        # pencil stroke timings (drive the SFX)
python3 audio.py out/events.json out/audio.wav 33.2
node render.js video out/video.mp4 30         # 1920x1080, ~2 min
ffmpeg -i out/video.mp4 -i out/audio.wav -c:v copy -c:a aac -b:a 192k -shortest out/final.mp4
node render.js stills out/stills 2.9 12.2    # single frames for checking
```

| File | Purpose |
| --- | --- |
| `engine.js` | Board: stroke draw-on, char-by-char handwriting, camera keyframes (pan/zoom/whip blur), pencil tracking |
| `shapes.js` | Hand-drawn icons: rocket, earth, orbit, explosion, stick figure, money bag, Mars, arrows |
| `scene-spacex.js` | The storyboard: subtitles, every element's position and timing, camera path |
| `index.html` | Stage: paper texture, pencil, subtitle bar, `renderAt(t)` |
| `render.js` | Playwright frame capture -> ffmpeg |
| `audio.py` | BGM (Fmaj7–G–Em7–Am7, 100 BPM) + pencil scratch, whoosh, thumps, chimes |

To make a new video, copy `scene-spacex.js`, rewrite `SUBS`, `buildScene()` and the camera keys.
