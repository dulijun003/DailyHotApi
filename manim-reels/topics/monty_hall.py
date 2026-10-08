"""The Monty Hall problem: why switching wins 2/3 of the time.

Render:  ./render.sh topics/monty_hall.py MontyHall
"""

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, PI,
    ArcBetweenPoints, Axes, BraceBetweenPoints, Circle, Create, DashedLine, Dot, Ellipse,
    FadeIn, FadeOut, GrowFromCenter, LaggedStart, Line, Polygon,
    RoundedRectangle, Transform, VGroup, VMobject, ValueTracker, always_redraw,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reelkit import components as C          # noqa: E402
from reelkit import style as S               # noqa: E402
from reelkit.scene import ReelScene          # noqa: E402

DOOR_FILL = S.SLATE
DOOR_EDGE = "#3E4F5E"
INSIDE = "#E9E3D8"
GOAT_C = "#8F8475"
DOORS_Y = 0.35


# ---- Icons -----------------------------------------------------------------

def car_icon(w=1.0, color=S.GOLD):
    s = w / 1.0
    body = RoundedRectangle(corner_radius=0.08 * s, width=1.0 * s, height=0.26 * s,
                            fill_color=color, fill_opacity=1, stroke_color="#8A6A22",
                            stroke_width=1.5)
    cabin = Polygon([-0.30 * s, 0.13 * s, 0], [-0.16 * s, 0.34 * s, 0],
                    [0.18 * s, 0.34 * s, 0], [0.32 * s, 0.13 * s, 0],
                    fill_color=color, fill_opacity=1, stroke_color="#8A6A22", stroke_width=1.5)
    window = Polygon([-0.23 * s, 0.15 * s, 0], [-0.13 * s, 0.29 * s, 0],
                     [0.15 * s, 0.29 * s, 0], [0.24 * s, 0.15 * s, 0],
                     fill_color=S.BG, fill_opacity=0.9, stroke_width=0)
    wheels = VGroup(*[
        VGroup(Circle(radius=0.11 * s, fill_color=S.INK, fill_opacity=1, stroke_width=0),
               Circle(radius=0.04 * s, fill_color=S.FAINT, fill_opacity=1, stroke_width=0)
               ).move_to([x * s, -0.13 * s, 0]) for x in (-0.28, 0.28)])
    return VGroup(cabin, window, body, wheels)


def goat_icon(w=0.6, color=GOAT_C):
    s = w / 0.6
    head = Ellipse(width=0.34 * s, height=0.46 * s, fill_color=color, fill_opacity=1,
                   stroke_width=0)
    snout = Ellipse(width=0.24 * s, height=0.16 * s, fill_color="#B3A895", fill_opacity=1,
                    stroke_width=0).shift(DOWN * 0.17 * s)
    horns = VGroup(*[
        ArcBetweenPoints([sx * 0.07 * s, 0.18 * s, 0], [sx * 0.24 * s, 0.36 * s, 0],
                         angle=-sx * PI / 2.2, stroke_color="#5C5348", stroke_width=5 * s)
        for sx in (-1, 1)])
    ears = VGroup(*[
        Ellipse(width=0.24 * s, height=0.09 * s, fill_color=color, fill_opacity=1,
                stroke_width=0).rotate(sx * -0.35).move_to([sx * 0.22 * s, 0.08 * s, 0])
        for sx in (-1, 1)])
    eyes = VGroup(*[Dot([sx * 0.075 * s, 0.03 * s, 0], radius=0.025 * s, color=S.INK)
                    for sx in (-1, 1)])
    beard = Polygon([-0.05 * s, -0.25 * s, 0], [0.05 * s, -0.25 * s, 0], [0, -0.38 * s, 0],
                    fill_color="#5C5348", fill_opacity=1, stroke_width=0)
    return VGroup(horns, ears, head, snout, eyes, beard)


