// Hand-drawn icon library. Each returns an array of strokes ({pts, closed, color, width, dash}).

// Rocket standing on its nozzle; origin = nozzle bottom centre (0,0), pointing up, height h, width w.
function rocketShape(w, h, opt = {}) {
  const hw = w / 2, top = -h;
  const bodyBottom = top + h * 0.915, nose = top + h * 0.17;
  const outline = [
    ...poly([[-hw, bodyBottom], [-hw, nose]], 6),
    ...bez([-hw, nose], [-hw, top + h * 0.06], [-hw * 0.45, top], [0, top]).slice(1),
    ...bez([0, top], [hw * 0.45, top], [hw, top + h * 0.06], [hw, nose]).slice(1),
    ...poly([[hw, nose], [hw, bodyBottom], [-hw, bodyBottom]], 6).slice(1),
  ];
  const strokes = [S(outline, { amp: opt.amp ?? 1.2, closed: true })];
  const bandY = top + h * 0.25, bandH = Math.max(5, h * 0.034);
  strokes.push(S(sampleLine([-hw, bandY], [hw, bandY]), { amp: 0.6 }));
  strokes.push(S(sampleLine([-hw, bandY + bandH], [hw, bandY + bandH]), { amp: 0.6 }));
  if (w > 40) {
    const n = 4;
    for (let i = 0; i < n; i++) {
      const x0 = -hw + (w / n) * (i + 0.15);
      strokes.push(S(sampleLine([x0, bandY + bandH], [x0 + w / n * 0.6, bandY]), { amp: 0, width: 3 }));
    }
    strokes.push(S(sampleLine([-hw, top + h * 0.83], [hw, top + h * 0.83]), { amp: 0.6 }));
  }
  const nt = hw * 0.62, nb = hw * 0.86;
  strokes.push(S(poly([[-nt, bodyBottom], [-nb, 0], [nb, 0], [nt, bodyBottom]], 5), { amp: 0.5 }));
  return strokes;
}

function flameShape(w) {
  const hw = w * 0.32;
  return [{ pts: smooth([[-hw, 0], [-hw * 0.6, w * 0.45], [0, w * 1.05], [hw * 0.6, w * 0.45], [hw, 0]], false, 8), color: ORANGE, width: Math.max(3, w * 0.08), fill: 'rgba(238,114,41,0.35)' }];
}

// Earth: circle + two continents
function earthShape(cx, cy, r, opt = {}) {
  const circle = ellipsePts(cx, cy, r, r, 0, -Math.PI * 0.75, Math.PI * 1.25);
  const k = r;
  const big = [[-0.58, -0.28], [-0.42, -0.5], [-0.18, -0.46], [-0.02, -0.6], [0.24, -0.5], [0.3, -0.3], [0.12, -0.2], [0.18, 0.02], [-0.04, 0.02], [-0.16, -0.1], [-0.38, -0.06], [-0.52, -0.12]]
    .map(([x, y]) => [cx + x * k, cy + y * k]);
  const small = [[-0.02, 0.36], [0.22, 0.24], [0.48, 0.36], [0.42, 0.56], [0.2, 0.6], [0.04, 0.5]]
    .map(([x, y]) => [cx + x * k, cy + y * k]);
  const w = opt.width || (r < 90 ? 5 : STROKE);
  return [
    S(circle, { amp: r * 0.012, width: w }),
    S(smooth(big, true, 8), { amp: 0.6, closed: true, width: w * 0.8 }),
    S(smooth(small, true, 8), { amp: 0.6, closed: true, width: w * 0.8 }),
  ];
}

function orbitShape(cx, cy, rx, ry, rot, opt = {}) {
  return [S(ellipsePts(cx, cy, rx, ry, rot, Math.PI, Math.PI * 3), { amp: 0.8, color: ORANGE, width: opt.width || 4, dash: opt.solid ? null : (opt.dash || '13 10') })];
}

function explosionShape(cx, cy, R) {
  const out = [], spikes = 11, rr = rng(Math.round(cx * 7 + cy));
  for (let i = 0; i <= spikes * 2; i++) {
    const a = (i / (spikes * 2)) * Math.PI * 2 - Math.PI / 2;
    const r = i % 2 === 0 ? R * (0.88 + rr() * 0.22) : R * (0.45 + rr() * 0.08);
    out.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
  }
  out[out.length - 1] = out[0];
  const inner = [];
  for (let i = 0; i <= 16; i++) {
    const a = (i / 16) * Math.PI * 2 - Math.PI / 2 + 0.2;
    const r = i % 2 === 0 ? R * 0.42 : R * 0.22;
    inner.push([cx + Math.cos(a) * r, cy + Math.sin(a) * r]);
  }
  inner[inner.length - 1] = inner[0];
  const rays = [205, 245, 300, 335].map(d => {
    const a = (d * Math.PI) / 180;
    return S(sampleLine([cx + Math.cos(a) * R * 1.12, cy - Math.sin(a) * R * 1.12], [cx + Math.cos(a) * R * 1.38, cy - Math.sin(a) * R * 1.38]), { amp: 0, width: 5 });
  });
  return [S(out, { amp: 0.5, closed: true, width: 5 }), S(inner, { amp: 0.3, closed: true, color: ORANGE, width: 4.5 }), ...rays];
}

