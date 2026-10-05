// SpaceX whiteboard sample (~33s) — layout and timing reconstructed from the reference video.
const DURATION = 33.2;

const SUBS = [
  [0.3, 3.0, '2008年 SpaceX的火箭已经连败三次'],
  [3.0, 4.65, '钱只够再打最后一发'],
  [4.7, 7.0, '9月28号 那一发成了'],
  [7.0, 9.0, '整整18年后的同一天'],
  [9.0, 10.55, '星舰第一次进入了地球轨道'],
  [10.6, 12.9, '两分钟 看完它这24年'],
  [13.7, 15.6, '2002年 马斯克创办了SpaceX'],
  [15.6, 18.8, '目标是 有一天让人类住到别的星球上'],
  [19.6, 21.25, '它的第一款火箭 叫猎鹰1号'],
  [21.3, 25.0, '2006年 失败 2007年 失败'],
  [25.0, 27.6, '2008年8月 还是失败'],
  [27.6, 29.2, '第四次 成了'],
  [29.2, 31.0, '成为第一枚私人研制'],
  [31.0, 33.2, '进入轨道的液体燃料火箭'],
];

// ---- helpers for moving objects ----
function pathFollower(pts) {
  const L = [0];
  for (let i = 1; i < pts.length; i++) L.push(L[i - 1] + Math.hypot(pts[i][0] - pts[i - 1][0], pts[i][1] - pts[i - 1][1]));
  const total = L[L.length - 1];
  return u => {
    const d = clamp(u) * total;
    let i = 1;
    while (i < L.length - 1 && L[i] < d) i++;
    const f = (d - L[i - 1]) / (L[i] - L[i - 1] || 1);
    const a = pts[i - 1], b = pts[i];
    return { x: lerp(a[0], b[0], f), y: lerp(a[1], b[1], f), rot: (Math.atan2(b[1] - a[1], b[0] - a[0]) * 180) / Math.PI + 90 };
  };
}
function orbitPos(o, theta) {
  const r = (o.rot * Math.PI) / 180, x = o.rx * Math.cos(theta), y = o.ry * Math.sin(theta);
  const dx = -o.rx * Math.sin(theta), dy = o.ry * Math.cos(theta);
  const tx = dx * Math.cos(r) - dy * Math.sin(r), ty = dx * Math.sin(r) + dy * Math.cos(r);
  return { x: o.cx + x * Math.cos(r) - y * Math.sin(r), y: o.cy + x * Math.sin(r) + y * Math.cos(r), rot: (Math.atan2(ty, tx) * 180) / Math.PI + 90 };
}
// rocket that stands at base, launches along a trail at [l0,l1] and then orbits
function launchRocket({ base, w, h, draw, l0, l1, trail, endScale, orbit, omega = 1.0 }) {
  const follow = pathFollower(trail);
  const xf = t => {
    if (t < l0) return { x: base[0], y: base[1], rot: 0, s: 1 };
    if (t < l1) {
      const u = clamp((t - l0) / (l1 - l0)), e = u * u * (1.6 - 0.6 * u);
      const p = follow(e);
      return { ...p, s: Math.exp(lerp(0, Math.log(endScale), easeSine(u))) };
    }
    return { ...orbitPos(orbit, Math.PI + (t - l1) * omega), s: endScale };
  };
  board.draw(draw[0], draw[1], rocketShape(w, h), { xf });
  board.shape(flameShape(w), { xf: t => { const b = xf(t); return { ...b, s: (b.s ?? 1) * (0.9 + 0.12 * Math.sin(t * 60)) }; }, vis: t => t > l0 - 0.12 && t < l1 - 0.05 });
  board.draw(l0, l1, [S(trail, { amp: 0.6, color: ORANGE, width: 4, dash: '13 10' })], { pen: false });
  return xf;
}
// rocket that rises and blows up
function failRocket({ x, ground, w, h, draw, rise, boomAt, boom }) {
  const xf = t => {
    const u = clamp((t - (boomAt - 0.32)) / 0.32);
    return { x, y: ground - rise * u * u, rot: 0, s: 1 };
  };
  board.draw(draw[0], draw[1], rocketShape(w, h), { xf, vis: t => t < boomAt });
  board.shape(flameShape(w), { xf: t => ({ ...xf(t), s: 0.9 + 0.15 * Math.sin(t * 70) }), vis: t => t > boomAt - 0.34 && t < boomAt });
  board.draw(boomAt, boomAt + 0.45, explosionShape(boom[0], boom[1], boom[2]));
}

