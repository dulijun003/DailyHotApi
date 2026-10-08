"""Brachistochrone: why the fastest path from A to B is a cycloid.

Render:  ./render.sh topics/brachistochrone.py Brachistochrone
"""

import sys
from pathlib import Path

import numpy as np
from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN,
    Circle, Create, DashedLine, Dot, FadeIn, FadeOut,
    Line, LaggedStart, Rectangle, ReplacementTransform, TracedPath,
    VGroup, VMobject, ValueTracker, Write, always_redraw, linear,
)

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from reelkit import components as C          # noqa: E402
from reelkit import physics as P             # noqa: E402
from reelkit import style as S               # noqa: E402
from reelkit.scene import ReelScene          # noqa: E402

# Problem setup: A at the origin, B 20 m across and 10 m down.
L, H = 20.0, 10.0
WORLD = P.World(origin=np.array([-2.55, 1.7, 0.0]), scale=0.255)
A_PT = WORLD.to_scene(0, 0)
B_PT = WORLD.to_scene(L, H)

TRACKS = {
    "Straight line":    (P.straight(L, H), S.INK),
    "Shallow parabola": (P.shallow_parabola(L, H), S.SLATE),
    "Circular arc":     (P.circular_arc(L, H), S.RED),
    "Steep polynomial": (P.steep_polynomial(L, H), S.OLIVE),
    "Cycloid":          (P.cycloid(L, H), S.TEAL),
}
STRAIGHT, _ = TRACKS["Straight line"]
ARC, _ = TRACKS["Circular arc"]
CYC, _ = TRACKS["Cycloid"]
CYC_A, CYC_THETA = P.cycloid_params(L, H)

BELOW = -2.35   # y of the first line of the caption area under the diagram


def endpoints():
    return VGroup(C.point_label(A_PT, "A", UP + LEFT), C.point_label(B_PT, "B", RIGHT))


def path(name, width=4):
    tr, color = TRACKS[name]
    return tr.mobject(WORLD, color, width)


