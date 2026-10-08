# manim-reels

A template for making Instagram/TikTok reels that explain maths and physics with animation (in the style of @nitesh_n.a_frontend).
Finished videos:
- `topics/brachistochrone.py`: the brachistochrone (recreation of the original)
- `topics/monty_hall.py`: the Monty Hall problem
  - `MontyHall`: English, background music + sound effects
  - `MontyHallZH`: **Chinese text + Chinese voiceover + subtitles** + background music + sound effects
  - Structure: hook (10,000 angry letters → "they were wrong") → main content → summary → end card (follow + next-episode teaser)

## Style
- Paper-white background, Inter font, LaTeX formulas, a muted palette (black / dark red / teal / gold beads)
- 4:5 portrait, 1080×1350, about 50 s
- No voice-over and no face on camera: the on-screen text tells the story, with background music and sound effects
- All numbers come from real physics (`reelkit/physics.py`): straight line 3.19 s, circular arc 2.63 s, cycloid 2.55 s, matching the original

## Setup
```bash
# System dependencies (Ubuntu/Debian)
sudo apt install ffmpeg libcairo2-dev libpango1.0-dev \
  texlive-latex-base texlive-latex-extra texlive-fonts-recommended dvisvgm cm-super
# Install the Inter font: https://rsms.me/inter/   (macOS: brew install --cask font-inter)

python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
On macOS, use `brew install ffmpeg pango` + MacTeX (or BasicTeX) instead of apt.

## Rendering
```bash
./render.sh topics/monty_hall.py MontyHallZH                   # Chinese voiceover version
./render.sh topics/brachistochrone.py Brachistochrone preview   # quick low-res draft, ~30 s
./render.sh topics/brachistochrone.py Brachistochrone           # final 1080×1350
MUSIC=bgm.mp3 ./render.sh topics/brachistochrone.py Brachistochrone  # add music (looped/trimmed with a fade-out)
```
The output goes to `out/<Scene>.mp4`.

## Audio (all synthesized in code, royalty-free)
- **Sound effects** `reelkit/audio.py`: pop, click, tick, whoosh, door (opening), goat (fail sound), chime (win), ding, rise (rising sweep)
  In a scene, call `self.sfx("door")` to play one at the current moment; `self.sfx("pop", delay=0.3, gain=-6)` adds a delay and volume change
- **Background music**: bright, curious explainer style, 100 BPM, royal road progression (Fmaj7–G6–Em7–Am7), Karplus-Strong plucked strings + glockenspiel + pad + light percussion
- **The music follows the video structure**: scenes call `self.music("intro" | "main" | "tension" | "outro")` to switch sections (switches land on bar lines),
  `self.music_hit()` to add a swell + accent at a key moment, and `self.music_end()` to land the final C major chord (use with `wait_for_downbeat()` so it falls on the beat)
- **Mix**: music sits under the effects, and the whole mix is loudness-normalized to -14 LUFS (the level Instagram/TikTok play at)
- To use your own music: `MUSIC=your_song.mp3 ./render.sh ...`; for no music: `MUSIC=none`
- To add new sounds: write a function in `audio.py` and register it in the `SFX` dictionary

## Chinese voiceover + subtitles
- Voice: edge-tts (Microsoft neural voices), default `zh-CN-YunxiNeural` (lively male voice). Female: `zh-CN-XiaoxiaoNeural`; news-anchor style: `zh-CN-YunyangNeural`
- Writing narration: put a `NARRATION = {"key": "text..."}` dictionary in the scene and use `with self.voice("key") as v:` to wrap the animations.
  Each block is **synthesized in one go** (natural intonation, no sentence-by-sentence breaks); the block lasts exactly as long as the voice, with only a short breath between blocks
- **Syncing visuals to specific words**: `v.until("山羊")` waits until the word "山羊" is spoken, then plays the next animation (edge-tts provides word-level timestamps)
- Inside a voice block, `self.wait()` is skipped automatically (the voice sets the pace); use `self.hold(s)` when you need a real pause
- Numbers are written in Chinese characters ("三分之二", "七十三号门") so they're read aloud correctly
- Each sentence is synthesized separately, with leading/trailing silence trimmed automatically, and cached in `reelkit/assets/tts/`; re-rendering only synthesizes lines that changed
- Subtitles are split by clause, matched to the voice timing, and output to `out/<Scene>.srt` (for uploading to platforms) and burned into the video
- Music gently ducks under the voice (sidechain compression, slow release, no pumping)
- A thin progress bar is drawn along the top edge (`PROGRESS=0` turns it off)
- Speech synthesis needs network access. If you hit certificate errors, set `SSL_CERT_FILE` to your CA bundle
- Note: whether edge-tts can be used commercially is a gray area. For a monetized account, consider switching to a commercially licensed TTS (e.g. Volcano Engine, iFlytek, Azure paid tier); only `reelkit/voice.py` needs to change

## Captions
`captions/<topic>.txt` holds the text for the post (story + source + hashtags), following the original's format.

## Layout
```
reelkit/
  style.py       palette, fonts, sizes (change these to restyle every video)
  components.py  title/subtitle, formula box, pill tag, bead, timer, legend, glow
  physics.py     beads sliding under gravity: exact time along any curve, cycloid fitting
  scene.py       ReelScene base class: BEATS run in order, PACE controls tempo, race() animates a race, sfx() plays a sound effect
  audio.py       procedural sound effects + background music (numpy synthesis)
  voice.py       voiceover (edge-tts), sentence splitting, silence trimming, caching
  subtitles.py   generates .srt / .ass subtitles from the voice timing
topics/
  brachistochrone.py   the recreated video (12 beats)
  monty_hall.py        the Monty Hall problem (10 beats: doors / probability transfer / case table / 1000-game simulation / 100 doors)
  _template.py         blank template for a new topic
```

## Making a new video
1. `cp topics/_template.py topics/xxx.py` and rename the class
2. Write the storyboard in `BEATS`, one method per beat (3–6 s each)
3. Reuse `self.set_header(...)`, `C.formula_box(...)` and `self.race(...)`
4. Check with `preview` first; if it runs too long or too short, adjust `PACE`
   (the `[beat]` lines in the render log show where each beat starts and ends)

## Topic ideas
Tautochrone (equal-time descent) · Fourier series drawing a picture · Galton board → normal distribution ·
Basel problem π²/6 · Buffon's needle for π · sorting algorithm races · random walks · the Bernoulli brothers' rivalry
