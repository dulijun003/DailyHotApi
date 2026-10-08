"""Copy this file to start a new reel:  cp topics/_template.py topics/my_topic.py

Structure that works for this format (~50 s, no voice-over, music only):
  1. hook      - a question + a visual race/comparison        (~5 s)
  2. result    - the counter-intuitive answer                  (~3 s)
  3-6. why     - 3-4 beats, one idea + one formula each        (~4-6 s each)
  7. reveal    - name the answer, show its formula             (~5 s)
  8. payoff    - replay the race / show the key trade-off      (~5 s)
  9. outro     - title card + one-line takeaway                (~3 s)

Preview:  ./render.sh topics/my_topic.py MyTopic preview
Final:    ./render.sh topics/my_topic.py MyTopic
"""

import sys
from pathlib import Path

from manim import DOWN, Circle, Create, Write

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reelkit import components as C   # noqa: E402
from reelkit import style as S        # noqa: E402
from reelkit.scene import ReelScene   # noqa: E402


class MyTopic(ReelScene):
    PACE = 0.7     # lower = snappier
    BEATS = ["hook", "explain", "outro"]

    def hook(self):
        self.set_header("A question that sounds easy?", "…but the answer surprises you")
        shape = Circle(radius=1.2, color=S.TEAL)
        self.play(Create(shape))
        self.wait(1)

    def explain(self):
        self.set_header("Here is why", title_color=S.TEAL)
        eq = C.formula_box(r"e^{i\pi} + 1 = 0", S.INK, S.TEAL).shift(DOWN * 2.3)
        self.play(Write(eq))
        self.wait(1.5)
        self.clear_stage()

    def outro(self):
        self.set_header("THE TAKEAWAY", "one line people will remember")
        self.wait(2)