// stick figure: head centre (hx,hy) radius r
function stickShape(hx, hy, r, pose = 'neutral') {
  const sh = [hx, hy + r * 1.75], hip = [hx, hy + r * 4.4];
  const legL = [hx - r * 1.35, hy + r * 7.9], legR = [hx + r * 1.35, hy + r * 7.9];
  const st = [
    S(ellipsePts(hx, hy, r, r, 0, -Math.PI / 2, Math.PI * 1.5), { amp: 0.4, width: 5 }),
    S(sampleLine([hx, hy + r], hip), { amp: 0.6, width: 5 }),
    S(poly([legL, hip, legR]), { amp: 0.6, width: 5 }),
  ];
  if (pose === 'neutral') st.push(S(poly([[hx - r * 1.3, hy + r * 3.6], sh, [hx + r * 1.3, hy + r * 3.6]]), { amp: 0.5, width: 5 }));
  if (pose === 'wave') {
    st.push(S(poly([[hx + r * 1.9, hy - r * 0.7], [hx + r * 1.55, hy + r * 0.9], sh]), { amp: 0.5, width: 5 }));
    st.push(S(poly([sh, [hx - r * 0.9, hy + r * 2.4], [hx - r * 1.2, hy + r * 3.6]]), { amp: 0.5, width: 5 }));
  }
  if (pose === 'despair') {
    st.push(S(poly([[hx - r * 0.75, hy - r * 0.55], [hx - r * 1.45, hy + r * 0.6], sh, [hx + r * 1.45, hy + r * 0.6], [hx + r * 0.75, hy - r * 0.55]]), { amp: 0.5, width: 5 }));
  }
  return st;
}

function moneyBagShape(cx, cy, s) {
  const nL = [cx - s * 0.16, cy - s * 0.3], nR = [cx + s * 0.16, cy - s * 0.3];
  const body = smooth([nL, [cx - s * 0.36, cy - s * 0.12], [cx - s * 0.5, cy + s * 0.18], [cx - s * 0.36, cy + s * 0.42], [cx, cy + s * 0.47], [cx + s * 0.36, cy + s * 0.42], [cx + s * 0.5, cy + s * 0.18], [cx + s * 0.36, cy - s * 0.12], nR], false, 10);
  const top = smooth([nL, [cx - s * 0.32, cy - s * 0.48], [cx - s * 0.12, cy - s * 0.43], [cx, cy - s * 0.5], [cx + s * 0.12, cy - s * 0.43], [cx + s * 0.32, cy - s * 0.48], nR], false, 8);
  return [S(body, { amp: 1 }), S(top, { amp: 0.6 }), S(sampleLine([cx - s * 0.2, cy - s * 0.31], [cx + s * 0.2, cy - s * 0.31]), { amp: 0.4, width: 5 })];
}

function arrowShape(a, b, opt = {}) {
  const ang = Math.atan2(b[1] - a[1], b[0] - a[0]), hl = opt.head || 22;
  const line = opt.curve ? smooth([a, opt.curve, b], false, 20) : sampleLine(a, b);
  const h1 = [b[0] - hl * Math.cos(ang - 0.45), b[1] - hl * Math.sin(ang - 0.45)];
  const h2 = [b[0] - hl * Math.cos(ang + 0.45), b[1] - hl * Math.sin(ang + 0.45)];
  return [S(line, { amp: 0.8, color: opt.color, width: opt.width }), S(poly([h1, b, h2]), { amp: 0, color: opt.color, width: opt.width })];
}

function marsShape(cx, cy, r) {
  const st = [S(ellipsePts(cx, cy, r, r, 0, -Math.PI * 0.6, Math.PI * 1.4), { amp: 1, width: 5 })];
  const cid = 'marsclip' + Math.round(cx);
  const cp = el('clipPath', { id: cid }, board.defs);
  el('circle', { cx, cy, r: r - 3 }, cp);
  for (let k = -r * 2; k <= r * 2; k += r / 6.2) {
    st.push({ pts: sampleLine([cx + k - r, cy + r], [cx + k + r, cy - r], 20), color: ORANGE, width: 4, clip: cid });
  }
  return st;
}
function houseShape(cx, by, s) {
  return [
    S(poly([[cx - s * 0.32, by], [cx - s * 0.32, by - s * 0.55], [cx + s * 0.32, by - s * 0.55], [cx + s * 0.32, by]]), { amp: 0.3, width: 4.5 }),
    S(poly([[cx - s * 0.45, by - s * 0.5], [cx, by - s * 0.95], [cx + s * 0.45, by - s * 0.5]]), { amp: 0.3, width: 4.5 }),
  ];
}
function checkShape(x, y, s) {
  return [S(poly([[x, y], [x + s * 0.32, y + s * 0.32], [x + s, y - s * 0.55]], 4), { amp: 0.5, color: ORANGE, width: 7 })];
}
function underline(a, b, opt = {}) {
  return [S(smooth([a, [lerp(a[0], b[0], 0.5), lerp(a[1], b[1], 0.5) + (opt.bow || 3)], b], false, 20), { amp: opt.amp ?? 1.2, color: opt.color || ORANGE, width: opt.width || 5 })];
}
