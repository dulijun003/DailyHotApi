# manim-reels

A template for making Instagram/TikTok reels that explain maths and physics with animation (in the style of @nitesh_n.a_frontend).
The first video recreates **Brachistochrone (the fastest-descent curve)**: `topics/brachistochrone.py`.

## Style
- Paper-white background, Inter font, LaTeX formulas, a muted palette (black / dark red / teal / gold beads)
- 4:5 portrait, 1080×1350, about 50 s
- No voice-over and no face on camera: the on-screen text tells the story, with background music added afterwards
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

## Layout
```
reelkit/
  style.py       palette, fonts, sizes (change these to restyle every video)
  components.py  title/subtitle, formula box, pill tag, bead, timer, legend, glow
  physics.py     beads sliding under gravity: exact time along any curve, cycloid fitting
  scene.py       ReelScene base class: BEATS run in order, PACE controls tempo, race() animates a race
topics/
  brachistochrone.py   the recreated video (12 beats)
  _template.py         blank template for a new topic
```

## Making a new video
1. `cp topics/_template.py topics/xxx.py` and rename the class
2. Write the storyboard in `BEATS`, one method per beat (3–6 s each)
3. Reuse `self.set_header(...)`, `C.formula_box(...)` and `self.race(...)`
4. Check with `preview` first; if it runs too long or too short, adjust `PACE`
   (the `[beat]` lines in the render log show where each beat starts and ends)

## Topic ideas
Tautochrone (equal-time descent) · Monty Hall · Fourier series drawing a picture · Galton board → normal distribution ·
Basel problem π²/6 · Buffon's needle for π · sorting algorithm races · random walks · the Bernoulli brothers' rivalry
