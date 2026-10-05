// Whiteboard animation engine: deterministic renderAt(t) for frame-by-frame capture.
const NS = 'http://www.w3.org/2000/svg';
const W = 1920, H = 1080;
const INK = '#080505', ORANGE = '#EE7229';
const STROKE = 6;

function el(tag, attrs, parent) {
  const e = document.createElementNS(NS, tag);
  for (const k in attrs) e.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(e);
  return e;
}
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, u) => a + (b - a) * u;
const ease = u => (u < 0.5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2);
const easeSine = u => -(Math.cos(Math.PI * u) - 1) / 2;
const easeOut = u => 1 - Math.pow(1 - u, 2);

// ---------- deterministic noise ----------
function rng(seed) {
  let s = (seed * 2654435761) >>> 0 || 1;
  return () => { s ^= s << 13; s >>>= 0; s ^= s >> 17; s ^= s << 5; s >>>= 0; return s / 4294967296; };
}
function noise1(seed) {
  const r = rng(seed), v = Array.from({ length: 97 }, () => r() * 2 - 1);
  return x => {
    const i = Math.floor(x), f = x - i, n = v.length;
    const a = v[((i % n) + n) % n], b = v[(((i + 1) % n) + n) % n];
    const u = f * f * (3 - 2 * f);
    return a + (b - a) * u;
  };
}
let SEED = 7;

// ---------- geometry sampling ----------
function sampleLine(a, b, step = 6) {
  const n = Math.max(2, Math.ceil(Math.hypot(b[0] - a[0], b[1] - a[1]) / step));
  return Array.from({ length: n + 1 }, (_, i) => [lerp(a[0], b[0], i / n), lerp(a[1], b[1], i / n)]);
}
function poly(points, step) {
  let out = [];
  for (let i = 0; i < points.length - 1; i++) {
    const s = sampleLine(points[i], points[i + 1], step);
    out = out.concat(i ? s.slice(1) : s);
  }
  return out;
}
function bez(p0, p1, p2, p3, n = 40) {
  return Array.from({ length: n + 1 }, (_, i) => {
    const t = i / n, m = 1 - t;
    return [m * m * m * p0[0] + 3 * m * m * t * p1[0] + 3 * m * t * t * p2[0] + t * t * t * p3[0],
            m * m * m * p0[1] + 3 * m * m * t * p1[1] + 3 * m * t * t * p2[1] + t * t * t * p3[1]];
  });
}
function ellipsePts(cx, cy, rx, ry, rotDeg = 0, a0 = 0, a1 = Math.PI * 2, n) {
  n = n || Math.max(24, Math.ceil((Math.abs(a1 - a0) * Math.max(rx, ry)) / 6));
  const r = (rotDeg * Math.PI) / 180, c = Math.cos(r), s = Math.sin(r);
  return Array.from({ length: n + 1 }, (_, i) => {
    const a = lerp(a0, a1, i / n), x = rx * Math.cos(a), y = ry * Math.sin(a);
    return [cx + x * c - y * s, cy + x * s + y * c];
  });
}
// Catmull-Rom through points
function smooth(points, closed = false, per = 12) {
  const P = closed ? [points[points.length - 1], ...points, points[0], points[1]]
                   : [points[0], ...points, points[points.length - 1]];
  const out = [];
  for (let i = 1; i < P.length - 2; i++) {
    const [p0, p1, p2, p3] = [P[i - 1], P[i], P[i + 1], P[i + 2]];
    for (let j = 0; j < per; j++) {
      const t = j / per, t2 = t * t, t3 = t2 * t;
      out.push([0, 1].map(k => 0.5 * (2 * p1[k] + (-p0[k] + p2[k]) * t + (2 * p0[k] - 5 * p1[k] + 4 * p2[k] - p3[k]) * t2 + (-p0[k] + 3 * p1[k] - 3 * p2[k] + p3[k]) * t3)));
    }
  }
  out.push(closed ? points[0] : points[points.length - 1]);
  return out;
}
// hand-drawn wobble: offset along normal with smooth noise
function wobble(pts, amp = 1.4, wl = 110) {
  if (amp <= 0 || pts.length < 3) return pts;
  const nz = noise1(SEED++);
  let acc = 0;
  return pts.map((p, i) => {
    if (i) acc += Math.hypot(p[0] - pts[i - 1][0], p[1] - pts[i - 1][1]);
    const a = pts[Math.max(0, i - 1)], b = pts[Math.min(pts.length - 1, i + 1)];
    let nx = -(b[1] - a[1]), ny = b[0] - a[0];
    const l = Math.hypot(nx, ny) || 1;
    const o = nz(acc / wl) * amp;
    return [p[0] + (nx / l) * o, p[1] + (ny / l) * o];
  });
}
const toD = (pts, closed) => 'M' + pts.map(p => p[0].toFixed(1) + ',' + p[1].toFixed(1)).join('L') + (closed ? 'Z' : '');
const S = (pts, opt = {}) => ({ pts: opt.raw ? pts : wobble(pts, opt.amp ?? 1.4), ...opt });

