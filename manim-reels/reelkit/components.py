"""Reusable visual building blocks."""

from manim import (
    DOWN, LEFT, RIGHT, UP, ORIGIN,
    Circle, Dot, DecimalNumber, Line, MathTex, RoundedRectangle, Text,
    VGroup, VMobject,
)

from . import style as S


def text(s, size=S.LABEL_SIZE, color=S.INK, weight="NORMAL", slant="NORMAL", font=None):
    # Read S.FONT at call time so a scene can switch fonts (e.g. for Chinese).
    if not S.ITALIC_OK:
        slant = "NORMAL"
    return Text(s, font=font or S.FONT, font_size=size, color=color, weight=weight, slant=slant)


def title(s, color=S.INK):
    return text(s, S.TITLE_SIZE, color, weight="BOLD")


def subtitle(s, color=S.MUTED, slant="ITALIC"):
    return text(s, S.SUBTITLE_SIZE, color, slant=slant)


def math(tex, color=S.INK, scale=S.MATH_SCALE):
    return MathTex(tex, color=color).scale(scale)


def header(title_str, sub_str=None, title_color=S.INK, sub_color=S.MUTED, boxed=False):
    """Title (+ optional subtitle) pinned to the top of the frame."""
    t = title(title_str, title_color)
    if boxed:
        t = pill(t, title_color)
    max_w = S.FRAME_WIDTH - 2 * S.SIDE_MARGIN
    if t.width > max_w:
        t.scale_to_fit_width(max_w)
    t.move_to(UP * S.TITLE_Y)
    group = VGroup(t)
    if sub_str:
        sub = subtitle(sub_str, sub_color)
        if sub.width > max_w:
            sub.scale_to_fit_width(max_w)
        sub.next_to(t, DOWN, buff=S.SUBTITLE_GAP)
        group.add(sub)
    return group


def pill(mob, color=S.INK, pad=0.16, fill_opacity=0.0):
    """Wrap a mobject in a rounded outline, like a tag/badge."""
    box = RoundedRectangle(
        corner_radius=0.1,
        width=mob.width + 2 * pad,
        height=mob.height + 1.4 * pad,
        stroke_color=color, stroke_width=2,
        fill_color=color, fill_opacity=fill_opacity,
    ).move_to(mob)
    return VGroup(box, mob)


def formula_box(tex, color=S.INK, box_color=S.FAINT, scale=S.MATH_SCALE):
    box = pill(math(tex, color, scale), box_color, pad=0.2)
    max_w = S.FRAME_WIDTH - 2 * S.SIDE_MARGIN
    if box.width > max_w:
        box.scale_to_fit_width(max_w)
    return box


def bead(color=S.GOLD, radius=0.09):
    b = Circle(radius=radius, stroke_color="#8A6A22", stroke_width=1.5,
               fill_color=color, fill_opacity=1)
    return b


def point_label(point, name, direction=UP + LEFT, color=S.INK):
    dot = Dot(point, radius=0.045, color=color)
    lab = text(name, S.LABEL_SIZE, color, weight="BOLD").next_to(dot, direction, buff=0.08)
    return VGroup(dot, lab)


def timer(label="t = ", decimals=2, unit=" s", size=S.LABEL_SIZE, color=S.MUTED):
    """A 't = 1.23 s' readout. Returns (group, number) so callers can update it."""
    pre = text(label, size, color, font=S.MONO)
    num = DecimalNumber(0, num_decimal_places=decimals, font_size=size * 1.6, color=color)
    post = text(unit.strip(), size, color, font=S.MONO)
    g = VGroup(pre, num, post).arrange(RIGHT, buff=0.06)
    num.add_updater(lambda m: m.next_to(pre, RIGHT, buff=0.06))
    post.add_updater(lambda m: m.next_to(num, RIGHT, buff=0.08))
    return g, num


def glow(path: VMobject, color, width=6, layers=5, spread=3.5, opacity=0.12):
    """Soft glow behind a path: stacked wide translucent strokes."""
    g = VGroup()
    for i in range(layers, 0, -1):
        c = path.copy().set_stroke(color, width=width + i * spread, opacity=opacity)
        g.add(c)
    g.add(path.copy().set_stroke(color, width=width, opacity=1))
    return g


def legend(rows, size=S.SMALL_SIZE, line_len=0.35):
    """rows: list of (label, color). Returns a left-aligned VGroup of line+label rows."""
    items = VGroup()
    for name, color in rows:
        ln = Line(ORIGIN, RIGHT * line_len, color=color, stroke_width=4)
        lab = text(name, size, S.INK)
        items.add(VGroup(ln, lab).arrange(RIGHT, buff=0.15))
    items.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
    return items