class Door(VGroup):
    """A door with a prize behind it. `open()` returns the opening animation."""

    def __init__(self, number, prize, w=1.45, h=2.2, label_size=26):
        super().__init__()
        self.prize_kind = prize
        self.inside = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                                       fill_color=INSIDE, fill_opacity=1,
                                       stroke_color=DOOR_EDGE, stroke_width=2)
        icon = car_icon(w * 0.75) if prize == "car" else goat_icon(w * 0.42)
        self.prize = icon.move_to(self.inside).shift(DOWN * h * 0.08)
        self.panel = RoundedRectangle(corner_radius=0.06, width=w, height=h,
                                      fill_color=DOOR_FILL, fill_opacity=1,
                                      stroke_color=DOOR_EDGE, stroke_width=2)
        self.num = C.text(str(number), label_size, S.BG, weight="BOLD").move_to(self.panel)
        self.num.shift(UP * h * 0.12)
        self.knob = Dot(self.panel.get_right() + LEFT * w * 0.14, radius=0.045, color=S.GOLD)
        self.add(self.inside, self.prize, self.panel, self.num, self.knob)
        self.is_open = False

    def open(self):
        self.is_open = True
        hinge = self.panel.get_left()
        return VGroup(self.panel, self.num, self.knob).animate.stretch(
            0.07, dim=0, about_point=hinge).set_opacity(0.85)


def doors_row(prizes=("car", "goat", "goat"), y=DOORS_Y, gap=1.85):
    row = VGroup(*[Door(i + 1, p) for i, p in enumerate(prizes)])
    for i, d in enumerate(row):
        d.move_to([(i - 1) * gap, y, 0])
    return row


def frac(num, den, color=S.INK, scale=0.95):
    return C.math(rf"\tfrac{{{num}}}{{{den}}}", color, scale)


