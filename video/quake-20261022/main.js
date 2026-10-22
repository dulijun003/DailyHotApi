// Caption News (字幕新闻) ·《巴青 7.0 级地震，60 秒讲清楚》— vertical 1080×1920, 30 fps
// One timeline (timeline.json: shots, captions, voice starts) drives the picture, the .srt and the mix.
// Material: NASA Terra imagery of the day (GIBS), USGS ShakeMap (public domain), NASA Black Marble and ISS imagery,
// the facts re-set from the official reports (FACTS.md).
const W = 1080, H = 1920, FPS = 30;
const cv = document.getElementById('out'), ctx = cv.getContext('2d');

// ---------- helpers ----------
const clamp = (x, a = 0, b = 1) => Math.max(a, Math.min(b, x));
const lerp = (a, b, t) => a + (b - a) * t;
const seg = (t, a, b) => clamp((t - a) / (b - a));
const eo = t => 1 - Math.pow(1 - clamp(t), 3);
const ei = t => Math.pow(clamp(t), 3);
const eio = t => { t = clamp(t); return t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2; };
const back = (t, s = 1.8) => { t = clamp(t) - 1; return 1 + t * t * ((s + 1) * t + s); };
const fmt = n => Math.round(n).toLocaleString('en-US');
const pop = (t, t0, d = .13) => lerp(1.3, 1, back(seg(t, t0, t0 + d), 1.6));

// ---------- palette, type, layout ----------
const C = { bg: '#0E0E0C', panel: '#151512', ink: '#F7F5EF', honey: '#FFC21A', loss: '#FF4A3D', grey: '#8D8B83', mute: '#5E5C55', rule: 'rgba(255,255,255,.045)', margin: 'rgba(255,74,61,.38)', dim: 'rgba(247,245,239,.74)', paper: '#F3F0E8', pink: '#141412' };
const F = { zh9: "'SC'", zh5: "'SC'", n8: "'IT','SC'", n5: "'IT','SC'" };
const BAND = 1560;                                                   // footage band (top); captions live under it
const CAP = { x: 72, y1: 1676, y2: 1782, zh: 88, enY: 1862, en: 33 }; // two stacked chunks + one English line
const GRADE = 'contrast(1.07) saturate(0.92) brightness(0.98)';
const SNAP = '10.23 01:34';                                          // information as of, Beijing

let TL = null, SHOTS = [], CAPS = [];
const shotAt = t => SHOTS.find(s => t >= s.a && t < s.b) || SHOTS[SHOTS.length - 1];

// ---------- loading (sync draw with placeholders, then load and draw again) ----------
const LOADED = new Map(), NEED = new Set(), PH = { width: 1080, height: 1560, ph: true };
function getImg(src) { const im = LOADED.get(src); if (im) return im; NEED.add(src); return PH; }
function load(src) {
  return new Promise((res, rej) => { const im = new Image(); im.onload = () => im.decode().then(() => res(im), () => res(im)); im.onerror = () => rej(new Error('missing ' + src)); im.src = src; })
    .then(im => { LOADED.set(src, im); if (src.startsWith('assets/fr') && LOADED.size > 60) { for (const k of LOADED.keys()) if (k.startsWith('assets/fr')) { LOADED.delete(k); break; } } });
}
const frame = (fr, n, t, a) => getImg(`assets/fr/${fr}_${String(clamp(Math.floor((t - a) * FPS + 1e-6) + 1, 1, n)).padStart(3, '0')}.jpg`);
function di(im, ...a) { if (!im.ph) ctx.drawImage(im, ...a); }