class Brachistochrone(ReelScene):
    PACE = 0.7
    BEATS = [
        "hook", "result", "energy", "steep_drop", "dot_trail", "variational",
        "five_tracks", "winner", "reveal", "final_race", "trade_off", "outro",
    ]

    # 1. Question + first race -------------------------------------------------
    def hook(self):
        self.set_header("Which reaches the bottom first?",
                        "The shorter path… or the faster path?")
        self.ends = endpoints()
        self.line = path("Straight line")
        self.arc = path("Circular arc")
        self.play(FadeIn(self.ends), Create(self.line), Create(self.arc), run_time=1.2)

        self.b_line, self.b_arc = C.bead(), C.bead()
        self.b_line.move_to(A_PT)
        self.b_arc.move_to(A_PT)
        note = C.text("same start · same finish · identical beads", S.SMALL_SIZE, S.MUTED)
        note.move_to(UP * BELOW)
        self.timer, self.timer_num = C.timer()
        self.timer.to_edge(RIGHT, buff=0.45).set_y(2.05)
        self.play(FadeIn(self.b_line), FadeIn(self.b_arc), FadeIn(note), FadeIn(self.timer))
        self.race([(STRAIGHT, self.b_line), (ARC, self.b_arc)], WORLD,
                  timer_num=self.timer_num)
        self.play(FadeOut(note), run_time=0.3)

    # 2. The counter-intuitive result -----------------------------------------
    def result(self):
        self.set_header("Curved path wins", "Even though it travels farther.",
                        title_color=S.RED, sub_color=S.INK, boxed=True)
        lines = VGroup(
            C.math(r"L_{\text{curve}} > L_{\text{straight}}", S.MUTED),
            C.math(r"T_{\text{curve}} < T_{\text{straight}}", S.MUTED),
            C.text(f"{ARC.total_time:.2f} s  <  {STRAIGHT.total_time:.2f} s",
                   S.LABEL_SIZE, S.TEAL, font=S.MONO),
        ).arrange(DOWN, buff=0.18).move_to(UP * (BELOW - 0.4))
        self.play(LaggedStart(*[FadeIn(m, shift=UP * 0.1) for m in lines], lag_ratio=0.5),
                  run_time=1.6)
        self.wait(1.4)
        self.play(FadeOut(lines), FadeOut(self.timer), run_time=0.4)

    # 3. Energy: falling turns height into speed --------------------------------
    def energy(self):
        self.play(FadeOut(self.header_mob), FadeOut(self.b_line),
                  self.line.animate.set_stroke(S.FAINT, 2), run_time=0.4)
        self.header_mob = None
        self.b_arc.move_to(A_PT)

        t = ValueTracker(0.0)
        y_max = ARC.ys.max()
        bar_w = 2.0
        cap = C.text("energy along the drop", S.SMALL_SIZE - 2, S.MUTED)
        pot_lab = C.text("potential", S.SMALL_SIZE, S.MUTED)
        kin_lab = C.text("kinetic", S.SMALL_SIZE, S.RED_SOFT)
        pot_bg = Rectangle(width=bar_w, height=0.12, stroke_width=0, fill_color=S.FAINT,
                           fill_opacity=0.5)
        kin_bg = pot_bg.copy()
        rows = VGroup(VGroup(pot_lab, pot_bg).arrange(RIGHT, buff=0.15),
                      VGroup(kin_lab, kin_bg).arrange(RIGHT, buff=0.22))
        rows.arrange(DOWN, aligned_edge=RIGHT, buff=0.14)
        panel = VGroup(cap, rows).arrange(DOWN, buff=0.12)
        panel.to_corner(UP + RIGHT, buff=0.45)

        def depth():
            return ARC.pos_at_time(t.get_value())[1]

        def bar(bg, frac, color):
            return always_redraw(lambda: Rectangle(
                width=max(bar_w * frac(), 1e-3), height=0.12, stroke_width=0,
                fill_color=color, fill_opacity=1,
            ).align_to(bg, LEFT).align_to(bg, UP))

        pot = bar(pot_bg, lambda: 1 - depth() / y_max, S.MUTED)
        kin = bar(kin_bg, lambda: depth() / y_max, S.RED_SOFT)
        v_read = always_redraw(lambda: C.text(
            f"v = {ARC.speed_at_time(t.get_value()):.1f} m/s",
            S.SMALL_SIZE, S.RED, font=S.MONO).next_to(rows, DOWN, buff=0.12))

        def drop():
            x, y = ARC.pos_at_time(t.get_value())
            top, bot = WORLD.to_scene(x, 0), WORLD.to_scene(x, max(y, 1e-3))
            ln = DashedLine(top, bot, color=S.RED_SOFT, stroke_width=2, dash_length=0.06)
            ref = Line(A_PT, WORLD.to_scene(L, 0), color=S.FAINT, stroke_width=1.5)
            lab = C.text("y", S.SMALL_SIZE, S.RED).next_to(ln, RIGHT, buff=0.06)
            return VGroup(ref, ln, lab)

        drop_m = always_redraw(drop)
        self.b_arc.add_updater(lambda m: m.move_to(WORLD.to_scene(*ARC.pos_at_time(t.get_value()))))

        eq = VGroup(C.math(r"m g y = \tfrac{1}{2} m v^2"),
                    C.text("the mass m cancels", S.SMALL_SIZE, S.MUTED))
        eq.arrange(DOWN, buff=0.15).move_to(UP * (BELOW - 0.2))
        eq2 = C.math(r"g y = \tfrac{1}{2} v^2").move_to(eq[0])

        self.add(pot_bg, kin_bg, pot, kin)
        self.play(FadeIn(panel), FadeIn(drop_m), FadeIn(v_read), FadeIn(eq[0]), run_time=0.6)
        self.play(t.animate.set_value(ARC.total_time * 0.48), run_time=2.4, rate_func=linear)
        self.play(FadeIn(eq[1]), ReplacementTransform(eq[0], eq2), run_time=0.8)
        self.wait(0.6)
        self.b_arc.clear_updaters()
        for m in (pot, kin, v_read, drop_m):
            m.clear_updaters()
        self.play(*[FadeOut(m) for m in (panel, pot_bg, kin_bg, pot, kin, v_read, drop_m,
                                         eq2, eq[1])], run_time=0.4)

    # 4. Steep start = early speed ---------------------------------------------
    def steep_drop(self):
        self.set_header("A steep initial drop builds speed early.")
        sub = VGroup(C.text("Straight path: moderate acceleration", S.SMALL_SIZE + 1, S.INK),
                     C.text("Deep curve: rapid initial acceleration", S.SMALL_SIZE + 1, S.RED,
                            weight="BOLD")).arrange(DOWN, buff=0.1)
        sub.next_to(self.header_mob, DOWN, buff=0.18)
        self.play(self.line.animate.set_stroke(S.INK, 4), FadeIn(sub), run_time=0.5)
        self.b_line.move_to(A_PT)
        self.b_arc.move_to(A_PT)
        self.add(self.b_line, self.b_arc)

        def speed_label(track, bead, color):
            lbl = always_redraw(lambda: C.text(
                f"v = {np.sqrt(2 * P.G * max(self._depth(track, bead), 0)):.1f} m/s",
                S.SMALL_SIZE - 1, color, font=S.MONO).next_to(bead, UP + RIGHT, buff=0.05))
            return lbl

        lab_line = speed_label(STRAIGHT, self.b_line, S.INK)
        lab_arc = speed_label(ARC, self.b_arc, S.RED)
        self.add(lab_line, lab_arc)
        box = C.formula_box(r"v = \sqrt{2 g y}", S.INK, S.RED_SOFT).move_to(UP * BELOW)
        hint = C.text("deeper → faster", S.SMALL_SIZE, S.RED_SOFT).next_to(box, DOWN, buff=0.15)
        self.play(FadeIn(box), FadeIn(hint), run_time=0.4)
        self.race([(STRAIGHT, self.b_line), (ARC, self.b_arc)], WORLD, t_end=0.75,
                  speed=0.3, hold=1.2)
        lab_line.clear_updaters()
        lab_arc.clear_updaters()
        self.play(*[FadeOut(m) for m in (sub, lab_line, lab_arc, box, hint,
                                         self.b_line, self.b_arc)], run_time=0.4)

    def _depth(self, track, bead):
        # Depth (world y) of a bead from its scene position.
        return (WORLD.origin[1] - bead.get_center()[1]) / WORLD.scale

    # 5. Dot trail: equal time steps ------------------------------------------
    def dot_trail(self):
        step = 0.2
        n_line = int(STRAIGHT.total_time / step)
        n_arc = int(ARC.total_time / step)
        self.set_header("Each dot marks 0.2 s of travel")
        counts = VGroup(C.text(f"straight: {n_line} dots", S.SMALL_SIZE, S.INK),
                        C.text(f"curve: {n_arc} dots", S.SMALL_SIZE, S.RED)
                        ).arrange(RIGHT, buff=0.4).next_to(self.header_mob, DOWN, buff=0.2)

        dots = VGroup()
        for track, color in ((STRAIGHT, S.INK), (ARC, S.RED)):
            for k in range(1, int(track.total_time / step) + 1):
                d = Dot(WORLD.to_scene(*track.pos_at_time(k * step)), radius=0.035, color=color)
                d.t_mark = k * step
                d.set_opacity(0)
                dots.add(d)
        self.add(dots)
        b1, b2 = C.bead().move_to(A_PT), C.bead().move_to(A_PT)
        self.add(b1, b2)

        def reveal(t):
            for d in dots:
                if t >= d.t_mark:
                    d.set_opacity(1)

        formula = C.math(r"dt = \frac{ds}{v}").scale(1.2).move_to(UP * BELOW)
        self.play(FadeIn(counts), FadeIn(formula), run_time=0.4)
        self.race([(STRAIGHT, b1), (ARC, b2)], WORLD, speed=0.9,
                  extra_updaters=[reveal], hold=1.0)
        self.clear_stage(run_time=0.5)

    # 6. Turning it into a functional ------------------------------------------
    def variational(self):
        self.set_header("Describe any path as y = y(x)", "with y measured downward from A")
        o = A_PT + DOWN * 0.1
        x_ax = Line(o, o + RIGHT * 5.3, color=S.FAINT, stroke_width=1.5)
        y_ax = Line(o, o + DOWN * 3.0, color=S.FAINT, stroke_width=1.5)
        xl = C.text("x", S.SMALL_SIZE, S.MUTED, slant="ITALIC").next_to(x_ax, RIGHT, buff=0.08)
        yl = C.text("y", S.SMALL_SIZE, S.MUTED, slant="ITALIC").next_to(y_ax, DOWN, buff=0.08)
        a = C.point_label(o, "A", UP + LEFT)
        b_pt = o + RIGHT * 5.0 + DOWN * 1.9
        b = C.point_label(b_pt, "B", RIGHT)

        xs = np.linspace(0, 1, 100)
        ys = 1.9 * (2.2 * xs - 2.0 * xs ** 2 + 0.8 * xs ** 3)
        curve = VMobject(stroke_color=S.TEAL, stroke_width=4)
        curve.set_points_smoothly([o + RIGHT * 5.0 * x + DOWN * y for x, y in zip(xs, ys)])
        y_lab = C.math(r"y = y(x)", S.INK, 0.6).next_to(curve.point_from_proportion(0.75),
                                                         UP + RIGHT, buff=0.15)

        self.play(Create(x_ax), Create(y_ax), FadeIn(xl), FadeIn(yl), FadeIn(a), FadeIn(b),
                  run_time=0.6)
        self.play(Create(curve), FadeIn(y_lab), run_time=1.0)

        # Little ds triangle on the curve.
        p0 = curve.point_from_proportion(0.42)
        p1 = curve.point_from_proportion(0.5)
        corner = np.array([p1[0], p0[1], 0])
        tri = VGroup(
            DashedLine(p0, corner, color=S.MUTED, stroke_width=1.5, dash_length=0.04),
            DashedLine(corner, p1, color=S.MUTED, stroke_width=1.5, dash_length=0.04),
            C.math("dx", S.MUTED, 0.45).next_to(Line(p0, corner), UP, buff=0.04),
            C.math("dy", S.MUTED, 0.45).next_to(Line(corner, p1), RIGHT, buff=0.04),
            C.math("ds", S.MUTED, 0.45).next_to(Line(p0, p1).get_center(), DOWN + LEFT, buff=0.04),
        )
        steps = VGroup(
            C.math(r"ds = \sqrt{dx^2 + dy^2}"),
            C.math(r"ds = \sqrt{1 + \left(\tfrac{dy}{dx}\right)^2}\,dx"),
            C.math(r"v = \sqrt{2 g y}"),
        ).arrange(DOWN, buff=0.18).move_to(UP * (BELOW + 0.15))
        self.play(FadeIn(tri), run_time=0.4)
        for s in steps:
            self.play(Write(s), run_time=0.7)
        self.wait(0.4)

        funct = C.formula_box(r"T[y] = \int_0^{x_B} \sqrt{\frac{1 + y'^2}{2 g y}}\,dx",
                              S.INK, S.TEAL, scale=0.62)
        funct.move_to(UP * (BELOW - 0.2))
        punch = VGroup(C.text("Now we must minimize an entire path.", S.SMALL_SIZE + 1, S.INK,
                              weight="BOLD"),
                       C.text("This is a problem in the calculus of variations.",
                              S.SMALL_SIZE, S.TEAL, slant="ITALIC")).arrange(DOWN, buff=0.08)
        punch.next_to(funct, DOWN, buff=0.15)
        self.play(steps.animate.scale(0.6).set_opacity(0.3).next_to(funct, UP, buff=0.12),
                  VGroup(x_ax, y_ax, xl, yl, tri).animate.set_opacity(0.35),
                  FadeIn(funct, shift=UP * 0.1), run_time=0.8)
        self.play(FadeIn(punch), run_time=0.5)
        self.wait(1.6)
        self.clear_stage()

    # 7. Five tracks race -------------------------------------------------------
    def five_tracks(self):
        self.set_header("Same bead. Same gravity. Five tracks.")
        self.ends = endpoints()
        self.paths = {name: path(name, 3.5) for name in TRACKS}
        self.play(FadeIn(self.ends),
                  LaggedStart(*[Create(p) for p in self.paths.values()], lag_ratio=0.15),
                  run_time=1.4)

        names = list(TRACKS)
        self.legend = C.legend([(n, TRACKS[n][1]) for n in names])
        self.times = VGroup(*[
            C.text(f"T = {TRACKS[n][0].total_time:.2f} s", S.SMALL_SIZE, S.MUTED, font=S.MONO)
            for n in names])
        for row, tm in zip(self.legend, self.times):
            tm.move_to(row).set_x(1.9)
        self.legend.to_edge(LEFT, buff=0.7).set_y(BELOW - 0.6)
        for row, tm in zip(self.legend, self.times):
            tm.set_y(row.get_y())
        self.play(FadeIn(self.legend), run_time=0.4)

        beads = [C.bead().move_to(A_PT) for _ in names]
        self.add(*beads)
        finished = set()

        def stamp(t):
            for i, n in enumerate(names):
                if i not in finished and t >= TRACKS[n][0].total_time:
                    finished.add(i)
                    self.add(self.times[i])

        self.race([(TRACKS[n][0], b) for n, b in zip(names, beads)], WORLD,
                  extra_updaters=[stamp], hold=0.6)
        self.beads = beads

    # 8. One curve wins ---------------------------------------------------------
    def winner(self):
        self.set_header("One curve consistently wins.", title_color=S.TEAL)
        others = [n for n in TRACKS if n != "Cycloid"]
        win_row = VGroup(self.legend[-1], self.times[-1])
        hl = C.pill(win_row.copy(), S.TEAL, pad=0.08, fill_opacity=0.12)[0]
        self.play(*[self.paths[n].animate.set_stroke(opacity=0.18) for n in others],
                  *[VGroup(self.legend[i], self.times[i]).animate.set_opacity(0.3)
                    for i in range(len(others))],
                  *[FadeOut(b) for b in self.beads],
                  self.paths["Cycloid"].animate.set_stroke(width=6),
                  self.times[-1].animate.set_color(S.TEAL),
                  FadeIn(hl), run_time=0.8)
        self.wait(1.4)
        self.clear_stage(self.ends, self.paths["Cycloid"])
        self.cyc_path = self.paths["Cycloid"].set_stroke(width=4)

    # 9. Reveal: it's a cycloid -------------------------------------------------
    def reveal(self):
        self.set_header("BRACHISTOCHRONE = CYCLOID", "a point on a rolling circle traces it",
                        title_color=S.TEAL, boxed=True)
        ceiling = Line(A_PT + LEFT * 0.2, WORLD.to_scene(L + 1, 0), color=S.FAINT, stroke_width=1.5)
        r = CYC_A * WORLD.scale
        theta = ValueTracker(0.0)

        def centre():
            return WORLD.to_scene(CYC_A * theta.get_value(), CYC_A)

        def tracer():
            th = theta.get_value()
            return WORLD.to_scene(CYC_A * (th - np.sin(th)), CYC_A * (1 - np.cos(th)))

        wheel = always_redraw(lambda: VGroup(
            Circle(radius=r, stroke_color=S.MUTED, stroke_width=1.5,
                   fill_color=S.FAINT, fill_opacity=0.25).move_to(centre()),
            Line(centre(), tracer(), color=S.MUTED, stroke_width=1.5),
            Dot(tracer(), radius=0.05, color=S.TEAL),
        ))
        trace = TracedPath(tracer, stroke_color=S.TEAL, stroke_width=5)
        self.play(FadeOut(self.cyc_path), Create(ceiling), FadeIn(wheel), run_time=0.5)
        self.add(trace)
        self.play(theta.animate.set_value(CYC_THETA), run_time=3.6, rate_func=linear)
        eqs = VGroup(C.formula_box(r"x = a(\theta - \sin\theta)", S.INK, S.MUTED),
                     C.formula_box(r"y = a(1 - \cos\theta)", S.INK, S.MUTED)
                     ).arrange(DOWN, buff=0.12).move_to(UP * (BELOW - 0.3))
        self.play(FadeIn(eqs, shift=UP * 0.1), run_time=0.5)
        self.wait(1.0)
        wheel.clear_updaters()
        self.add(self.cyc_path)
        self.remove(trace)
        fit = C.text(f"fitted to A and B:  a = {CYC_A:.2f} m,  θ_B = {CYC_THETA:.2f} rad",
                     S.SMALL_SIZE - 2, S.MUTED).next_to(eqs, DOWN, buff=0.15)
        self.play(FadeOut(wheel), FadeOut(ceiling), FadeIn(fit), run_time=0.6)
        self.wait(0.8)
        self.clear_stage(self.ends, self.cyc_path)

    # 10. Final race ------------------------------------------------------------
    def final_race(self):
        self.set_header("The final race")
        names = ["Straight line", "Circular arc", "Cycloid"]
        lg = VGroup(*[
            VGroup(Line(ORIGIN, RIGHT * 0.3, color=TRACKS[n][1], stroke_width=4),
                   C.text(n.split()[0].lower() if n != "Circular arc" else "circular arc",
                          S.SMALL_SIZE, S.INK)).arrange(RIGHT, buff=0.1)
            for n in names]).arrange(RIGHT, buff=0.3).next_to(self.header_mob, DOWN, buff=0.2)
        line, arc = path("Straight line"), path("Circular arc")
        timer, num = C.timer()
        timer.to_edge(RIGHT, buff=0.45).set_y(2.05)
        self.play(FadeIn(lg), Create(line), Create(arc), FadeIn(timer), run_time=0.8)
        beads = [C.bead().move_to(A_PT) for _ in names]
        self.add(*beads)
        self.race([(TRACKS[n][0], b) for n, b in zip(names, beads)], WORLD,
                  timer_num=num, hold=0.8)
        self.clear_stage(self.ends, self.cyc_path)

    # 11. Why it wins: the trade-off --------------------------------------------
    def trade_off(self):
        self.set_header("The central trade-off")
        t_split = CYC.total_time * 0.22
        early = CYC.subpath(WORLD, 0, t_split, S.RED_SOFT, 6)
        late = CYC.subpath(WORLD, t_split, CYC.total_time, S.TEAL, 6)
        early_g = C.glow(early, S.RED_SOFT, 6)
        late_g = C.glow(late, S.TEAL, 6)

        early_lab = VGroup(C.text("Early: steep descent", S.SMALL_SIZE, S.RED, weight="BOLD"),
                           C.text("→ gain speed quickly", S.SMALL_SIZE, S.INK)
                           ).arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        early_lab.next_to(A_PT, RIGHT, buff=0.5).shift(UP * 0.5)
        pointer = Line(early_lab.get_left() + LEFT * 0.05, early.point_from_proportion(0.5),
                       color=S.RED_SOFT, stroke_width=1.5)
        self.play(FadeIn(early_g), FadeIn(early_lab), Create(pointer), run_time=0.8)
        self.wait(0.6)

        late_lab = VGroup(C.text("Later: use that speed", S.SMALL_SIZE, S.TEAL, weight="BOLD"),
                          C.text("across the remaining distance", S.SMALL_SIZE, S.INK)
                          ).arrange(DOWN, buff=0.05)
        late_lab.next_to(late, DOWN, buff=0.25)
        self.play(FadeIn(late_g), FadeIn(late_lab), run_time=0.8)

        box = C.pill(VGroup(C.text("extra distance", S.SMALL_SIZE + 1, S.INK),
                            C.text("vs", S.SMALL_SIZE, S.MUTED),
                            C.text("earlier acceleration", S.SMALL_SIZE + 1, S.INK)
                            ).arrange(RIGHT, buff=0.15), S.INK, pad=0.14)
        box.next_to(late_lab, DOWN, buff=0.3)
        punch = C.text("The cycloid finds the optimal balance.", S.LABEL_SIZE, S.TEAL,
                       weight="BOLD").next_to(box, DOWN, buff=0.25)
        self.play(FadeIn(box), run_time=0.5)
        self.play(FadeIn(punch, shift=UP * 0.1), run_time=0.5)
        self.wait(1.8)
        self.clear_stage(self.ends, self.cyc_path)

    # 12. Outro card ------------------------------------------------------------
    def outro(self):
        self.set_header("THE BRACHISTOCHRONE", "brachistos (shortest) + chronos (time)")
        ceiling = Line(A_PT, WORLD.to_scene(L + 1, 0), color=S.FAINT, stroke_width=1.5)
        th = CYC_THETA * 0.72
        wheel = Circle(radius=CYC_A * WORLD.scale, stroke_color=S.FAINT, stroke_width=1.5,
                       fill_color=S.FAINT, fill_opacity=0.2
                       ).move_to(WORLD.to_scene(CYC_A * th, CYC_A))
        b = C.bead().move_to(WORLD.to_scene(CYC_A * (th - np.sin(th)), CYC_A * (1 - np.cos(th))))
        eqs = C.formula_box(r"x = a(\theta - \sin\theta), \quad y = a(1 - \cos\theta)",
                            S.INK, S.INK).move_to(UP * (BELOW - 0.1))
        tag = VGroup(C.text("The fastest descent is not the shortest path.", S.LABEL_SIZE,
                            S.INK, weight="BOLD", slant="ITALIC"),
                     C.text("Nature's quickest route between two heights is not a straight line.",
                            S.SMALL_SIZE - 2, S.TEAL, slant="ITALIC")).arrange(DOWN, buff=0.1)
        tag.next_to(eqs, DOWN, buff=0.3)
        self.add_foreground_mobjects(self.cyc_path, b)
        self.play(FadeIn(ceiling), FadeIn(wheel), FadeIn(b), FadeIn(eqs), run_time=0.8)
        self.play(FadeIn(tag, shift=UP * 0.1), run_time=0.6)
        self.wait(2.5)