function buildScene() {
  const T = board.text.bind(board), D = board.draw.bind(board);
  const K = 170; // big year titles

  // ================= Scene A : 2008 -> 2026 =================
  const y2008 = T(-1.2, -0.6, '2008', 490, 222, K);
  T(0.3, 0.85, '年', 490 + y2008.width, 222, K);
  [574, 742, 912].forEach((x, i) => D(-2 + i * 0.3, -1.75 + i * 0.3, rocketShape(74, 440), { xf: () => ({ x, y: 820 }) }));
  const X = (cx, cy, s) => [S(sampleLine([cx - s, cy - s], [cx + s, cy + s]), { amp: 0.6, color: ORANGE }), S(sampleLine([cx + s, cy - s], [cx - s, cy + s]), { amp: 0.6, color: ORANGE })];
  D(-0.6, -0.3, X(574, 588, 72));
  D(-0.25, 0.25, X(742, 588, 72));
  D(1.95, 2.35, X(912, 588, 72));
  T(2.42, 2.98, '连败三次', 1030, 595, 100, { color: ORANGE });

  D(3.3, 3.72, moneyBagShape(1542, 570, 200));
  T(3.72, 3.8, '$', 1515, 610, 96, { stroke: 2 });
  D(3.82, 3.95, arrowShape([1666, 578], [1820, 578], { head: 20 }));
  const orbA = { cx: 2340, cy: 186, rx: 130, ry: 45, rot: -8 };
  launchRocket({ base: [1956, 820], w: 74, h: 450, draw: [3.97, 4.42], l0: 6.0, l1: 6.45, endScale: 0.17, orbit: orbA, omega: 1.1,
    trail: smooth([[1956, 820], [1962, 660], [1995, 520], [2050, 400], [2120, 296], [2211, 204]], false, 10) });
  T(4.46, 4.84, '最后一发', 1376, 330, 88, { color: ORANGE });
  T(4.9, 5.32, '9.28', 2086, 640, 150);
  D(5.36, 5.86, earthShape(2340, 186, 70));
  D(5.86, 6.02, orbitShape(orbA.cx, orbA.cy, orbA.rx, orbA.ry, orbA.rot));
  D(6.06, 6.2, checkShape(2168, 400, 52));
  T(6.22, 6.88, '成了', 2240, 412, 92, { color: ORANGE });
  D(6.95, 7.25, arrowShape([2406, 604], [2870, 566], { color: ORANGE, curve: [2640, 575], width: 5 }));
  T(7.28, 7.62, '18年后', 2520, 504, 74);
  T(7.8, 8.15, '9.28', 3000, 560, 140);
  D(8.15, 8.3, [...underline([2990, 624], [3270, 622], { bow: 2 }), ...underline([2996, 644], [3266, 643], { bow: 2 })]);
  T(8.3, 8.52, '同一天', 3030, 704, 73, { color: ORANGE });
  T(8.85, 9.3, '2026年', 2980, 204, K);
  D(9.32, 9.88, earthShape(3794, 500, 144));
  const orbB = { cx: 3793, cy: 502, rx: 263, ry: 98, rot: -10 };
  D(9.88, 10.0, orbitShape(orbB.cx, orbB.cy, orbB.rx, orbB.ry, orbB.rot, { solid: true, width: 4 }));
  T(10.0, 10.3, '星舰入轨', 3650, 249, 72, { color: ORANGE });
  D(10.3, 10.5, rocketShape(26, 140), { xf: t => ({ ...orbitPos(orbB, Math.PI * 0.82 + Math.max(0, t - 10.3) * 1.25), s: 1 }) });

  // timeline overview
  D(10.85, 11.45, [S(sampleLine([490, 914], [3979, 914]), { amp: 1.5, width: 6 })]);
  D(11.4, 11.5, [490, 1356, 3979].map(x => S(sampleLine([x, 896], [x, 932]), { amp: 0, width: 6 })));
  T(11.5, 11.6, '2002', 395, 990, 86);
  T(11.6, 11.7, '2008', 1261, 990, 86);
  T(11.7, 11.8, '2026', 3884, 990, 86);
  T(11.82, 12.1, '24年', 2134, 816, 95, { color: ORANGE });

  // ================= Scene B : 2002 =================
  T(13.9, 14.38, '2002年', 4520, 230, K);
  D(14.4, 14.75, stickShape(4694, 420, 36, 'wave'));
  T(14.75, 14.95, '马斯克', 4596, 770, 64);
  D(14.95, 15.15, arrowShape([4816, 530], [5000, 530], { head: 20 }));
  T(15.2, 15.65, 'SpaceX', 5050, 520, 140);
  D(15.65, 15.8, underline([5049, 612], [5455, 600], { bow: 5 }));
  T(15.82, 16.1, '目标', 5776, 240, 115, { color: ORANGE });
  D(16.15, 16.66, earthShape(5888, 585, 150));
  const arc = smooth([[5996, 476], [6200, 330], [6406, 290], [6560, 318], [6668, 395]], false, 12);
  D(16.7, 17.95, [S(arc, { amp: 0.6, color: ORANGE, width: 4.5, dash: '14 10' }), S(poly([[6640, 360], [6668, 395], [6626, 398]]), { amp: 0, color: ORANGE, width: 4.5 })]);
  const mars = marsShape(6790, 399, 121);
  D(18.0, 18.22, [mars[0]]);
  D(18.22, 18.48, mars.slice(1));
  D(18.5, 18.7, houseShape(6790, 282, 100));

  // ================= Scene C : Falcon 1 =================
  const O = 12000;
  D(19.55, 19.82, stickShape(O + 830, 566, 26, 'neutral'), { vis: t => !despair(t) });
  board.shape(stickShape(O + 830, 566, 26, 'despair'), { vis: despair });
  D(19.84, 20.42, rocketShape(110, 656), { xf: () => ({ x: O + 265, y: 820 }) });
  T(20.72, 21.12, '猎鹰1号', O + 400, 200, 130);
  D(21.15, 21.45, [S(smooth([[O + 1004, 692], [O + 1400, 689], [O + 1900, 693]], false, 30), { amp: 1.5, width: 6 })]);
  D(25.3, 25.5, [S(smooth([[O + 1900, 693], [O + 2200, 690], [O + 2450, 694]], false, 30), { amp: 1.5, width: 6 })]);
  failRocket({ x: O + 1165, ground: 690, w: 36, h: 250, draw: [21.5, 21.88], rise: 80, boomAt: 22.42, boom: [O + 1170, 488, 95] });
  T(21.9, 22.16, '2006', O + 1090, 750, 66);
  failRocket({ x: O + 1538, ground: 690, w: 36, h: 250, draw: [23.02, 23.38], rise: 225, boomAt: 24.62, boom: [O + 1540, 340, 95] });
  T(23.4, 23.66, '2007', O + 1466, 750, 66);
  failRocket({ x: O + 1892, ground: 690, w: 36, h: 250, draw: [25.0, 25.3], rise: 345, boomAt: 26.3, boom: [O + 1890, 220, 92] });
  T(25.52, 25.84, '2008.8', O + 1794, 750, 65);
  D(26.8, 27.2, earthShape(O + 2640, 190, 110));
  const orbC = { cx: O + 2640, cy: 190, rx: 180, ry: 55, rot: -6 };
  D(27.2, 27.42, orbitShape(orbC.cx, orbC.cy, orbC.rx, orbC.ry, orbC.rot));
  launchRocket({ base: [O + 2258, 690], w: 36, h: 250, draw: [27.44, 27.78], l0: 28.12, l1: 28.55, endScale: 0.36, orbit: orbC, omega: 0.9,
    trail: smooth([[O + 2254, 690], [O + 2262, 560], [O + 2290, 420], [O + 2340, 300], [O + 2400, 236], [O + 2461, 209]], false, 10) });
  T(27.78, 28.05, '第四次', O + 2170, 750, 60, { color: ORANGE });
  T(28.1, 28.48, '成了', O + 1960, 440, 125, { color: ORANGE });
  T(29.82, 30.62, [['第一枚', ORANGE], ['私人研制、', INK]], O + 2836, 454, 63);
  T(30.7, 32.25, '进入轨道的液体燃料火箭', O + 2836, 560, 64);
  D(32.3, 32.6, underline([O + 3162, 602], [O + 3422, 604], { bow: 4 }));

  function despair(t) { return (t > 22.78 && t < 23.45) || (t > 24.8 && t < 25.4) || (t > 26.65 && t < 27.3); }

  // ================= camera =================
  const c = (x, y, s = 1) => ({ x: x + 960 / s, y: y + 540 / s, s });
  board.camera([
    { t: 0, ...c(0, 0) },
    { t: 3.9, move: 0.9, ...c(990, 0) },
    { t: 8.2, move: 1.1, ...c(2270, -36) },
    { t: 11.5, move: 0.8, ...c(112, -473, 0.45) },
    { t: 12.7, ...c(112, -473, 0.45) },
    { t: 13.85, move: 1.15, ...c(4050, 0) },
    { t: 16.5, move: 0.8, ...c(5406, -40) },
    { t: 18.72, move: 0.5, ...c(4435, -207, 0.71) },
    { t: 19.0, ...c(4435, -207, 0.71) },
    { t: 19.6, move: 0.6, ...c(O, 0), ease: easeSine, blur: true },
    { t: 25.7, move: 0.9, ...c(O + 1150, -36) },
    { t: 29.8, move: 1.0, ...c(O + 1766, -36) },
  ]);
}