// ---------- drawing basics ----------
function text(s, x, y, font, color, align = 'left', base = 'alphabetic') { ctx.font = font; ctx.fillStyle = color; ctx.textAlign = align; ctx.textBaseline = base; ctx.fillText(s, x, y); }
const TWC = new Map();
function tw(s, font) { const k = font + '|' + s; let w = TWC.get(k); if (w == null) { ctx.font = font; w = ctx.measureText(s).width; TWC.set(k, w); } return w; }
function warm(x, y, w, h, a = .06) { ctx.save(); ctx.globalCompositeOperation = 'soft-light'; ctx.fillStyle = `rgba(255,170,70,${a})`; ctx.fillRect(x, y, w, h); ctx.restore(); }
// a prepared frame (already at display size) in a box, pushed by z around (fx, fy) in box fractions
function plate(im, x, y, w, h, z = 1, fx = .5, fy = .5, filt = GRADE) {
  ctx.save(); ctx.beginPath(); ctx.rect(x, y, w, h); ctx.clip();
  const ox = x + (w - im.width) / 2, oy = y + (h - im.height) / 2, px = x + w * fx, py = y + h * fy;
  ctx.filter = filt; di(im, px + (ox - px) * z, py + (oy - py) * z, im.width * z, im.height * z); ctx.filter = 'none';
  warm(x, y, w, h); ctx.restore();
}
function shade() {   // bottom gradient under the captions, top gradient under the bug and credit
  const g = ctx.createLinearGradient(0, 1180, 0, H); g.addColorStop(0, 'rgba(14,14,12,0)'); g.addColorStop(.42, 'rgba(14,14,12,.78)'); g.addColorStop(1, 'rgba(14,14,12,.96)');
  ctx.fillStyle = g; ctx.fillRect(0, 1180, W, H - 1180);
  const r = ctx.createRadialGradient(0, H, 0, 0, H, 900); r.addColorStop(0, 'rgba(14,14,12,.45)'); r.addColorStop(1, 'rgba(14,14,12,0)'); ctx.fillStyle = r; ctx.fillRect(0, 900, W, H - 900);
  const t = ctx.createLinearGradient(0, 0, 0, 260); t.addColorStop(0, 'rgba(14,14,12,.55)'); t.addColorStop(1, 'rgba(14,14,12,0)'); ctx.fillStyle = t; ctx.fillRect(0, 0, W, 260);
}
function flash(t, t0, dur = .12) { const k = seg(t, t0, t0 + dur); if (k <= 0 || k >= 1) return; ctx.fillStyle = `rgba(255,255,255,${(1 - k) * .9})`; ctx.fillRect(0, 0, W, H); }
// ledger paper: the data-card ground — dark ruled sheet, red double margin; slides in from the right with speed streaks
function ledger(t, a, slide = true) {
  const k = slide ? eo(seg(t, a - .04, a + .18)) : 1, ox = (1 - k) * 120;
  ctx.fillStyle = C.panel; ctx.fillRect(0, 0, W, H);
  ctx.save(); ctx.translate(ox, 0); ctx.strokeStyle = C.rule; ctx.lineWidth = 2;
  for (let y = 216; y < H; y += 54) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke(); }
  ctx.strokeStyle = C.margin; [40, 48].forEach(x => { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke(); });
  ctx.restore();
  if (slide && k < 1) { ctx.fillStyle = `rgba(255,194,26,${(1 - k) * .5})`; for (let i = 0; i < 7; i++) ctx.fillRect(W - (1 - k) * 700 - i * 90, 260 + i * 190, 480 * (1 - k), 3); }
}
function camPush(t, a, b, z0, z1, cx = W / 2, cy = 800) { const z = lerp(z0, z1, eio(seg(t, a, b))); ctx.translate(cx, cy); ctx.scale(z, z); ctx.translate(-cx, -cy); }
// numbers with fixed-width digits, so a rolling counter never jitters
function num(s, x, y, size, color, align = 'left', w8 = 800) {
  const f = `${w8} ${size}px ${F.n8}`; const cw = tw('0', f);
  const wOf = ch => /[0-9]/.test(ch) ? cw : tw(ch, f);
  let total = 0; for (const ch of s) total += wOf(ch);
  let cx = align === 'right' ? x - total : align === 'center' ? x - total / 2 : x;
  ctx.font = f; ctx.fillStyle = color; ctx.textBaseline = 'alphabetic';
  for (const ch of s) { const w = wOf(ch); ctx.textAlign = 'center'; ctx.fillText(ch, cx + w / 2, y); cx += w; }
  return total;
}
const wan = v => (v / 1e4).toFixed(0) + '万';
function bug(t) {   // channel bug (fictional channel 热榜60秒), top-left safe area, from frame 1
  const k = eo(seg(t, 0, .2)); const x = 60, y = 84;
  ctx.save(); ctx.globalAlpha = k;
  const w1 = tw('热榜60秒', `900 30px ${F.zh9}`) + 28;
  ctx.fillStyle = C.honey; ctx.fillRect(x, y, w1, 48); text('热榜60秒', x + 14, y + 35, `900 30px ${F.zh9}`, C.bg);
  const lab = 'HOT 60 · 10.22', w2 = tw(lab, `800 19px ${F.n8}`) + 28;
  ctx.fillStyle = 'rgba(14,14,12,.66)'; ctx.fillRect(x + w1, y, w2, 48); text(lab, x + w1 + 14, y + 32, `800 19px ${F.n8}`, C.honey);
  ctx.restore();
  TX.push({ id: 'bug', text: '热榜60秒', x0: x, y0: y, x1: x + w1 + w2, y1: y + 48 });
}
function sourceTag(t, t0, label) {   // source tag: slides in under the bug
  const k = eo(seg(t, t0, t0 + .2)); if (k <= 0) return; ctx.save(); ctx.globalAlpha = k; const x = 60 - (1 - k) * 40, y = 144;
  const w1 = tw('来源', `900 22px ${F.zh9}`) + 20, w2 = tw(label, `500 21px ${F.n5}`) + 22;
  ctx.fillStyle = C.ink; ctx.fillRect(x, y, w1, 36); text('来源', x + 10, y + 26, `900 22px ${F.zh9}`, C.bg);
  ctx.fillStyle = 'rgba(14,14,12,.82)'; ctx.fillRect(x + w1, y, w2, 36); text(label, x + w1 + 11, y + 25, `500 21px ${F.n5}`, C.ink); ctx.restore();
}
function credit(s) {   // per-shot material credit, top right
  if (!s) return; const f = `500 19px ${F.zh5}`; const w = tw(s, f);
  ctx.fillStyle = 'rgba(14,14,12,.5)'; ctx.fillRect(W - 44 - w - 16, 92, w + 16, 30); text(s, W - 52, 113, f, 'rgba(247,245,239,.86)', 'right');
}
function chip(x, y, zh, col = C.honey, size = 30, fg = C.bg) {   // a small label block; returns its width
  const f = `900 ${size}px ${F.zh9}`, w = tw(zh, f) + size * .9;
  ctx.fillStyle = col; ctx.fillRect(x, y - size * 1.05, w, size * 1.45); text(zh, x + size * .45, y, f, fg); return w;
}
function stamp(t, t0, x, y, zh, rot = -.06, size = 64) {   // stamp thump: a ruled box that slams in
  if (t < t0) return; const k = seg(t, t0, t0 + .14), sc = lerp(1.6, 1, back(k, 1.3));
  ctx.save(); ctx.translate(x, y); ctx.rotate(rot); ctx.scale(sc, sc); ctx.globalAlpha = clamp(k * 3);
  const f = `900 ${size}px ${F.zh9}`, w = tw(zh, f) + 60;
  ctx.fillStyle = C.honey; ctx.fillRect(-w / 2, -size * .95, w, size * 1.35); ctx.strokeStyle = C.bg; ctx.lineWidth = 4; ctx.strokeRect(-w / 2 + 10, -size * .95 + 10, w - 20, size * 1.35 - 20);
  text(zh, 0, size * .2, f, C.bg, 'center'); ctx.restore();
  TX.push({ id: 'stamp' + t0, text: zh, x0: x - w / 2, y0: y - size, x1: x + w / 2, y1: y + size * .5 });
}