class MontyHall(ReelScene):
    PACE = 1.0
    BEATS = ["hook", "host_opens", "dilemma", "answer", "odds", "collapse", "cases",
             "simulate", "hundred", "outro"]

    # 1. Setup ---------------------------------------------------------------
    def hook(self):
        self.sfx("whoosh")
        self.set_header("Three doors. One car. Two goats.", "Pick a door.")
        # Car is behind door 2 in the story; you pick door 1.
        self.doors = doors_row(("goat", "car", "goat"))
        for i in range(3):
            self.sfx("pop", delay=0.18 * i * self.PACE)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in self.doors], lag_ratio=0.25),
                  run_time=1.2)
        self.wait(0.4)
        self.pick_door(0)
        self.wait(0.8)

    def pick_door(self, i):
        d = self.doors[i]
        self.pick_tag = C.pill(C.text("YOUR PICK", S.SMALL_SIZE, S.TEAL, weight="BOLD"),
                               S.TEAL, pad=0.1).next_to(d, UP, buff=0.18)
        self.sfx("click")
        self.play(d.panel.animate.set_stroke(S.TEAL, 6), FadeIn(self.pick_tag, shift=DOWN * 0.1),
                  run_time=0.5)

    # 2. Host opens a goat door -------------------------------------------------
    def host_opens(self):
        self.set_header("The host knows where the car is.", "He opens another door: a goat.")
        self.wait(0.5)
        self.sfx("door")
        self.play(self.doors[2].open(), run_time=0.8)
        self.sfx("goat", delay=0.0)
        self.play(self.doors[2].prize.animate.scale(1.12), run_time=0.25)
        self.play(self.doors[2].prize.animate.scale(1 / 1.12), run_time=0.25)
        self.wait(0.8)

    # 3. Stay or switch? ----------------------------------------------------------
    def dilemma(self):
        self.set_header("Stay with door 1, or switch to door 2?")
        stay = C.pill(C.text("STAY", S.LABEL_SIZE, S.INK, weight="BOLD"), S.INK, pad=0.16)
        switch = C.pill(C.text("SWITCH", S.LABEL_SIZE, S.TEAL, weight="BOLD"), S.TEAL, pad=0.16)
        self.choice = VGroup(stay, switch).arrange(RIGHT, buff=0.8).move_to(UP * -1.7)
        self.sfx("pop")
        self.sfx("pop", delay=0.25)
        self.play(LaggedStart(FadeIn(stay, shift=UP * 0.1), FadeIn(switch, shift=UP * 0.1),
                              lag_ratio=0.4), run_time=0.7)
        self.gut = VGroup(C.text("Most people think:", S.SMALL_SIZE + 1, S.MUTED),
                          C.text("two doors left, so it's 50 / 50", S.LABEL_SIZE + 2, S.INK,
                                 weight="BOLD")).arrange(DOWN, buff=0.12).move_to(UP * -2.85)
        self.play(FadeIn(self.gut, shift=UP * 0.1), run_time=0.6)
        self.wait(1.4)

    # 4. The counter-intuitive answer ------------------------------------------------
    def answer(self):
        strike = Line(self.gut[1].get_left() + LEFT * 0.1, self.gut[1].get_right() + RIGHT * 0.1,
                      color=S.RED, stroke_width=5)
        self.sfx("rise")
        self.play(Create(strike), self.gut.animate.set_opacity(0.45), run_time=0.5)
        self.set_header("Switching wins 2 out of 3 times.", "Staying wins only 1 in 3.",
                        title_color=S.TEAL, sub_color=S.INK, boxed=True)
        self.sfx("ding")
        self.play(self.choice[1].animate.scale(1.15).set_fill(S.TEAL, 0.12),
                  self.choice[0].animate.set_opacity(0.4), run_time=0.5)
        self.wait(1.6)
        self.play(FadeOut(strike), FadeOut(self.gut), FadeOut(self.choice), run_time=0.4)

    # 5. Odds at the moment you pick -------------------------------------------------
    def odds(self):
        self.set_header("Rewind: when you first pick…", "the car is equally likely to be anywhere.")
        # Close door 3 again, hide prizes from now on (we argue with odds only).
        d3 = self.doors[2]
        hinge = d3.panel.get_left()
        self.sfx("door", gain=-6)
        self.play(VGroup(d3.panel, d3.num, d3.knob).animate.stretch(
            1 / 0.07, dim=0, about_point=hinge).set_opacity(1), run_time=0.6)
        d3.is_open = False
        self.thirds = VGroup(*[frac(1, 3).next_to(d, DOWN, buff=0.25) for d in self.doors])
        for i in range(3):
            self.sfx("pop", delay=0.2 * i * self.PACE)
        self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in self.thirds], lag_ratio=0.3),
                  run_time=0.9)
        self.wait(0.6)

        left = self.doors[1].get_corner(DOWN + LEFT) + DOWN * 1.55
        right = self.doors[2].get_corner(DOWN + RIGHT) + DOWN * 1.55
        self.brace = BraceBetweenPoints(right, left, color=S.RED)   # opens downward
        self.brace_lab = VGroup(frac(2, 3, S.RED, 1.1),
                                C.text("car is behind one of these", S.SMALL_SIZE, S.RED)
                                ).arrange(DOWN, buff=0.08).next_to(self.brace, DOWN, buff=0.1)
        mine = C.text("your pick", S.SMALL_SIZE, S.TEAL, weight="BOLD")
        mine.move_to([self.doors[0].get_x(), self.brace_lab[1].get_y(), 0])
        self.mine = mine
        self.set_header("Your pick: 1 in 3.", "The other two doors together: 2 in 3.")
        self.sfx("whoosh")
        self.play(FadeIn(self.brace), FadeIn(self.brace_lab), FadeIn(mine),
                  self.thirds[0].animate.set_color(S.TEAL),
                  self.thirds[1:].animate.set_color(S.RED), run_time=0.7)
        self.wait(1.4)

    # 6. Host's knowledge concentrates the 2/3 ------------------------------------------
    def collapse(self):
        self.set_header("The host never opens the car.", "He removes a goat from YOUR 2/3 group.")
        self.sfx("door")
        self.play(self.doors[2].open(), self.thirds[2].animate.set_opacity(0.2), run_time=0.8)
        self.sfx("goat")
        self.wait(0.7)

        d2 = self.doors[1]
        new_brace = BraceBetweenPoints(d2.get_corner(DOWN + RIGHT) + DOWN * 1.55,
                                       d2.get_corner(DOWN + LEFT) + DOWN * 1.55, color=S.RED)
        new_lab = VGroup(frac(2, 3, S.RED, 1.25),
                         C.text("all on door 2", S.SMALL_SIZE, S.RED, weight="BOLD")
                         ).arrange(DOWN, buff=0.08).next_to(new_brace, DOWN, buff=0.1)
        self.set_header("So the whole 2/3 lands", "on the one door he left closed.")
        self.sfx("rise")
        self.play(Transform(self.brace, new_brace), Transform(self.brace_lab, new_lab),
                  FadeOut(self.thirds[1]), FadeOut(self.thirds[2]), run_time=1.0)
        self.sfx("ding")
        self.play(d2.panel.animate.set_stroke(S.RED, 6), run_time=0.3)
        self.wait(1.6)
        self.clear_stage()

    # 7. Enumerate every case ---------------------------------------------------------
    def cases(self):
        self.set_header("Check every case", "You pick door 1. The car could be anywhere.")
        cols = [-2.0, -0.55, 0.85, 2.15]
        heads = VGroup(*[C.text(t, S.SMALL_SIZE, S.MUTED, weight="BOLD").move_to([x, 1.75, 0])
                         for t, x in zip(["Car behind", "Host opens", "Stay", "Switch"], cols)])
        self.play(FadeIn(heads), run_time=0.4)

        def mini(car, opened):
            g = VGroup()
            for i in range(3):
                fill = S.GOLD if i == car else (INSIDE if i == opened else DOOR_FILL)
                r = RoundedRectangle(corner_radius=0.03, width=0.32, height=0.44,
                                     fill_color=fill, fill_opacity=1,
                                     stroke_color=S.TEAL if i == 0 else DOOR_EDGE,
                                     stroke_width=3 if i == 0 else 1.2)
                g.add(r)
            return g.arrange(RIGHT, buff=0.07)

        def verdict(win):
            return C.text("WIN" if win else "lose", S.LABEL_SIZE,
                          S.TEAL if win else S.MUTED, weight="BOLD" if win else "NORMAL")

        rows = VGroup()
        for k, (car, opened) in enumerate([(0, 1), (1, 2), (2, 1)]):
            y = 1.0 - k * 0.95
            stay_win = car == 0
            row = VGroup(mini(car, -1).move_to([cols[0], y, 0]),
                         C.text(f"door {opened + 1}", S.LABEL_SIZE, S.INK).move_to([cols[1], y, 0]),
                         verdict(stay_win).move_to([cols[2], y, 0]),
                         verdict(not stay_win).move_to([cols[3], y, 0]))
            rows.add(row)
        sep = Line(LEFT * 2.9, RIGHT * 2.9, color=S.FAINT, stroke_width=1.5).set_y(-1.55)

        for k, row in enumerate(rows):
            self.sfx("tick")
            self.play(FadeIn(row[:2], shift=RIGHT * 0.1), run_time=0.35)
            self.sfx("pop", gain=-6)
            self.play(FadeIn(row[2:], shift=UP * 0.05), run_time=0.35)
            self.wait(0.35)

        totals = VGroup(C.text("Total", S.LABEL_SIZE, S.INK, weight="BOLD").move_to([cols[0], -2.05, 0]),
                        frac(1, 3, S.MUTED, 1.1).move_to([cols[2], -2.05, 0]),
                        frac(2, 3, S.TEAL, 1.25).move_to([cols[3], -2.05, 0]))
        self.play(Create(sep), FadeIn(totals), run_time=0.5)
        hl = C.pill(VGroup(*[r[3] for r in rows], totals[2]).copy(), S.TEAL, pad=0.15,
                    fill_opacity=0.08)[0]
        self.sfx("chime", gain=-4)
        self.play(FadeIn(hl), run_time=0.4)
        self.wait(1.4)
        self.clear_stage()

    # 8. Monte-Carlo simulation -----------------------------------------------------------
    def simulate(self):
        n_games = 1000
        rng = np.random.default_rng(2024)
        car = rng.integers(0, 3, n_games)
        pick = rng.integers(0, 3, n_games)
        stay = np.cumsum(car == pick) / np.arange(1, n_games + 1)
        switch = np.cumsum(car != pick) / np.arange(1, n_games + 1)

        self.set_header("Still doubtful? Play 1,000 games.", "Running win rate of each strategy")
        ax = Axes(x_range=[0, n_games, 250], y_range=[0, 1, 0.25], x_length=5.0, y_length=3.0,
                  axis_config={"color": S.FAINT, "stroke_width": 1.5, "include_ticks": False},
                  tips=False).move_to(UP * 0.0 + RIGHT * 0.15)
        guides = VGroup()
        for v, col in ((1 / 3, S.MUTED), (2 / 3, S.TEAL)):
            guides.add(DashedLine(ax.c2p(0, v), ax.c2p(n_games, v), color=col, stroke_width=1.2,
                                  dash_length=0.06, stroke_opacity=0.6))
        ylabs = VGroup(*[C.text(t, S.SMALL_SIZE - 2, S.MUTED).next_to(ax.c2p(0, v), LEFT, buff=0.1)
                         for t, v in (("0%", 0), ("33%", 1 / 3), ("67%", 2 / 3), ("100%", 1))])
        xlab = C.text("games played", S.SMALL_SIZE - 1, S.MUTED).next_to(ax, DOWN, buff=0.12)
        self.play(Create(ax), FadeIn(guides), FadeIn(ylabs), FadeIn(xlab), run_time=0.6)

        n = ValueTracker(1)

        def curve(data, color):
            def build():
                k = max(2, int(n.get_value()))
                xs = np.arange(1, k + 1)
                # Sub-sample so the path stays light.
                idx = np.unique(np.linspace(0, k - 1, min(k, 300)).astype(int))
                m = VMobject(stroke_color=color, stroke_width=3.5)
                m.set_points_as_corners([ax.c2p(xs[i], data[i]) for i in idx])
                return m
            return always_redraw(build)

        c_stay, c_switch = curve(stay, S.INK), curve(switch, S.TEAL)

        def readout(label, data, color):
            def build():
                k = max(1, int(n.get_value()))
                return C.text(f"{label}  {data[k - 1] * 100:4.1f}%", S.LABEL_SIZE + 2, color,
                              weight="BOLD", font=S.MONO)
            return build

        r_stay = always_redraw(lambda: readout("STAY  ", stay, S.INK)().move_to([-1.35, -2.35, 0]))
        r_sw = always_redraw(lambda: readout("SWITCH", switch, S.TEAL)().move_to([1.45, -2.35, 0]))
        count = always_redraw(lambda: C.text(f"game {int(n.get_value()):,}", S.SMALL_SIZE,
                                             S.MUTED, font=S.MONO).move_to([0, -2.9, 0]))
        self.add(c_stay, c_switch, r_stay, r_sw, count)

        # Ticks speed up with the counter (exponential pacing of games).
        dur = 4.5
        for k in range(28):
            self.sfx("tick", delay=dur * (k / 28) ** 1.6, gain=-8)
        self.play(n.animate.set_value(n_games), run_time=dur, paced=False,
                  rate_func=lambda a: a ** 2.2)
        for m in (c_stay, c_switch, r_stay, r_sw, count):
            m.clear_updaters()
        self.sfx("chime", gain=-4)
        self.play(r_sw.animate.scale(1.12), run_time=0.3)
        self.wait(1.4)
        self.clear_stage()

    # 9. 100 doors ------------------------------------------------------------------------
    def hundred(self):
        self.set_header("Still not convinced? Try 100 doors.", "You pick door 1.")
        cells = VGroup()
        for i in range(100):
            r = RoundedRectangle(corner_radius=0.03, width=0.36, height=0.40,
                                 fill_color=DOOR_FILL, fill_opacity=1, stroke_color=DOOR_EDGE,
                                 stroke_width=1)
            r.add(C.text(str(i + 1), 9, S.BG).move_to(r))
            cells.add(r)
        cells.arrange_in_grid(10, 10, buff=(0.1, 0.08)).move_to(DOWN * 0.15)
        self.sfx("whoosh")
        self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.01),
                  run_time=1.0)
        self.sfx("click")
        self.play(cells[0][0].animate.set_stroke(S.TEAL, 5), run_time=0.3)
        self.wait(0.4)

        keep = 72   # door 73 stays closed
        others = [c for i, c in enumerate(cells) if i not in (0, keep)]
        self.set_header("The host opens 98 goat doors.", "Every door except one.")
        for k in range(6):
            self.sfx("door", delay=k * 0.3 * self.PACE, gain=-10)
        self.play(LaggedStart(*[c.animate.set_fill(INSIDE).set_stroke(S.FAINT)
                                for c in others], lag_ratio=0.015),
                  *[c[1].animate.set_opacity(0) for c in others], run_time=2.0)
        self.sfx("rise")
        self.play(cells[keep][0].animate.set_stroke(S.RED, 5), cells[keep].animate.scale(1.25),
                  cells[0].animate.scale(1.25), run_time=0.5)
        q = VGroup(C.text("Stay with your 1-in-100 guess,", S.LABEL_SIZE, S.INK),
                   C.text("or take the door he carefully avoided?", S.LABEL_SIZE, S.RED,
                          weight="BOLD")).arrange(DOWN, buff=0.08).move_to(UP * -3.2)
        self.play(FadeIn(q, shift=UP * 0.1), run_time=0.5)
        self.wait(2.0)
        self.clear_stage()

    # 10. Outro -----------------------------------------------------------------------------
    def outro(self):
        self.set_header("THE MONTY HALL PROBLEM", "Let's Make a Deal, 1963 · Marilyn vos Savant, 1990")
        doors = doors_row(("goat", "car", "goat"), y=0.55)
        doors[0].panel.set_stroke(S.TEAL, 5)
        self.add(doors)
        self.play(FadeIn(doors), run_time=0.4)
        self.sfx("door")
        self.play(doors[2].open(), run_time=0.5)
        self.sfx("door", delay=0.15)
        self.play(doors[1].open(), run_time=0.5)
        self.sfx("chime")
        self.play(doors[1].prize.animate.scale(1.15), run_time=0.3)
        res = VGroup(
            VGroup(C.text("stay", S.LABEL_SIZE, S.MUTED), frac(1, 3, S.MUTED, 1.1)
                   ).arrange(RIGHT, buff=0.15),
            C.text("vs", S.SMALL_SIZE, S.MUTED),
            VGroup(C.text("switch", S.LABEL_SIZE, S.TEAL, weight="BOLD"),
                   frac(2, 3, S.TEAL, 1.25)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.35)
        box = C.pill(res.scale(1.35), S.INK, pad=0.22).move_to(UP * -1.75)
        tag = VGroup(C.text("Always switch.", S.LABEL_SIZE + 2, S.INK, weight="BOLD",
                            slant="ITALIC"),
                     C.text("New information changes the odds, even when it feels like it can't.",
                            S.SMALL_SIZE - 2, S.TEAL, slant="ITALIC")).arrange(DOWN, buff=0.1)
        tag.next_to(box, DOWN, buff=0.35)
        self.play(FadeIn(box), run_time=0.4)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.5)
        self.wait(2.4)
