# manim-reels

A template for making Instagram/TikTok reels that explain maths and physics with animation (in the style of @nitesh_n.a_frontend).
Finished videos:
- `topics/brachistochrone.py`: the brachistochrone (recreation of the original)
- `topics/monty_hall.py`: the Monty Hall problem, with background music and sound effects

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
./render.sh topics/brachistochrone.py Brachistochrone preview   # quick low-res draft, ~30 s
./render.sh topics/brachistochrone.py Brachistochrone           # final 1080×1350
MUSIC=bgm.mp3 ./render.sh topics/brachistochrone.py Brachistochrone  # add music (looped/trimmed with a fade-out)
```
The output goes to `out/<Scene>.mp4`.

## Audio (all synthesized in code, royalty-free)
- **Sound effects** `reelkit/audio.py`: pop, click, tick, whoosh, door (opening), goat (fail sound), chime (win), ding, rise (rising sweep)
  In a scene, call `self.sfx("door")` to play one at the current moment; `self.sfx("pop", delay=0.3, gain=-6)` adds a delay and volume change
- **Background music**: lo-fi, A minor, 84 BPM (Am9–Fmaj9–Cadd9–G6/9). `render.sh` generates it at exactly the video's length, with fade-in/out
- **Mix**: music sits under the effects, and the whole mix is loudness-normalized to -14 LUFS (the level Instagram/TikTok play at)
- To use your own music: `MUSIC=your_song.mp3 ./render.sh ...`; for no music: `MUSIC=none`
- To add new sounds: write a function in `audio.py` and register it in the `SFX` dictionary

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