// ---------- caption card: two chunks stacked, slammed in one after another, one keyword in a honey block ----------
function capCard(c, t) {
  const [a, b, zh, en, big = 1] = c; if (t < a || t >= b) return;
  const size = CAP.zh * big, parts = zh.split('|');
  parts.forEach((p, i) => {
    const t0 = a + .04 + i * .12, k = seg(t, t0, t0 + .13); if (t < t0) return;
    const y = (i === 0 ? CAP.y1 : CAP.y2) + (big > 1 ? (i === 0 ? -30 : 0) : 0) + (big > 1 && i === 1 ? 10 : 0);
    const sc = lerp(1.3, 1, back(k, 1.6));
    ctx.save(); ctx.translate(CAP.x, y); ctx.scale(sc, sc); ctx.globalAlpha = clamp(k * 3);
    let x = 0;
    for (const q of p.split(/(\{[^}]+\})/).filter(Boolean)) {
      const hot = q[0] === '{', s = hot ? q.slice(1, -1) : q, f = `900 ${size}px ${F.zh9}`, w = tw(s, f);
      if (hot) { const wk = eo(seg(t, t0 + .05, t0 + .17)); ctx.fillStyle = C.honey; ctx.fillRect(x - 12, -size * .9, (w + 24) * wk, size * 1.1); }
      else { ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; ctx.shadowOffsetY = 4; }
      text(s, x, 0, f, hot ? C.bg : C.ink); ctx.shadowColor = 'transparent'; x += w + (hot ? 24 : 0);
    }
    ctx.restore();
  });
  const ke = eo(seg(t, a + .1, a + .28));
  ctx.save(); ctx.globalAlpha = ke; ctx.shadowColor = 'rgba(0,0,0,.7)'; ctx.shadowBlur = 12;
  text(en, CAP.x, CAP.enY + (big > 1 ? 12 : 0) + (1 - ke) * 10, `500 ${CAP.en}px ${F.n5}`, C.ink); ctx.restore();
}

// ---------- the hot-list entry as a document: paper card, wrapped text, highlighter driven by substrings ----------
function wrap(s, font, maxW) {   // CJK breaks per character, Latin words stay whole; returns [{s, i0}]
  const out = []; let line = '', i0 = 0, w = 0;
  const toks = s.match(/[A-Za-z0-9.]+ ?|./gu) || [];
  let i = 0;
  for (const tok of toks) {
    const cw = tw(tok, font);
    if (w + cw > maxW && line) { out.push({ s: line, i0 }); line = ''; w = 0; i0 = i; }
    line += tok; w += cw; i += tok.length;
  }
  if (line) out.push({ s: line, i0 }); return out;
}
// spec: {list, rank, title, desc, meta, marks: [[t0, dur, field, substring]]}; drawn at the card's local origin, width CW
const CW = 900;
function docCard(t, sp) {
  const P = 48, inner = CW - 2 * P; let y = 0;
  const tf = `900 60px ${F.zh9}`, df = `500 34px ${F.zh5}`;
  const TX0 = sp.rank ? 110 : 0;
  const tl = wrap(sp.title, tf, inner - TX0), dl = sp.desc ? wrap(sp.desc, df, inner) : [];
  const h = 140 + tl.length * 78 + (dl.length ? 30 + dl.length * 50 : 0) + 110;
  ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 50; ctx.shadowOffsetY = 18;
  ctx.fillStyle = C.paper; ctx.fillRect(0, 0, CW, h); ctx.shadowColor = 'transparent';
  // header: list name + type, snapshot time
  ctx.fillStyle = '#E4E0D5'; ctx.fillRect(0, 0, CW, 92);
  text(sp.list.name, P, 60, `900 36px ${F.zh9}`, C.pink); text(sp.list.type, P + tw(sp.list.name, `900 36px ${F.zh9}`) + 18, 58, `500 28px ${F.zh5}`, '#6B685F');
  text(sp.time || SNAP, CW - P, 58, `500 26px ${F.n5}`, '#6B685F', 'right');
  y = 140;
  // rank badge
  if (sp.rank) { ctx.fillStyle = sp.rank === 1 ? '#E2422F' : '#3A3935'; ctx.fillRect(P, y + 4, 84, 84); num(String(sp.rank), P + 42, y + 68, 54, '#fff', 'center'); }
  const mark = (field, lines, font, lh, x0, yTop) => {
    for (const [t0, d, f, sub] of sp.marks || []) {
      if (f !== field) continue; const k = eo(seg(t, t0, t0 + d)); if (k <= 0) continue;
      const src = field === 'title' ? sp.title : sp.desc, a = src.indexOf(sub), b = a + sub.length; if (a < 0) continue;
      // total highlighted width, swept left → right across lines
      const spans = []; let tot = 0;
      lines.forEach((ln, li) => { const s0 = Math.max(a, ln.i0), s1 = Math.min(b, ln.i0 + ln.s.length); if (s1 <= s0) return; const xa = tw(ln.s.slice(0, s0 - ln.i0), font), xb = tw(ln.s.slice(0, s1 - ln.i0), font); spans.push([li, xa, xb]); tot += xb - xa; });
      let left = tot * k;
      for (const [li, xa, xb] of spans) { const ww = Math.min(xb - xa, left); if (ww <= 0) break; ctx.fillStyle = 'rgba(255,200,30,.92)'; ctx.fillRect(x0 + xa - 6, yTop + li * lh - lh * .78, ww + 12, lh * .92); left -= ww; }
    }
  };
  mark('title', tl, tf, 78, P + TX0, y + 70);
  tl.forEach((ln, i) => text(ln.s, P + TX0, y + 70 + i * 78, tf, C.pink));
  y += tl.length * 78 + 30;
  if (dl.length) { mark('desc', dl, df, 50, P, y + 30); dl.forEach((ln, i) => text(ln.s, P, y + 30 + i * 50, df, '#3A3935')); y += dl.length * 50 + 30; }
  ctx.fillStyle = 'rgba(0,0,0,.12)'; ctx.fillRect(P, y + 6, inner, 2);
  if (sp.meta) text(sp.meta, P, y + 62, `500 30px ${F.n5}`, '#6B685F');
  return h;
}
function desk(t, s, sp, z0, z1, fy = .42, rot = -.02) {   // the card on a dark desk, slow push, vignette
  ctx.fillStyle = '#201F1B'; ctx.fillRect(0, 0, W, H);
  const z = lerp(z0, z1, eio(seg(t, s.a, s.b)));
  ctx.save(); ctx.translate(W / 2, BAND * fy); ctx.rotate(rot); ctx.scale(z, z); ctx.translate(-CW / 2, -200);
  const h = docCard(t, sp); ctx.restore();
  warm(0, 0, W, H, .04);
  const v = ctx.createRadialGradient(W / 2, BAND * fy, 300, W / 2, BAND * fy, 1300); v.addColorStop(0, 'rgba(0,0,0,0)'); v.addColorStop(1, 'rgba(0,0,0,.6)'); ctx.fillStyle = v; ctx.fillRect(0, 0, W, H);
  return h;
}

