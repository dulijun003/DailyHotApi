"""Physics helpers: frictionless beads sliding on tracks under gravity.

World coordinates are metres with x to the right and y DOWNWARD (y = depth
below the start point), which is how the brachistochrone is usually written.
`World` maps them onto Manim scene coordinates.
"""

from dataclasses import dataclass

import numpy as np
from manim import VMobject

G = 9.81


@dataclass
class World:
    """Maps world metres (y down) to scene units (y up)."""
    origin: np.ndarray      # scene point of world (0, 0)
    scale: float            # scene units per metre

    def to_scene(self, x, y):
        return self.origin + np.array([x * self.scale, -y * self.scale, 0.0])

    def points(self, xs, ys):
        return np.array([self.to_scene(x, y) for x, y in zip(xs, ys)])


class Track:
    """A track sampled as a polyline, with bead travel time at every sample.

    The bead starts at rest at sample 0. Speed at depth y is sqrt(2 g y)
    (energy conservation). On a straight segment the acceleration is
    constant, so the segment takes exactly 2 ds / (v0 + v1).
    """

    def __init__(self, xs, ys, g=G):
        self.xs = np.asarray(xs, dtype=float)
        self.ys = np.asarray(ys, dtype=float)
        dx = np.diff(self.xs)
        dy = np.diff(self.ys)
        ds = np.hypot(dx, dy)
        v = np.sqrt(2 * g * np.maximum(self.ys, 0))
        v_sum = np.maximum(v[:-1] + v[1:], 1e-9)
        self.times = np.concatenate([[0.0], np.cumsum(2 * ds / v_sum)])
        self.lengths = np.concatenate([[0.0], np.cumsum(ds)])
        self.g = g

    @property
    def total_time(self):
        return float(self.times[-1])

    @property
    def length(self):
        return float(self.lengths[-1])

    def pos_at_time(self, t):
        t = np.clip(t, 0, self.total_time)
        return (float(np.interp(t, self.times, self.xs)),
                float(np.interp(t, self.times, self.ys)))

    def speed_at_time(self, t):
        _, y = self.pos_at_time(t)
        return float(np.sqrt(2 * self.g * max(y, 0)))

    def mobject(self, world: World, color, width=4):
        m = VMobject(stroke_color=color, stroke_width=width)
        m.set_points_as_corners(world.points(self.xs, self.ys))
        return m

    def subpath(self, world: World, t0, t1, color, width=4, n=120):
        """Mobject for the part of the track travelled between times t0 and t1."""
        ts = np.linspace(t0, t1, n)
        pts = [world.to_scene(*self.pos_at_time(t)) for t in ts]
        m = VMobject(stroke_color=color, stroke_width=width)
        m.set_points_smoothly(pts)
        return m


# ---- Track factories (A = (0, 0), B = (L, H)) ------------------------------

def straight(L, H, n=400):
    s = np.linspace(0, 1, n)
    return Track(L * s, H * s)


def shallow_parabola(L, H, n=400):
    # Sags slightly below the chord.
    s = np.linspace(0, 1, n)
    return Track(L * s, H * (2 * s - s * s) * 0.5 + H * s * 0.5)


def circular_arc(L, H, n=400):
    """Arc of a circle through A and B, vertical at A.

    Centre is on the horizontal line through A: (r, 0) with r chosen so the
    circle passes through B.
    """
    r = (L * L + H * H) / (2 * L)
    phi_b = np.arctan2(H, L - r)          # angle of B seen from centre (y down)
    phis = np.linspace(np.pi, phi_b, n)
    xs = r + r * np.cos(phis)
    ys = r * np.sin(phis)
    return Track(xs, ys)


def steep_polynomial(L, H, n=400):
    # Dives fast then wiggles up and down: shows that "steep" alone is not enough.
    s = np.linspace(0, 1, n)
    ys = H * (s + 1.6 * s * (1 - s) ** 2 - 0.9 * s * s * (1 - s))
    return Track(L * s, ys)


def cycloid_params(L, H):
    """Return (a, theta_B) for the cycloid x=a(t-sin t), y=a(1-cos t) through (L, H)."""
    target = L / H
    f = lambda t: (t - np.sin(t)) / (1 - np.cos(t)) - target
    lo, hi = 1e-6, 2 * np.pi - 1e-6
    for _ in range(200):
        mid = (lo + hi) / 2
        if f(mid) > 0:
            hi = mid
        else:
            lo = mid
    theta = (lo + hi) / 2
    a = H / (1 - np.cos(theta))
    return a, theta


def cycloid(L, H, n=600):
    a, theta_b = cycloid_params(L, H)
    # Dense sampling near A where the curve is vertical.
    th = theta_b * (np.linspace(0, 1, n) ** 1.5)
    return Track(a * (th - np.sin(th)), a * (1 - np.cos(th)))


def cycloid_time(L, H, g=G):
    a, theta_b = cycloid_params(L, H)
    return theta_b * np.sqrt(a / g)