// ---------- world ----------
class Board {
  constructor(svg) {
    this.svg = svg;
    this.defs = el('defs', {}, svg);
    this.world = el('g', { id: 'world' }, this.defs);
    this.views = [];
    this.items = [];       // all animated items
    this.segs = [];        // pen segments for pencil tracking
    this.cams = [];
    this.uid = 0;
    this.blurN = 10;
    for (let i = 0; i < this.blurN; i++) this.views.push(el('use', { href: '#world' }, svg));
  }
  id(p) { return p + (this.uid++); }

  // strokes: [{pts, closed, color, width, dash}], drawn sequentially within [t0,t1]
  draw(t0, t1, strokes, opt = {}) {
    const g = el('g', {}, opt.parent || this.world);
    const item = { kind: 'draw', t0, t1, g, parts: [], xf: opt.xf, vis: opt.vis };
    const lens = [];
    for (const s of strokes) {
      const color = s.color || opt.color || INK;
      const width = s.width || opt.width || STROKE;
      const dash = s.dash || opt.dash;
      const d = toD(s.pts, s.closed);
      const p = el('path', { d, fill: 'none', stroke: color, 'stroke-width': width, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' }, g);
      if (s.clip) p.setAttribute('clip-path', `url(#${s.clip})`);
      const L = p.getTotalLength();
      let mp = null;
      if (dash) {
        p.setAttribute('stroke-dasharray', dash);
        p.setAttribute('stroke-linecap', 'butt');
        const mid = this.id('m');
        const m = el('mask', { id: mid, maskUnits: 'userSpaceOnUse', x: -1e5, y: -1e5, width: 2e5, height: 2e5 }, g);
        mp = el('path', { d, fill: 'none', stroke: '#fff', 'stroke-width': width + 8, 'stroke-linecap': 'round', 'stroke-dasharray': `${L + 1} ${L + 1}` }, m);
        p.setAttribute('mask', `url(#${mid})`);
      } else {
        p.setAttribute('stroke-dasharray', `${L + 1} ${L + 1}`);
      }
      item.parts.push({ p, mp, L, color, pts: s.pts, instant: s.instant });
      lens.push(s.instant ? 0 : L + 40);
    }
    // time allocation proportional to length
    const total = lens.reduce((a, b) => a + b, 0) || 1;
    let acc = 0;
    item.parts.forEach((pt, i) => {
      pt.a = lerp(t0, t1, acc / total); acc += lens[i];
      pt.b = lerp(t0, t1, (acc - (lens[i] ? 40 : 0)) / total);
      if (!pt.instant && opt.pen !== false) this.segs.push({ a: pt.a, b: pt.b, color: pt.color, at: u => pt.p.getPointAtLength(u * pt.L), item });
    });
    this.items.push(item);
    return item;
  }

  // text written char by char. runs: string or [[str,color],...]
  text(t0, t1, runs, x, cy, size, opt = {}) {
    if (typeof runs === 'string') runs = [[runs, opt.color || INK]];
    const g = el('g', {}, opt.parent || this.world);
    const item = { kind: 'text', t0, t1, g, chars: [], xf: opt.xf, vis: opt.vis };
    const family = opt.family || "KleeLatin, Xiaolai";
    const weight = opt.weight || 600;
    let cx = x;
    const all = [];
    for (const [str, color] of runs) for (const ch of str) all.push([ch, color]);
    for (const [ch, color] of all) {
      const cid = this.id('c');
      const cp = el('clipPath', { id: cid }, g);
      const r = el('rect', { x: cx - 4, y: cy - size, width: 0, height: size * 2 }, cp);
      const tx = el('text', { x: cx, y: cy, 'font-family': family, 'font-weight': weight, 'font-size': size, fill: color, 'dominant-baseline': 'central', 'clip-path': `url(#${cid})` }, g);
      const sw = opt.stroke ?? (/[\x00-\x7f]/.test(ch) ? size * 0.01 : size * 0.022);
      if (sw) { tx.setAttribute('stroke', color); tx.setAttribute('stroke-width', sw); tx.setAttribute('stroke-linejoin', 'round'); }
      tx.textContent = ch;
      const w = ch === ' ' ? size * 0.3 : tx.getComputedTextLength();
      item.chars.push({ r, x: cx, w, color, ch });
      cx += w + (opt.spacing || 0);
    }
    item.width = cx - x;
    const weights = item.chars.map(c => (c.ch === ' ' ? 0.15 : /[\x00-\x7f]/.test(c.ch) ? 0.6 : 1));
    const total = weights.reduce((a, b) => a + b, 0);
    let acc = 0;
    item.chars.forEach((c, i) => {
      c.a = lerp(t0, t1, acc / total); acc += weights[i]; c.b = lerp(t0, t1, acc / total);
      if (c.ch === ' ') return;
      const seed = i * 1.7;
      this.segs.push({ a: c.a, b: c.b, color: c.color, item, at: u => ({ x: c.x + c.w * (0.1 + 0.85 * u), y: cy + size * 0.28 * Math.sin((u * 2.6 + seed) * Math.PI) + size * 0.05 }) });
    });
    this.items.push(item);
    return item;
  }

  // instant shape (no drawing) visible according to vis(t)
  shape(strokes, opt = {}) {
    const g = el('g', {}, opt.parent || this.world);
    for (const s of strokes) {
      const a = { d: toD(s.pts, s.closed), fill: s.fill || 'none', stroke: s.color || opt.color || INK, 'stroke-width': s.width || STROKE, 'stroke-linecap': 'round', 'stroke-linejoin': 'round' };
      if (s.dash) a['stroke-dasharray'] = s.dash;
      el('path', a, g);
    }
    const item = { kind: 'shape', g, xf: opt.xf, vis: opt.vis };
    this.items.push(item);
    return item;
  }

  group(opt = {}) {
    const g = el('g', {}, this.world);
    const item = { kind: 'group', g, xf: opt.xf, vis: opt.vis };
    this.items.push(item);
    return g;
  }

  camera(keys) { this.cams = keys; }
  camAt(t) {
    const K = this.cams;
    if (t <= K[0].t) return K[0];
    for (let i = 0; i < K.length - 1; i++) {
      const a = K[i], b = K[i + 1];
      if (t < b.t) {
        if (!b.move) return a;              // hold
        const m0 = b.t - b.move;
        if (t < m0) return a;
        const u = (b.ease || ease)((t - m0) / b.move);
        // zoom in log space; interpolate the focus so the path looks natural
        const s = Math.exp(lerp(Math.log(a.s), Math.log(b.s), u));
        return { x: lerp(a.x, b.x, u), y: lerp(a.y, b.y, u), s, blur: !!b.blur };
      }
    }
    return K[K.length - 1];
  }
  project(c, p) { return [(p[0] - c.x) * c.s + W / 2, (p[1] - c.y) * c.s + H / 2]; }
  camXf(c) { return `translate(${W / 2},${H / 2}) scale(${c.s}) translate(${-c.x},${-c.y})`; }

  xfOf(item, t) {
    if (!item.xf) return null;
    return item.xf(t);
  }
  applyXf(xf, p) {
    if (!xf) return p;
    const r = ((xf.rot || 0) * Math.PI) / 180, s = xf.s ?? 1;
    const x = p[0] * s, y = p[1] * s;
    return [xf.x + x * Math.cos(r) - y * Math.sin(r), xf.y + x * Math.sin(r) + y * Math.cos(r)];
  }

  render(t) {
    for (const it of this.items) {
      const visible = it.vis ? it.vis(t) : true;
      it.g.style.display = visible ? '' : 'none';
      if (!visible) continue;
      const xf = this.xfOf(it, t);
      if (xf) it.g.setAttribute('transform', `translate(${xf.x},${xf.y}) rotate(${xf.rot || 0}) scale(${xf.s ?? 1})`);
      if (it.kind === 'draw') {
        for (const pt of it.parts) {
          const u = pt.instant ? (t >= pt.a ? 1 : 0) : clamp((t - pt.a) / (pt.b - pt.a || 1e-6));
          const off = (pt.L + 1) * (1 - u);
          (pt.mp || pt.p).setAttribute('stroke-dashoffset', off);
          pt.p.style.visibility = u <= 0 ? 'hidden' : '';
        }
      } else if (it.kind === 'text') {
        for (const c of it.chars) {
          const u = clamp((t - c.a) / (c.b - c.a));
          c.r.setAttribute('width', u >= 1 ? c.w + 40 : (c.w + 8) * u);
        }
      }
    }
    // camera with optional motion blur (accumulated sub-frames)
    const c = this.camAt(t);
    const dt = 1 / 30, c2 = this.camAt(t + dt);
    const speed = Math.hypot((c2.x - c.x) * c.s, (c2.y - c.y) * c.s) + Math.abs(Math.log(c2.s / c.s)) * 1500;
    const n = c.blur && speed > 40 ? this.blurN : 1;
    this.views.forEach((v, i) => {
      if (i >= n) { v.style.display = 'none'; return; }
      v.style.display = '';
      const ci = n === 1 ? c : this.camAt(t + (dt * 1.6 * i) / (n - 1) - dt * 0.8);
      v.setAttribute('transform', this.camXf(ci));
      v.setAttribute('opacity', n === 1 ? 1 : 1.6 / n);
    });
    this.cur = c;
    return c;
  }

  // pencil tip location (screen) + ink color, or null when pencil away
  pencil(t, c) {
    const segs = this.segs;
    const pt = (s, u) => {
      const p = s.at(u);
      const xf = this.xfOf(s.item, t);
      return this.project(c, this.applyXf(xf, [p.x, p.y]));
    };
    let prev = null, next = null;
    for (const s of segs) {
      if (t >= s.a && t <= s.b) return { p: pt(s, (t - s.a) / (s.b - s.a || 1)), color: s.color, drawing: true };
      if (s.b < t && (!prev || s.b > prev.b)) prev = s;
      if (s.a > t && (!next || s.a < next.a)) next = s;
    }
    const OFF = [W + 260, H + 300];
    const LEAVE = 0.4;
    if (prev && next && next.a - prev.b <= 0.75) {
      const u = easeSine((t - prev.b) / (next.a - prev.b));
      const a = pt(prev, 1), b = pt(next, 0);
      // small hop while travelling
      return { p: [lerp(a[0], b[0], u), lerp(a[1], b[1], u) - Math.sin(u * Math.PI) * 14], color: next.color };
    }
    if (prev && t - prev.b < LEAVE) {
      const u = ease((t - prev.b) / LEAVE), a = pt(prev, 1);
      return { p: [lerp(a[0], OFF[0], u), lerp(a[1], OFF[1], u)], color: prev.color };
    }
    if (next && next.a - t < LEAVE) {
      const u = ease(1 - (next.a - t) / LEAVE), b = pt(next, 0);
      return { p: [lerp(OFF[0], b[0], u), lerp(OFF[1], b[1], u)], color: next.color };
    }
    return null;
  }
}