// ---------- geography: plate carrée plates (NASA GIBS, EPSG:4326) under one geo camera ----------
const EPI = [93.79, 32.40];
const PLATES = {
  region: { src: 'assets/img/terra.jpg', lon0: 89.8, lat1: 35.4, ppd: 300 },        // 2400×1800, 2026-10-22 (Terra, daytime)
  detail: { src: 'assets/img/terra_d.jpg', lon0: 92.8, lat1: 33.4, ppd: 800 },      // 1600×1600, same pass
  shake: { src: 'assets/img/shake.png', lon0: 91.5167, lat1: 34.3167, ppd: 1 / 0.0106, ppdy: 1 / 0.009 },   // USGS ShakeMap overlay
};
// camera: centre (lon, lat), z screen px per degree, centred at (sx, sy)
function geoCam(lon, lat, z, sx = W / 2, sy = 760) { return { lon, lat, z, sx, sy, S: (x, y) => [sx + (x - lon) * z, sy - (y - lat) * z] }; }
function drawPlate(cam, p, alpha = 1, filt = GRADE) {
  const im = getImg(p.src); if (im.ph) return;
  const [x0, y0] = cam.S(p.lon0, p.lat1), sx = cam.z / p.ppd, sy = cam.z / (p.ppdy || p.ppd);
  ctx.save(); ctx.globalAlpha = alpha; ctx.filter = filt; ctx.drawImage(im, x0, y0, im.width * sx, im.height * sy); ctx.filter = 'none'; ctx.restore();
}
function ground(cam, grey = 0) {   // region plate always, the detail plate dissolves in as the camera descends
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, BAND); ctx.clip();
  const f = grey ? `${GRADE} saturate(${1 - .8 * grey}) brightness(${1 - .25 * grey})` : GRADE;
  drawPlate(cam, PLATES.region, 1, f);
  const kd = clamp((cam.z - 420) / 260); if (kd > 0) drawPlate(cam, PLATES.detail, kd, f);
  warm(0, 0, W, BAND); ctx.restore();
}
const KM = 1 / 111.32;   // degrees of latitude per km
function ring(cam, km, k, col = C.ink, lw = 3, dash = []) {   // a distance ring, true on the ground (an ellipse in plate carrée)
  if (k <= 0) return; const [x, y] = cam.S(...EPI), ry = km * KM * cam.z, rx = ry / Math.cos(EPI[1] * Math.PI / 180);
  ctx.save(); ctx.strokeStyle = col; ctx.lineWidth = lw; ctx.setLineDash(dash); ctx.shadowColor = 'rgba(0,0,0,.7)'; ctx.shadowBlur = 6;
  ctx.beginPath(); ctx.ellipse(x, y, rx, ry, 0, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * k); ctx.stroke(); ctx.restore();
}
function epicentre(cam, t, t0) {
  const [x, y] = cam.S(...EPI); if (t < t0) return [x, y];
  for (const d of [0, .5, 1.0]) { const pr = seg(t, t0 + d, t0 + d + 1.2); if (pr > 0 && pr < 1) { ctx.strokeStyle = `rgba(255,74,61,${1 - pr})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(x, y, 14 + pr * 200, 0, 7); ctx.stroke(); } }
  ctx.fillStyle = C.loss; ctx.beginPath(); ctx.arc(x, y, 15, 0, 7); ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke(); return [x, y];
}
const gframe = (t, a, rate = 1) => frame('gl', 138, a + (t - a) * rate, a);

// ---------- shots ----------
// 0–5 s: hook — the night over Asia; "7.0" lands on frame 4 and rolls
function shotHook(s, t) {
  plate(gframe(t, s.a), 0, 0, W, BAND, lerp(1.0, 1.06, eio(seg(t, s.a, s.b))), .5, .45);
  shade();
  if (t >= .06) {
    const k1 = seg(t, .06, .19); ctx.save(); ctx.translate(72, 640); ctx.scale(pop(t, .06), pop(t, .06)); ctx.globalAlpha = clamp(k1 * 3);
    ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 20; text('今晚 22:33 · 西藏', 0, 0, `900 64px ${F.zh9}`, C.ink); ctx.restore();
  }
  if (t >= .13) {
    const k = seg(t, .13, .26), v = 7 * eo(seg(t, .13, .58));
    ctx.save(); ctx.translate(72, 960); const sc = lerp(1.45, 1, back(k, 1.4)); ctx.scale(sc, sc); ctx.globalAlpha = clamp(k * 3);
    const nf = 280, cw = tw('0', `800 ${nf}px ${F.n8}`), wd = tw('.', `800 ${nf}px ${F.n8}`), wn = cw * 2 + wd, wu = tw('级', `900 150px ${F.zh9}`);
    ctx.fillStyle = C.honey; ctx.fillRect(-24, -250, wn + wu + 80, 310); num(v.toFixed(1), 0, 0, nf, C.bg); text('级', wn + 26, -18, `900 150px ${F.zh9}`, C.bg);
    ctx.restore(); TX.push({ id: 'hook', text: '7.0级', x0: 48, y0: 700, x1: 700, y1: 1030 });
  }
  if (t >= .45) { const kb = seg(t, .45, .58); ctx.save(); ctx.globalAlpha = clamp(kb * 3); ctx.translate(72, 1120); ctx.scale(pop(t, .45), pop(t, .45)); text('地震 · 震源深度 10 千米', 0, 0, `900 52px ${F.zh9}`, C.ink); ctx.restore(); TX.push({ id: 'hook2', text: '地震震源深度10千米', x0: 72, y0: 1060, x1: 800, y1: 1130 }); }
}
// 5–9.5 s: from the region to the point — the day's own satellite picture, a reticle locks on the epicentre
function shotLocate(s, t) {
  const k = eio(seg(t, s.a, 8.6)), cam = geoCam(lerp(93.8, EPI[0], k), lerp(32.4, EPI[1], k), Math.exp(lerp(Math.log(270), Math.log(450), k)));
  ground(cam); shade();
  const [x, y] = cam.S(...EPI), kl = eo(seg(t, 6.3, 6.6)), r = lerp(260, 90, kl);
  if (kl > 0) {
    ctx.save(); ctx.globalAlpha = kl; ctx.strokeStyle = C.ink; ctx.lineWidth = 3; ctx.shadowColor = 'rgba(0,0,0,.8)'; ctx.shadowBlur = 6;
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(x - r, y); ctx.moveTo(x + r, y); ctx.lineTo(W, y); ctx.moveTo(x, 240); ctx.lineTo(x, y - r); ctx.moveTo(x, y + r); ctx.lineTo(x, BAND); ctx.stroke();
    ctx.strokeStyle = C.honey; ctx.lineWidth = 5; const L = 34;
    for (const [dx, dy] of [[-1, -1], [1, -1], [1, 1], [-1, 1]]) { const cx = x + dx * r, cy = y + dy * r; ctx.beginPath(); ctx.moveTo(cx, cy - dy * -L * 0 - dy * L); ctx.lineTo(cx, cy); ctx.lineTo(cx - dx * L, cy); ctx.stroke(); }
    ctx.restore();
  }
  epicentre(cam, t, 6.6);
  const kc = eo(seg(t, 6.5, 6.7)); if (kc > 0) {
    ctx.save(); ctx.globalAlpha = kc; const w = chip(72, y + 300, '那曲市 · 巴青县', C.ink, 40); num('32.40°N  93.79°E', 72, y + 360, 34, C.honey, 'left', 700); ctx.restore();
    TX.push({ id: 'loc', text: '那曲市巴青县', x0: 72, y0: y + 250, x1: 72 + w, y1: y + 310 });
  }
  sourceTag(t, s.a + .2, '中国地震台网 正式测定');
}
// 9.5–16.5 s: the depth — a section through the ground, the focus 10 km down
function shotDepth(s, t) {
  ledger(t, s.a); ctx.save(); camPush(t, s.a, s.b, 1, 1.03, 540, 800);
  text('震源深度', 72, 300, `900 64px ${F.zh9}`, C.ink); text('Focal depth, km below the surface', 74, 348, `500 26px ${F.n5}`, C.grey);
  const gy = 560, ppk = 50, x0 = 160, x1 = 1000;   // 50 px per km
  // the ground: the surface line, then the section fills downward
  const kg = eo(seg(t, s.a + .1, s.a + .5));
  ctx.fillStyle = 'rgba(141,139,131,.10)'; ctx.fillRect(x0, gy, (x1 - x0) * kg, 16 * ppk);
  ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(x0, gy); ctx.lineTo(lerp(x0, x1, kg), gy); ctx.stroke();
  text('地表', x0, gy - 22, `900 34px ${F.zh9}`, C.ink);
  for (let km = 0; km <= 15; km += 5) { const y = gy + km * ppk; ctx.fillStyle = C.grey; ctx.fillRect(x0 - 26, y - 1, 18, 3); num(String(km), x0 - 40, y + 12, 28, C.grey, 'right', 600); }
  // the drop to the focus, as the voice says "10"
  const kd = eio(seg(t, 10.55, 11.2)), xe = 640, ye = gy + 10 * ppk * kd;
  if (kd > 0) {
    ctx.save(); ctx.setLineDash([14, 10]); ctx.strokeStyle = C.honey; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(xe, gy); ctx.lineTo(xe, ye); ctx.stroke(); ctx.restore();
    ctx.fillStyle = C.ink; ctx.beginPath(); ctx.moveTo(xe - 18, gy - 30); ctx.lineTo(xe + 18, gy - 30); ctx.lineTo(xe, gy - 4); ctx.fill(); text('震中', xe + 30, gy - 16, `900 30px ${F.zh9}`, C.dim);
  }
  if (t > 11.2) {
    const pr = seg(t, 11.2, 12.4); ctx.strokeStyle = `rgba(255,74,61,${1 - pr})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(xe, ye, 16 + pr * 160, 0, 7); ctx.stroke();
    ctx.fillStyle = C.loss; ctx.beginPath(); ctx.arc(xe, ye, 18, 0, 7); ctx.fill();
    const k = seg(t, 11.2, 11.34); ctx.save(); ctx.translate(xe + 60, ye + 40); ctx.scale(pop(t, 11.2), pop(t, 11.2)); ctx.globalAlpha = clamp(k * 3);
    ctx.fillStyle = C.honey; ctx.fillRect(0, -110, 330, 140); const wn = num('10', 24, 10, 120, C.bg); text('千米', 34 + wn, -4, `900 56px ${F.zh9}`, C.bg); ctx.restore();
    TX.push({ id: 'd10', text: '10千米', x0: xe + 60, y0: ye - 70, x1: xe + 390, y1: ye + 70 });
  }
  // shallow: the waves have little rock to cross before the surface
  const ka = eo(seg(t, 12.6, 13.4)); if (ka > 0) {
    ctx.save(); ctx.globalAlpha = ka; ctx.strokeStyle = 'rgba(255,74,61,.7)'; ctx.lineWidth = 3;
    for (let i = 1; i <= 3; i++) { ctx.beginPath(); ctx.arc(xe, ye, i * 120 * ka, Math.PI * 1.05, Math.PI * 1.95); ctx.stroke(); }
    ctx.restore();
  }
  ctx.restore();
  shade(); sourceTag(t, s.a + .2, '中国地震台网 · 10.22 22:33');
}
// 16.5–22 s: who is near — rings at 5 and 20 km on the day's satellite picture, the places within each
function shotNear(s, t) {
  const cam = geoCam(EPI[0], EPI[1], Math.exp(lerp(Math.log(700), Math.log(980), eio(seg(t, s.a, s.b)))), W / 2, 900);
  ground(cam); shade(); epicentre(cam, t, s.a);
  ring(cam, 5, eo(seg(t, 17.1, 17.6)), C.honey, 5); ring(cam, 20, eo(seg(t, 19.1, 19.7)), C.ink, 4, [16, 10]);
  const [x, y] = cam.S(...EPI), r5 = 5 * KM * cam.z, r20 = 20 * KM * cam.z;
  if (t > 17.6) { const w = chip(x + r5 * 1.2 + 10, y - r5 * .3, '5 km', C.honey, 30); }
  if (t > 19.7) chip(x - 60, y - r20 - 24, '20 km', C.ink, 30);
  [['5 公里内', '冷达 · 普钦村 · 改迦咔村', 17.6, C.honey], ['20 公里内', '岗切乡 · 玛如乡', 19.1, C.ink]].forEach(([h, names, t0, col], i) => {
    const k = eo(seg(t, t0, t0 + .22)); if (k <= 0) return; const yy = 300 + i * 150;
    ctx.save(); ctx.globalAlpha = k; ctx.translate((1 - k) * -60, 0);
    ctx.fillStyle = 'rgba(14,14,12,.8)'; ctx.fillRect(60, yy - 70, 960, 124);
    const w = chip(84, yy, h, col, 38, col === C.ink ? C.bg : C.bg); text(names, 84 + w + 24, yy - 2, `900 44px ${F.zh9}`, C.ink);
    ctx.restore(); TX.push({ id: 'near' + i, text: i ? names : h + names, x0: 60, y0: yy - 70, x1: 1020, y1: yy + 54 });
  });
  sourceTag(t, s.a + .2, '中国地震台网 · 据澎湃新闻');
}
// 22–29 s: how far — distance bars, one per place, grown as the voice names it
const DIST = [['索县', 57, 22.6], ['巴青县城', 59, 23.6], ['比如县', 103, 24.1], ['聂荣县', 144, 24.5], ['青海 杂多县', 152, 24.9], ['那曲市', 194, 25.3], ['拉萨市', 399, 25.8]];
function shotDist(s, t) {
  ledger(t, s.a); ctx.save(); camPush(t, s.a, s.b, 1, 1.025, 300, 800);
  text('距震中', 72, 300, `900 64px ${F.zh9}`, C.ink); text('Distance from the epicentre, km', 74, 348, `500 26px ${F.n5}`, C.grey);
  const bx = 330, ppk = 560 / 400, y0 = 440, rh = 132;
  DIST.forEach(([lab, km, t0], i) => {
    const y = y0 + i * rh, k = eio(seg(t, t0, t0 + .45)), hot = i === 0 || i === 6;
    if (t < t0 - .3) { text(lab, bx - 30, y + 46, `900 40px ${F.zh9}`, C.mute, 'right'); return; }
    text(lab, bx - 30, y + 46, `900 ${hot ? 44 : 38}px ${F.zh9}`, hot ? C.honey : C.ink, 'right');
    ctx.fillStyle = hot ? C.honey : '#5E5C55'; ctx.fillRect(bx, y + 8, km * ppk * k, hot ? 58 : 46);
    if (k > .4) num(String(Math.round(km * k)), bx + km * ppk * k + 18, y + 54, hot ? 50 : 38, hot ? C.honey : C.dim);
    if (k >= 1) TX.push({ id: 'ds' + i, text: lab + km, x0: 60, y0: y, x1: bx + km * ppk + 160, y1: y + 70 });
  });
  ctx.restore();
  shade(); sourceTag(t, s.a + .2, '中国地震台网 · 据澎湃新闻');
}
// 29–35.5 s: how high — the plateau from the space station (file photo); the altitude lands as a stamp
function shotHigh(s, t) {
  const im = getImg('assets/img/plateau.jpg'); plate(im, 0, 0, W, BAND, lerp(1.0, 1.06, eio(seg(t, s.a, s.b))), .45, .5, GRADE + ' brightness(0.82)');
  shade();
  if (t > 30.9) {
    const k = seg(t, 30.9, 31.04); ctx.save(); ctx.translate(72, 820); ctx.scale(pop(t, 30.9), pop(t, 30.9)); ctx.globalAlpha = clamp(k * 3);
    ctx.fillStyle = C.honey; ctx.fillRect(-20, -200, 860, 250); const wn = num('4,864', 10, 20, 210, C.bg); text('米', 30 + wn, 0, `900 110px ${F.zh9}`, C.bg); ctx.restore();
    TX.push({ id: 'alt', text: '4864米', x0: 52, y0: 620, x1: 840, y1: 870 });
    const k2 = eo(seg(t, 31.2, 31.4)); ctx.save(); ctx.globalAlpha = k2; chip(72, 960, '震中 5 公里范围 · 平均海拔', C.ink, 34); ctx.restore();
    if (k2 >= 1) TX.push({ id: 'alt2', text: '平均海拔', x0: 72, y0: 920, x1: 560, y1: 980 });
  }
  sourceTag(t, s.a + .2, '中国地震台网 · 据澎湃新闻');
}
// 35.5–41.5 s: two numbers — the first automatic reading, struck through; the official reading lands
function shotTwo(s, t) {
  ctx.fillStyle = C.panel; ctx.fillRect(0, 0, W, H);
  const mid = 840, kd = eo(seg(t, s.a - .1, s.a + .18)); ctx.fillStyle = C.honey; ctx.fillRect(0, mid - 2, W * kd, 4);
  const rows = [[260, '自动测定', '6.7', '级左右', 36.6, C.loss], [mid + 70, '正式测定', '7.0', '级', 39.6, C.honey]];
  rows.forEach(([y, lab, v, unit, t0, col], i) => {
    const kl = eo(seg(t, s.a + .15 + i * .12, s.a + .4 + i * .12)); if (kl <= 0) return;
    ctx.save(); ctx.globalAlpha = kl * (i === 0 && t > 38.0 ? .55 : 1);
    chip(72, y + 70, lab, i ? C.honey : C.ink, 48);
    if (t >= t0) { ctx.save(); ctx.translate(72, y + 380); ctx.scale(pop(t, t0, .14), pop(t, t0, .14)); const wn = num(v, 0, 0, 260, i ? C.honey : C.ink); text(unit, wn + 20, -20, `900 80px ${F.zh9}`, C.grey); ctx.restore(); }
    else num('–', 72, y + 380, 260, C.mute);
    ctx.restore();
    if (t >= t0) TX.push({ id: 'two' + i, text: lab + v, x0: 72, y0: y, x1: 900, y1: y + 400 });
  });
  const ks = eo(seg(t, 38.0, 38.35)); if (ks > 0) { ctx.strokeStyle = C.loss; ctx.lineWidth = 12; ctx.beginPath(); ctx.moveTo(60, 520); ctx.lineTo(60 + 760 * ks, 560); ctx.stroke(); }
  const ku = eo(seg(t, 39.8, 40.0)); if (ku > 0) { ctx.save(); ctx.globalAlpha = ku; chip(72, 1420, '美国地质调查局 USGS：也是 7.0', C.ink, 36); ctx.restore(); if (ku >= 1) TX.push({ id: 'usgs', text: 'USGS也是7.0', x0: 72, y0: 1370, x1: 700, y1: 1440 }); }
  shade(); sourceTag(t, s.a + .2, '新华社快讯 · 中国地震台网');
}
// 41.5–47.5 s: what followed — the ground in grey, USGS estimated shaking over it, the aftershocks in the order they came
const AFT = [['22:59', '3.9', 42.9], ['23:03', '3.4', 43.25], ['23:13', '4.2', 44.4], ['23:18', '3.6', 44.8]];
function shotAfter(s, t) {
  const cam = geoCam(EPI[0], EPI[1] - .25, lerp(250, 275, eio(seg(t, s.a, s.b))), W / 2, 1000);
  ground(cam, 1); const ko = eo(seg(t, s.a + .15, s.a + .8));
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W, BAND); ctx.clip(); drawPlate(cam, PLATES.shake, .55 * ko, 'none'); ctx.restore();
  shade(); epicentre(cam, t, s.a);
  if (t > 44.4) { const [x, y] = cam.S(93.80, 32.47), pr = seg(t, 44.4, 45.4); ctx.strokeStyle = `rgba(255,194,26,${1 - pr})`; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(x, y, 10 + pr * 90, 0, 7); ctx.stroke(); ctx.fillStyle = C.honey; ctx.beginPath(); ctx.arc(x, y, 10, 0, 7); ctx.fill(); }
  ctx.fillStyle = 'rgba(14,14,12,.82)'; ctx.fillRect(60, 240, 960, 330 * eo(seg(t, s.a, s.a + .25)));
  text('余震 · 10月22日', 92, 300, `900 40px ${F.zh9}`, C.ink);
  AFT.forEach(([hm, m, t0], i) => {
    const k = eo(seg(t, t0, t0 + .18)), hot = hm === '23:13', x = 92 + (i % 2) * 470, y = 380 + Math.floor(i / 2) * 110; if (k <= 0) return;
    ctx.save(); ctx.globalAlpha = k; num(hm, x, y + 30, 44, hot ? C.honey : C.ink, 'left', 700); num(m, x + 170, y + 30, 64, hot ? C.honey : C.ink); text('级', x + 280, y + 26, `900 36px ${F.zh9}`, C.grey); ctx.restore();
    TX.push({ id: 'af' + i, text: hm + m, x0: x, y0: y - 30, x1: x + 330, y1: y + 40 });
  });
  const kl = eo(seg(t, 44.85, 45.05)); if (kl > 0) { ctx.save(); ctx.globalAlpha = kl; chip(72, 1460, 'USGS 模型估算震动 · 最强 VIII 度', C.ink, 32); ctx.restore(); if (kl >= 1) TX.push({ id: 'mmi', text: '最强VIII度', x0: 72, y0: 1420, x1: 700, y1: 1480 }); }
  credit('卫星 NASA Terra · 震动估算 USGS ShakeMap');
  sourceTag(t, s.a + .2, '中国地震台网 · 余震速报');
}
// 47.5–54.5 s: the first report from the county — re-set as a document, highlighted as it is read
function shotHurt(s, t) {
  desk(t, s, { list: { name: '巴青县应急管理局', type: '通报 · 据澎湃新闻' }, time: '10.23 00:11', title: '岗切乡发现2名受伤群众，已送往救治',
    desc: '距离震中最近的玛如乡、岗切乡震感强烈，有房屋开裂情况。县消防救援大队首批救援力量已赶赴灾区。', meta: '据澎湃新闻 · 10.23 00:11（文字为摘要重排）',
    marks: [[49.4, .9, 'title', '岗切乡发现2名受伤群众'], [52.6, .5, 'desc', '有房屋开裂情况']] }, .96, 1.03, .36, -.015);
  const k = seg(t, 50.4, 50.54); if (t > 50.4) {
    ctx.save(); ctx.translate(640, 1300); ctx.rotate(-.03); ctx.scale(pop(t, 50.4), pop(t, 50.4)); ctx.globalAlpha = clamp(k * 3);
    ctx.fillStyle = C.honey; ctx.fillRect(-20, -140, 400, 180); const wn = num('2', 10, 10, 150, C.bg); text('人受伤', 30 + wn, -10, `900 70px ${F.zh9}`, C.bg); ctx.restore();
    TX.push({ id: 'hurt', text: '2人受伤', x0: 620, y0: 1160, x1: 1030, y1: 1340 });
  }
  shade(); sourceTag(t, s.a + .2, '巴青县应急管理局 · 10.23 00:11');
}
// 54.5–58 s: the response — two panels, each lights as it is named
function shotResp(s, t) {
  ledger(t, s.a); ctx.save(); camPush(t, s.a, s.b, 1, 1.02, 540, 800);
  text('应急响应', 72, 300, `900 64px ${F.zh9}`, C.ink); text('Emergency response', 74, 348, `500 26px ${F.n5}`, C.grey);
  [['国家地震灾害', '4 级应急响应', '国务院抗震救灾指挥部办公室、应急管理部', 54.75], ['中国地震局', '二级应急响应', '地震部门的响应级别', 55.0]].forEach(([a, b, c, th], i) => {
    const t0 = s.a + .1 + i * .1, k = eo(seg(t, t0, t0 + .28)), y = 420 + i * 420 + (1 - k) * 200, on = t >= th;
    ctx.save(); ctx.globalAlpha = clamp(k * 1.5);
    ctx.fillStyle = on ? 'rgba(255,194,26,.08)' : 'rgba(255,255,255,.035)'; ctx.fillRect(72, y, 936, 360);
    if (on) { ctx.strokeStyle = C.honey; ctx.lineWidth = 6; ctx.strokeRect(75, y + 3, 930, 354); }
    text(a, 110, y + 100, `900 56px ${F.zh9}`, C.ink);
    if (on) chip(110, y + 220, b, C.honey, 72); else text(b, 110, y + 220, `900 72px ${F.zh9}`, C.mute);
    text(c, 112, y + 310, `500 28px ${F.zh5}`, C.grey);
    ctx.restore(); if (on) TX.push({ id: 'rp' + i, text: b, x0: 72, y0: y, x1: 1008, y1: y + 360 });
  });
  ctx.restore();
  shade(); sourceTag(t, s.a + .2, '据澎湃新闻 · 东网');
}
// 58–65.5 s: back up to the night; sources
function shotEnd(s, t) {
  plate(gframe(t, s.a, .6), 0, 0, W, BAND, lerp(1.12, 1.0, eio(seg(t, s.a, s.a + 4))), .55, .45, GRADE + ' brightness(.9)');
  shade(); flash(t, s.a, .08);
  const ks = eo(seg(t, 58.9, 59.2)); ctx.save(); ctx.globalAlpha = ks;
  const l1 = '信息 中国地震台网 · 新华社 · 澎湃新闻', l2 = '截至 ' + SNAP + ' · 画面 NASA · USGS';
  text(l1, 72, 1450, `500 24px ${F.n5}`, C.dim); text(l2, 72, 1490, `500 24px ${F.n5}`, C.dim); ctx.restore();
  if (ks >= 1) { TX.push({ id: 'e1', text: l1, x0: 72, y0: 1425, x1: 1000, y1: 1456 }); TX.push({ id: 'e2', text: l2, x0: 72, y0: 1465, x1: 900, y1: 1496 }); }
}

