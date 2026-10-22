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

