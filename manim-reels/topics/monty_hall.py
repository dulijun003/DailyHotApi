"""The Monty Hall problem: why switching wins 2/3 of the time.

Render:  ./render.sh topics/monty_hall.py MontyHall      # English, music + sfx
         ./render.sh topics/monty_hall.py MontyHallZH    # 中文 + 配音 + 字幕
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


# ---- On-screen text, per language ------------------------------------------

TEXT = {
    "en": dict(
        series="COUNTERINTUITIVE MATH · 01", handle="@counterintuitive.math", avatar="C",
        cold_t="Stay or switch?", letters="angry letters", phds="nearly 1,000 from PhDs",
        stamp="THEY WERE WRONG",
        hook_t="Three doors. One car. Two goats.", hook_s="Pick a door.",
        pick="YOUR PICK",
        host_t="The host knows where the car is.", host_s="He opens another door: a goat.",
        dilemma_t="Stay with door 1, or switch to door 2?",
        stay="STAY", switch="SWITCH",
        gut1="Most people think:", gut2="two doors left, so it's 50 / 50",
        answer_t="Switching wins 2 out of 3 times.", answer_s="Staying wins only 1 in 3.",
        odds_t="Rewind: when you first pick…",
        odds_s="the car is equally likely to be anywhere.",
        odds2_t="Your pick: 1 in 3.", odds2_s="The other two doors together: 2 in 3.",
        behind="car is behind one of these", your_pick="your pick",
        collapse_t="The host never opens the car.",
        collapse_s="He removes a goat from YOUR 2/3 group.",
        collapse2_t="So the whole 2/3 lands", collapse2_s="on the one door he left closed.",
        all_on="all on door 2",
        cases_t="Check every case", cases_s="You pick door 1. The car could be anywhere.",
        cols=["Car behind", "Host opens", "Stay", "Switch"],
        door_n="door {n}", win="WIN", lose="lose", total="Total",
        sim_t="Still doubtful? Play 1,000 games.", sim_s="Running win rate of each strategy",
        games_played="games played", sim_stay="STAY", sim_switch="SWITCH",
        game_n="game {n:,}",
        h_t="Still not convinced? Try 100 doors.", h_s="You pick door 1.",
        h2_t="The host opens 98 goat doors.", h2_s="Every door except one.",
        hq1="Stay with your 1-in-100 guess,", hq2="or take the door he carefully avoided?",
        out_t="THE MONTY HALL PROBLEM",
        out_s="Let's Make a Deal, 1963 · Marilyn vos Savant, 1990",
        out_stay="stay", out_switch="switch", vs="vs",
        tag1="Always switch.",
        tag2="New information changes the odds, even when it feels like it can't.",
        follow="+ Follow", followed="Following", next_lbl="NEXT EPISODE",
        next_t="23 people in a room:", next_s="two share a birthday more than 50% of the time",
    ),
    "zh": dict(
        series="反直觉数学 · 01", handle="@反直觉数学", avatar="反",
        cold_t="换，还是不换？", letters="封抗议信", phds="其中近 1000 位博士",
        stamp="错的是他们",
        hook_t="三扇门，一辆车，两只羊", hook_s="先选一扇门",
        pick="你的选择",
        host_t="主持人知道车在哪", host_s="他打开另一扇门：一只羊",
        dilemma_t="坚持 1 号门，还是换 2 号门？",
        stay="坚持", switch="换门",
        gut1="大多数人觉得：", gut2="只剩两扇门，一半一半",
        answer_t="换门的胜率是 2/3", answer_s="坚持只有 1/3",
        odds_t="倒回去：你刚选的时候", odds_s="车在每扇门后的概率一样",
        odds2_t="你选中的概率：1/3", odds2_s="另外两扇门加起来：2/3",
        behind="车在这两扇之一", your_pick="你的选择",
        collapse_t="主持人永远不会开出汽车", collapse_s="他只是从 2/3 那组里排除了一只羊",
        collapse2_t="于是整个 2/3", collapse2_s="都落到了他没开的那扇门上",
        all_on="全在 2 号门",
        cases_t="把所有情况列出来", cases_s="你选 1 号门，车可能在任何一扇后面",
        cols=["车在", "主持人开", "坚持", "换门"],
        door_n="{n} 号门", win="赢", lose="输", total="合计",
        sim_t="还不信？实打实玩 1000 局", sim_s="两种策略的累计胜率",
        games_played="已玩局数", sim_stay="坚持", sim_switch="换门",
        game_n="第 {n} 局",
        h_t="还是别扭？试试 100 扇门", h_s="你选了 1 号门",
        h2_t="主持人打开了 98 扇羊门", h2_s="只留下一扇",
        hq1="坚持你那 1% 的猜测，", hq2="还是换成他刻意避开的那扇？",
        out_t="蒙提霍尔问题", out_s="源自 1963 年美国电视节目《Let's Make a Deal》",
        out_stay="坚持", out_switch="换门", vs="vs",
        tag1="永远选择换门。", tag2="新信息会改变概率，哪怕直觉告诉你不会。",
        follow="+ 关注", followed="已关注", next_lbl="下期预告",
        next_t="23 个人里", next_s="两人同一天生日的概率超过 50%",
    ),
}

# Spoken narration (Chinese). One block = one natural breath group; cues in the
# code (v.until("...")) land animations on words. Numbers are written in
# Chinese characters so the voice reads them naturally.
NARRATION_ZH = {
    "intro.1": "一道数学题，让上万名读者写信痛骂一位专栏作家，其中近千人是博士。",
    "intro.2": "可最后证明，错的是他们。",
    "hook.1": "规则很简单：三扇门，一扇后面是汽车，另外两扇是山羊。你先选一扇，比如一号门。",
    "host.1": "知道答案的主持人，打开了另一扇门：三号门，是只山羊。",
    "dilemma.1": "现在他问你：坚持一号门，还是换成二号门？",
    "dilemma.2": "大多数人会说：只剩两扇，一半一半，换不换都一样。",
    "answer.1": "错！换门赢的概率是三分之二，坚持只有三分之一。为什么？",
    "odds.1": "倒回你刚选的那一刻：车在每扇门后的概率，都是三分之一。",
    "odds.2": "你选中的是三分之一，另外两扇加起来，是三分之二。",
    "collapse.1": "关键在于：主持人知道车在哪，他永远不会开出汽车。",
    "collapse.2": "所以他开掉三号门，这三分之二并没有消失，而是全部压到了二号门上。",
    "cases.1": "把所有情况列出来：车在一号门，坚持赢；车在二号门，换门赢；车在三号门，"
                "还是换门赢。三种情况，换门赢两种。",
    "sim.1": "还不信？让电脑实打实玩一千局。坚持的胜率停在百分之三十三，换门，停在百分之六十七。",
    "hundred.1": "还觉得别扭？想象一百扇门。你选一号，主持人打开剩下的九十八扇，全是山羊，"
                  "只留下七十三号。",
    "hundred.2": "你还守着你那百分之一吗？",
    "outro.1": "这就是著名的蒙提霍尔问题。记住：永远要换门，新的信息，会改变概率。",
    "endcard.1": "关注我，下期聊：为什么二十三个人里，大概率有两人同一天生日？",
}


def envelope(w=0.42):
    h = w * 0.66
    body = RoundedRectangle(corner_radius=0.03, width=w, height=h, fill_color=S.BG,
                            fill_opacity=1, stroke_color=S.MUTED, stroke_width=1.5)
    flap = VMobject(stroke_color=S.MUTED, stroke_width=1.5).set_points_as_corners(
        [body.get_corner(UP + LEFT), body.get_center() + DOWN * h * 0.1,
         body.get_corner(UP + RIGHT)])
    return VGroup(body, flap)


class MontyHall(ReelScene):
    LANG = "en"
    PACE = 1.0
    BEATS = ["cold_open", "hook", "host_opens", "dilemma", "answer", "odds", "collapse",
             "cases", "simulate", "hundred", "outro", "endcard"]

    def setup(self):
        super().setup()
        self.T = TEXT[self.LANG]

    # 0. Cold open: the hook before the rules ------------------------------------
    def cold_open(self):
        T = self.T
        self.music("intro")
        badge = C.pill(C.text(T["series"], S.SMALL_SIZE, S.TEAL, weight="BOLD"), S.TEAL,
                       pad=0.12).move_to(UP * 3.35)
        big = C.text(T["cold_t"], 54, S.INK, weight="BOLD").move_to(UP * 2.3)
        rng = np.random.default_rng(3)
        envs = VGroup(*[
            envelope().rotate(rng.uniform(-0.5, 0.5)).move_to(
                [rng.uniform(-2.7, 2.7), rng.uniform(-2.9, 1.2), 0])
            for _ in range(36)])
        count = ValueTracker(0)
        num = always_redraw(lambda: C.text(f"{int(count.get_value()):,}", 64, S.RED,
                                           weight="BOLD", font="Inter").move_to(UP * 0.1))
        letters = C.text(T["letters"], S.LABEL_SIZE + 2, S.INK, weight="BOLD")
        letters.next_to(num, DOWN, buff=0.2)
        phds = C.text(T["phds"], S.LABEL_SIZE, S.MUTED).next_to(letters, DOWN, buff=0.18)
        backing = RoundedRectangle(corner_radius=0.2, width=4.2, height=2.4, stroke_width=0,
                                   fill_color=S.BG, fill_opacity=0.92).move_to(DOWN * 0.45)

        with self.voice("intro.1") as v:
            self.sfx("whoosh")
            self.play(FadeIn(big, scale=1.25), FadeIn(badge), run_time=0.5)
            self.wait(0.6)
            v.until("上万名")
            for k in range(8):
                self.sfx("pop", delay=k * 0.17, gain=-8)
            self.add(backing, num)
            self.play(LaggedStart(*[FadeIn(e, shift=DOWN * 0.3, scale=0.7) for e in envs],
                                  lag_ratio=0.04),
                      count.animate.set_value(10000), FadeIn(letters), run_time=1.6)
            self.bring_to_front(backing, num, letters)
            self.wait(0.6)
            v.until("近千人")
            self.play(FadeIn(phds, shift=UP * 0.1), run_time=0.4)
            self.wait(0.8)
        num.clear_updaters()

        stamp = VGroup(
            RoundedRectangle(corner_radius=0.08, width=3.6, height=0.95, stroke_color=S.RED,
                             stroke_width=6, fill_color=S.BG, fill_opacity=0.9),
            C.text(T["stamp"], 36, S.RED, weight="BOLD"),
        ).rotate(-0.18).move_to(DOWN * 0.5)
        with self.voice("intro.2") as v:
            v.until("错的", lead=0.15)
            self.music_hit(delay=0.15)
            self.sfx("rise", gain=-4)
            stamp.scale(1.8).set_opacity(0)
            self.play(stamp.animate.scale(1 / 1.8).set_opacity(1), run_time=0.3)
            self.sfx("door", gain=-4)
            self.wait(1.2)

    # 1. Setup ---------------------------------------------------------------
    def hook(self):
        T = self.T
        self.music("main")
        with self.voice("hook.1") as v:
            self.clear_stage(run_time=0.4)
            self.set_header(T["hook_t"], T["hook_s"])
            # Car is behind door 2 in the story; you pick door 1.
            self.doors = doors_row(("goat", "car", "goat"))
            v.until("三扇门")
            for i in range(3):
                self.sfx("pop", delay=0.18 * i * self.PACE)
            self.play(LaggedStart(*[GrowFromCenter(d) for d in self.doors], lag_ratio=0.25),
                      run_time=1.2)
            self.wait(0.4)
            v.until("一号门")
            self.pick_door(0)
            self.wait(0.8)

    def pick_door(self, i):
        d = self.doors[i]
        self.pick_tag = C.pill(C.text(self.T["pick"], S.SMALL_SIZE, S.TEAL, weight="BOLD"),
                               S.TEAL, pad=0.1).next_to(d, UP, buff=0.18)
        self.sfx("click")
        self.play(d.panel.animate.set_stroke(S.TEAL, 6), FadeIn(self.pick_tag, shift=DOWN * 0.1),
                  run_time=0.5)

    # 2. Host opens a goat door -------------------------------------------------
    def host_opens(self):
        with self.voice("host.1") as v:
            self.set_header(self.T["host_t"], self.T["host_s"])
            self.wait(0.5)
            v.until("打开", lead=0.2)
            self.sfx("door")
            self.play(self.doors[2].open(), run_time=0.8)
            v.until("山羊", lead=0.1)
            self.sfx("goat")
            self.play(self.doors[2].prize.animate.scale(1.12), run_time=0.25)
            self.play(self.doors[2].prize.animate.scale(1 / 1.12), run_time=0.25)
            self.wait(0.8)

    # 3. Stay or switch? ----------------------------------------------------------
    def dilemma(self):
        T = self.T
        self.music("tension")
        with self.voice("dilemma.1") as v:
            self.set_header(T["dilemma_t"])
            stay = C.pill(C.text(T["stay"], S.LABEL_SIZE, S.INK, weight="BOLD"), S.INK, pad=0.16)
            switch = C.pill(C.text(T["switch"], S.LABEL_SIZE, S.TEAL, weight="BOLD"), S.TEAL,
                            pad=0.16)
            self.choice = VGroup(stay, switch).arrange(RIGHT, buff=0.8).move_to(UP * -1.7)
            v.until("坚持")
            self.sfx("pop")
            self.play(FadeIn(stay, shift=UP * 0.1), run_time=0.35)
            v.until("换成")
            self.sfx("pop")
            self.play(FadeIn(switch, shift=UP * 0.1), run_time=0.35)
        with self.voice("dilemma.2") as v:
            self.gut = VGroup(C.text(T["gut1"], S.SMALL_SIZE + 1, S.MUTED),
                              C.text(T["gut2"], S.LABEL_SIZE + 2, S.INK, weight="BOLD")
                              ).arrange(DOWN, buff=0.12).move_to(UP * -2.75)
            self.play(FadeIn(self.gut[0], shift=UP * 0.1), run_time=0.4)
            v.until("一半")
            self.play(FadeIn(self.gut[1], shift=UP * 0.1), run_time=0.5)
            self.wait(1.4)

    # 4. The counter-intuitive answer ------------------------------------------------
    def answer(self):
        with self.voice("answer.1") as v:
            strike = Line(self.gut[1].get_left() + LEFT * 0.1,
                          self.gut[1].get_right() + RIGHT * 0.1, color=S.RED, stroke_width=5)
            self.music_hit()
            self.music("main")
            self.sfx("rise")
            self.play(Create(strike), self.gut.animate.set_opacity(0.45), run_time=0.4)
            v.until("换门")
            self.set_header(self.T["answer_t"], self.T["answer_s"],
                            title_color=S.TEAL, sub_color=S.INK, boxed=True)
            self.sfx("ding")
            self.play(self.choice[1].animate.scale(1.15).set_fill(S.TEAL, 0.12),
                      self.choice[0].animate.set_opacity(0.4), run_time=0.5)
            self.wait(1.6)
            v.until("为什么")
            self.play(FadeOut(strike), FadeOut(self.gut), FadeOut(self.choice), run_time=0.4)

    # 5. Odds at the moment you pick -------------------------------------------------
    def odds(self):
        T = self.T
        with self.voice("odds.1") as v:
            self.set_header(T["odds_t"], T["odds_s"])
            # Close door 3 again; from here on we argue with odds only.
            d3 = self.doors[2]
            hinge = d3.panel.get_left()
            self.sfx("door", gain=-6)
            self.play(VGroup(d3.panel, d3.num, d3.knob).animate.stretch(
                1 / 0.07, dim=0, about_point=hinge).set_opacity(1), run_time=0.6)
            d3.is_open = False
            self.thirds = VGroup(*[frac(1, 3).next_to(d, DOWN, buff=0.25) for d in self.doors])
            v.until("三分之一", lead=0.3)
            for i in range(3):
                self.sfx("pop", delay=0.2 * i * self.PACE)
            self.play(LaggedStart(*[FadeIn(f, shift=UP * 0.1) for f in self.thirds],
                                  lag_ratio=0.3), run_time=0.9)
            self.wait(0.6)

        with self.voice("odds.2") as v:
            left = self.doors[1].get_corner(DOWN + LEFT) + DOWN * 1.55
            right = self.doors[2].get_corner(DOWN + RIGHT) + DOWN * 1.55
            self.brace = BraceBetweenPoints(right, left, color=S.RED)
            self.brace_lab = VGroup(frac(2, 3, S.RED, 1.1),
                                    C.text(T["behind"], S.SMALL_SIZE, S.RED)
                                    ).arrange(DOWN, buff=0.08).next_to(self.brace, DOWN, buff=0.1)
            mine = C.text(T["your_pick"], S.SMALL_SIZE, S.TEAL, weight="BOLD")
            mine.move_to([self.doors[0].get_x(), self.brace_lab[1].get_y(), 0])
            self.set_header(T["odds2_t"], T["odds2_s"])
            self.play(FadeIn(mine), self.thirds[0].animate.set_color(S.TEAL), run_time=0.4)
            v.until("另外两扇")
            self.sfx("whoosh")
            self.play(FadeIn(self.brace), FadeIn(self.brace_lab),
                      self.thirds[1:].animate.set_color(S.RED), run_time=0.7)
            self.wait(1.4)

    # 6. Host's knowledge concentrates the 2/3 ------------------------------------------
    def collapse(self):
        T = self.T
        with self.voice("collapse.1") as v:
            self.set_header(T["collapse_t"], T["collapse_s"])
            v.until("永远不会", lead=0.2)
            self.sfx("door")
            self.play(self.doors[2].open(), self.thirds[2].animate.set_opacity(0.2), run_time=0.8)
            self.sfx("goat")
            self.wait(0.7)

        with self.voice("collapse.2") as v:
            d2 = self.doors[1]
            new_brace = BraceBetweenPoints(d2.get_corner(DOWN + RIGHT) + DOWN * 1.55,
                                           d2.get_corner(DOWN + LEFT) + DOWN * 1.55, color=S.RED)
            new_lab = VGroup(frac(2, 3, S.RED, 1.25),
                             C.text(T["all_on"], S.SMALL_SIZE, S.RED, weight="BOLD")
                             ).arrange(DOWN, buff=0.08).next_to(new_brace, DOWN, buff=0.1)
            self.set_header(T["collapse2_t"], T["collapse2_s"])
            v.until("全部压到", lead=0.2)
            self.sfx("rise")
            self.play(Transform(self.brace, new_brace), Transform(self.brace_lab, new_lab),
                      FadeOut(self.thirds[1]), FadeOut(self.thirds[2]), run_time=0.9)
            v.until("二号门")
            self.sfx("ding")
            self.play(d2.panel.animate.set_stroke(S.RED, 6), run_time=0.3)
            self.wait(1.6)

    # 7. Enumerate every case ---------------------------------------------------------
    def cases(self):
        T = self.T
        cols = [-2.0, -0.55, 0.85, 2.15]

        def mini(car):
            g = VGroup()
            for i in range(3):
                r = RoundedRectangle(corner_radius=0.03, width=0.32, height=0.44,
                                     fill_color=S.GOLD if i == car else DOOR_FILL, fill_opacity=1,
                                     stroke_color=S.TEAL if i == 0 else DOOR_EDGE,
                                     stroke_width=3 if i == 0 else 1.2)
                g.add(r)
            return g.arrange(RIGHT, buff=0.07)

        def verdict(win):
            return C.text(T["win"] if win else T["lose"], S.LABEL_SIZE,
                          S.TEAL if win else S.MUTED, weight="BOLD" if win else "NORMAL")

        rows = VGroup()
        for k, (car, opened) in enumerate([(0, 1), (1, 2), (2, 1)]):
            y = 1.0 - k * 0.95
            stay_win = car == 0
            rows.add(VGroup(
                mini(car).move_to([cols[0], y, 0]),
                C.text(T["door_n"].format(n=opened + 1), S.LABEL_SIZE, S.INK).move_to([cols[1], y, 0]),
                verdict(stay_win).move_to([cols[2], y, 0]),
                verdict(not stay_win).move_to([cols[3], y, 0])))
        sep = Line(LEFT * 2.9, RIGHT * 2.9, color=S.FAINT, stroke_width=1.5).set_y(-1.55)
        cues = ["车在一号门", "车在二号门", "车在三号门"]
        win_cues = ["坚持赢", "换门赢", "还是换门赢"]

        with self.voice("cases.1") as v:
            self.clear_stage(run_time=0.4)
            self.set_header(T["cases_t"], T["cases_s"])
            heads = VGroup(*[C.text(t, S.SMALL_SIZE, S.MUTED, weight="BOLD").move_to([x, 1.75, 0])
                             for t, x in zip(T["cols"], cols)])
            self.play(FadeIn(heads), run_time=0.3)
            for k, row in enumerate(rows):
                v.until(cues[k])
                self.sfx("tick")
                self.play(FadeIn(row[:2], shift=RIGHT * 0.1), run_time=0.3)
                self.wait(0.3)
                v.until(win_cues[k])
                self.sfx("pop", gain=-6)
                self.play(FadeIn(row[2:], shift=UP * 0.05), run_time=0.3)
                self.wait(0.35)
            v.until("三种情况")
            totals = VGroup(
                C.text(T["total"], S.LABEL_SIZE, S.INK, weight="BOLD").move_to([cols[0], -2.05, 0]),
                frac(1, 3, S.MUTED, 1.1).move_to([cols[2], -2.05, 0]),
                frac(2, 3, S.TEAL, 1.25).move_to([cols[3], -2.05, 0]))
            self.play(Create(sep), FadeIn(totals), run_time=0.4)
            hl = C.pill(VGroup(*[r[3] for r in rows], totals[2]).copy(), S.TEAL, pad=0.15,
                        fill_opacity=0.08)[0]
            v.until("换门赢两种")
            self.sfx("chime", gain=-4)
            self.play(FadeIn(hl), run_time=0.4)
            self.wait(1.4)

    # 8. Monte-Carlo simulation -----------------------------------------------------------
    def simulate(self):
        T = self.T
        n_games = 1000
        rng = np.random.default_rng(2024)
        car = rng.integers(0, 3, n_games)
        pick = rng.integers(0, 3, n_games)
        stay = np.cumsum(car == pick) / np.arange(1, n_games + 1)
        switch = np.cumsum(car != pick) / np.arange(1, n_games + 1)

        ax = Axes(x_range=[0, n_games, 250], y_range=[0, 1, 0.25], x_length=5.0,
                  y_length=3.0, tips=False,
                  axis_config={"color": S.FAINT, "stroke_width": 1.5, "include_ticks": False},
                  ).move_to(RIGHT * 0.15)
        guides = VGroup()
        for val, col in ((1 / 3, S.MUTED), (2 / 3, S.TEAL)):
            guides.add(DashedLine(ax.c2p(0, val), ax.c2p(n_games, val), color=col,
                                  stroke_width=1.2, dash_length=0.06, stroke_opacity=0.6))
        ylabs = VGroup(*[C.text(t, S.SMALL_SIZE - 2, S.MUTED).next_to(ax.c2p(0, val), LEFT,
                                                                     buff=0.1)
                         for t, val in (("0%", 0), ("33%", 1 / 3), ("67%", 2 / 3), ("100%", 1))])
        xlab = C.text(T["games_played"], S.SMALL_SIZE - 1, S.MUTED).next_to(ax, DOWN, buff=0.12)
        n = ValueTracker(1)

        def curve(data, color):
            def build():
                k = max(2, int(n.get_value()))
                xs = np.arange(1, k + 1)
                idx = np.unique(np.linspace(0, k - 1, min(k, 300)).astype(int))
                m = VMobject(stroke_color=color, stroke_width=3.5)
                m.set_points_as_corners([ax.c2p(xs[i], data[i]) for i in idx])
                return m
            return always_redraw(build)

        def readout(label, data, color, x):
            def build():
                k = max(1, int(n.get_value()))
                return VGroup(
                    C.text(label, S.LABEL_SIZE + 2, color, weight="BOLD"),
                    C.text(f"{data[k - 1] * 100:4.1f}%", S.LABEL_SIZE + 2, color, weight="BOLD",
                           font=S.MONO)).arrange(RIGHT, buff=0.2).move_to([x, -2.35, 0])
            return always_redraw(build)

        with self.voice("sim.1") as v:
            self.clear_stage(run_time=0.4)
            self.set_header(T["sim_t"], T["sim_s"])
            self.play(Create(ax), FadeIn(guides), FadeIn(ylabs), FadeIn(xlab), run_time=0.5)
            c_stay, c_switch = curve(stay, S.INK), curve(switch, S.TEAL)
            r_stay = readout(T["sim_stay"], stay, S.INK, -1.35)
            r_sw = readout(T["sim_switch"], switch, S.TEAL, 1.45)
            count = always_redraw(lambda: C.text(T["game_n"].format(n=int(n.get_value())),
                                                 S.SMALL_SIZE, S.MUTED).move_to([0, -2.9, 0]))
            self.add(c_stay, c_switch, r_stay, r_sw, count)
            v.until("一千局")
            # Ticks speed up with the counter (games are paced exponentially).
            dur = 3.2
            for k in range(24):
                self.sfx("tick", delay=dur * (k / 24) ** 1.6, gain=-8)
            self.play(n.animate.set_value(n_games), run_time=dur, paced=False,
                      rate_func=lambda a: a ** 2.2)
            for m in (c_stay, c_switch, r_stay, r_sw, count):
                m.clear_updaters()
            v.until("百分之三十三")
            self.play(r_stay.animate.scale(1.08), run_time=0.25)
            v.until("百分之六十七")
            self.sfx("chime", gain=-4)
            self.play(r_sw.animate.scale(1.15), run_time=0.3)
            self.wait(1.4)

    # 9. 100 doors ------------------------------------------------------------------------
    def hundred(self):
        T = self.T
        cells = VGroup()
        for i in range(100):
            r = RoundedRectangle(corner_radius=0.03, width=0.36, height=0.40,
                                 fill_color=DOOR_FILL, fill_opacity=1, stroke_color=DOOR_EDGE,
                                 stroke_width=1)
            r.add(C.text(str(i + 1), 9, S.BG, font="Inter").move_to(r))
            cells.add(r)
        cells.arrange_in_grid(10, 10, buff=(0.1, 0.08)).move_to(DOWN * 0.15)
        keep = 72   # door 73 stays closed
        others = [c for i, c in enumerate(cells) if i not in (0, keep)]

        with self.voice("hundred.1") as v:
            self.clear_stage(run_time=0.4)
            self.set_header(T["h_t"], T["h_s"])
            v.until("一百扇门", lead=0.2)
            self.sfx("whoosh")
            self.play(LaggedStart(*[FadeIn(c, scale=0.6) for c in cells], lag_ratio=0.01),
                      run_time=0.9)
            self.wait(0.4)
            v.until("你选一号")
            self.sfx("click")
            self.play(cells[0][0].animate.set_stroke(S.TEAL, 5), run_time=0.3)
            self.wait(0.4)
            v.until("主持人打开")
            self.set_header(T["h2_t"], T["h2_s"], run_time=0.4)
            for k in range(6):
                self.sfx("door", delay=k * 0.3 * self.PACE, gain=-10)
            self.play(LaggedStart(*[c.animate.set_fill(INSIDE).set_stroke(S.FAINT)
                                    for c in others], lag_ratio=0.015),
                      *[c[1].animate.set_opacity(0) for c in others], run_time=1.8)
            v.until("七十三号", lead=0.1)
            self.sfx("rise")
            self.play(cells[keep][0].animate.set_stroke(S.RED, 5), cells[keep].animate.scale(1.25),
                      cells[0].animate.scale(1.25), run_time=0.4)
        with self.voice("hundred.2"):
            q = VGroup(C.text(T["hq1"], S.LABEL_SIZE, S.INK),
                       C.text(T["hq2"], S.LABEL_SIZE, S.RED, weight="BOLD")
                       ).arrange(DOWN, buff=0.08).move_to(UP * -2.95)
            self.play(FadeIn(q, shift=UP * 0.1), run_time=0.4)
            self.wait(2.0)

    # 10. Outro -----------------------------------------------------------------------------
    def outro(self):
        T = self.T
        self.music("outro")
        doors = doors_row(("goat", "car", "goat"), y=0.55)
        doors[0].panel.set_stroke(S.TEAL, 5)
        res = VGroup(
            VGroup(C.text(T["out_stay"], S.LABEL_SIZE, S.MUTED), frac(1, 3, S.MUTED, 1.1)
                   ).arrange(RIGHT, buff=0.15),
            C.text(T["vs"], S.SMALL_SIZE, S.MUTED),
            VGroup(C.text(T["out_switch"], S.LABEL_SIZE, S.TEAL, weight="BOLD"),
                   frac(2, 3, S.TEAL, 1.25)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.35)
        box = C.pill(res.scale(1.35), S.INK, pad=0.22).move_to(UP * -1.45)
        tag = VGroup(C.text(T["tag1"], S.LABEL_SIZE + 2, S.INK, weight="BOLD", slant="ITALIC"),
                     C.text(T["tag2"], S.SMALL_SIZE - 2, S.TEAL, slant="ITALIC")
                     ).arrange(DOWN, buff=0.1)
        tag.next_to(box, DOWN, buff=0.28)

        with self.voice("outro.1") as v:
            self.clear_stage(run_time=0.4)
            self.set_header(T["out_t"], T["out_s"])
            self.play(FadeIn(doors), run_time=0.4)
            self.sfx("door")
            self.play(doors[2].open(), run_time=0.4)
            self.sfx("door", delay=0.15)
            self.play(doors[1].open(), run_time=0.4)
            self.sfx("chime")
            self.play(doors[1].prize.animate.scale(1.15), run_time=0.3)
            v.until("永远要换门", lead=0.2)
            self.play(FadeIn(box), run_time=0.4)
            v.until("新的信息")
            self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.5)
            self.wait(2.4)

    # 11. End card: follow + next episode -------------------------------------------------
    def endcard(self):
        T = self.T
        avatar = VGroup(Circle(radius=0.62, fill_color=S.TEAL, fill_opacity=1, stroke_width=0),
                        C.text(T["avatar"], 40, S.BG, weight="BOLD"))
        handle = C.text(T["handle"], S.LABEL_SIZE + 4, S.INK, weight="BOLD")
        btn_box = RoundedRectangle(corner_radius=0.22, width=2.0, height=0.6, stroke_width=0,
                                   fill_color=S.RED, fill_opacity=1)
        btn_txt = C.text(T["follow"], S.LABEL_SIZE + 2, S.BG, weight="BOLD").move_to(btn_box)
        btn = VGroup(btn_box, btn_txt)
        VGroup(avatar, handle, btn).arrange(DOWN, buff=0.3).move_to(UP * 1.75)

        nxt_lbl = C.pill(C.text(T["next_lbl"], S.SMALL_SIZE, S.TEAL, weight="BOLD"), S.TEAL,
                         pad=0.1)
        nxt_t = C.text(T["next_t"], S.LABEL_SIZE + 6, S.INK, weight="BOLD")
        nxt_s = C.text(T["next_s"], S.LABEL_SIZE, S.MUTED)
        card_in = VGroup(nxt_lbl, nxt_t, nxt_s).arrange(DOWN, buff=0.2)
        card = VGroup(RoundedRectangle(corner_radius=0.18, width=5.4, height=card_in.height + 0.6,
                                       stroke_color=S.FAINT, stroke_width=2,
                                       fill_color="#FFFFFF", fill_opacity=0.5), card_in)
        card[0].move_to(card_in)
        card.move_to(DOWN * 1.35)

        with self.voice("endcard.1") as v:
            self.clear_stage(run_time=0.4)
            self.sfx("whoosh")
            self.play(GrowFromCenter(avatar), FadeIn(handle, shift=UP * 0.1), run_time=0.5)
            self.play(FadeIn(btn, scale=0.8), run_time=0.3)
            v.until("下期")
            self.sfx("click")
            self.play(btn_box.animate.set_fill(S.FAINT).scale(0.94),
                      Transform(btn_txt, C.text(T["followed"], S.LABEL_SIZE + 2, S.INK,
                                                weight="BOLD").move_to(btn_box)),
                      run_time=0.25)
            self.play(btn_box.animate.scale(1 / 0.94), run_time=0.15)
            self.sfx("pop")
            self.play(FadeIn(card, shift=UP * 0.2), run_time=0.5)
        # Land the final chord on a bar line, then let it ring over the card.
        self.wait_for_downbeat(min_wait=0.2)
        self.music_end()
        self.play(card.animate.scale(1.03), run_time=0.4, paced=False)
        self.hold(2.8)


class MontyHallZH(MontyHall):
    """Chinese version with voice-over and burned-in subtitles."""
    LANG = "zh"
    NARRATION = NARRATION_ZH
    VOICE = "zh-CN-YunxiNeural"
    SFX_GAIN = -9.0            # sit effects under the voice

    def setup(self):
        S.FONT = "Noto Sans CJK SC"
        S.ITALIC_OK = False
        super().setup()