// ---------- main render ----------
let TX = [];
const DRAW = { hook: shotHook, locate: shotLocate, depth: shotDepth, near: shotNear, dist: shotDist, high: shotHigh, two: shotTwo, after: shotAfter, hurt: shotHurt, resp: shotResp, end: shotEnd };
function draw(t) {
  TX = []; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.filter = 'none';
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const s = shotAt(t); DRAW[s.k](s, t);
  if (s.k !== 'after') credit(s.cr);
  for (const c of CAPS) capCard(c, t);
  bug(t);
}
async function render(t) { NEED.clear(); draw(t); if (NEED.size) { await Promise.all([...NEED].map(load)); NEED.clear(); draw(t); } }
window.render = render;
window.TEXTS = () => TX;
function buildEV() {
  const ev = [
    ...SHOTS.slice(1).map(s => ({ t: s.a, type: 'cut', k: s.k })),
    ...CAPS.flatMap(c => c[2].split('|').map((_, i) => ({ t: +(c[0] + .04 + i * .12).toFixed(3), type: 'slam', big: c[4] || 1 }))),
    { t: .06, type: 'slam' }, { t: .13, type: 'hook' }, { t: .13, type: 'rattle', d: .45 }, { t: .45, type: 'slam' },
    { t: 5.0, type: 'whoosh' }, { t: 5.1, type: 'riser', d: 1.3 }, { t: 6.3, type: 'lock' }, { t: 6.6, type: 'ring' }, { t: 6.5, type: 'pop' },
    { t: 9.5, type: 'whoosh' }, { t: 10.55, type: 'drop', d: .65 }, { t: 11.2, type: 'stamp' }, { t: 11.2, type: 'ring' },
    { t: 16.5, type: 'whoosh' }, { t: 17.1, type: 'draw', d: .5 }, { t: 17.6, type: 'pop' }, { t: 19.1, type: 'draw', d: .6 }, { t: 19.1, type: 'pop' },
    { t: 22.0, type: 'whoosh' }, ...DIST.map(([, , t0]) => ({ t: t0, type: 'grow', d: .45 })),
    { t: 30.9, type: 'stamp' }, { t: 31.2, type: 'pop' },
    { t: 35.5, type: 'whoosh' }, { t: 36.6, type: 'pop' }, { t: 38.0, type: 'strike' }, { t: 39.6, type: 'stamp' }, { t: 39.8, type: 'pop' },
    { t: 42.5, type: 'whoosh' }, ...AFT.map(([, , t0]) => ({ t: t0, type: 'tick' })), { t: 44.4, type: 'ring' }, { t: 44.85, type: 'pop' },
    { t: 47.5, type: 'paper' }, { t: 49.4, type: 'marker', d: .9 }, { t: 50.4, type: 'stamp' }, { t: 52.6, type: 'marker', d: .5 },
    { t: 54.5, type: 'whoosh' }, { t: 54.75, type: 'pop' }, { t: 55.0, type: 'pop' },
    { t: 58.0, type: 'whoosh' }, { t: 62.6, type: 'verdict' },
  ];
  return ev.sort((a, b) => a.t - b.t);
}
(async () => {
  await Promise.all([900, 800, 700, 600, 500].map(w => Promise.all([document.fonts.load(`${w} 40px SC`, '地震'), document.fonts.load(`${w} 40px IT`, '0A')])));
  TL = await (await fetch('timeline.json')).json(); window.DUR = TL.dur;
  SHOTS = TL.shots; CAPS = TL.caps.map(c => [c.t0, c.t1, c.zh, c.en, c.big || 1]);
  window.EV = buildEV();
  await Promise.all(Object.values(PLATES).map(p => load(p.src)).concat([load('assets/img/plateau.jpg')]));
  await render(0); window.READY = true;
})();
