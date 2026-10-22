// Caption News (字幕新闻) ·《热榜60秒 · 10.22》— vertical 1080×1920, 30 fps, 61 s
// One timeline (timeline.json: shots, captions, voice starts) drives the picture, the .srt and the mix.
// The material is the night's hot lists themselves (assets/lists.json, from a local DailyHotApi snapshot),
// plus public-domain NASA imagery and Natural Earth physical geography.
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
const SNAP = '10.23 00:47';                                          // snapshot time, Beijing

let TL = null, SHOTS = [], CAPS = [], LISTS = null, MAP = null;
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
  const tl = wrap(sp.title, tf, inner - 110), dl = sp.desc ? wrap(sp.desc, df, inner) : [];
  const h = 140 + tl.length * 78 + (dl.length ? 30 + dl.length * 50 : 0) + 110;
  ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 50; ctx.shadowOffsetY = 18;
  ctx.fillStyle = C.paper; ctx.fillRect(0, 0, CW, h); ctx.shadowColor = 'transparent';
  // header: list name + type, snapshot time
  ctx.fillStyle = '#E4E0D5'; ctx.fillRect(0, 0, CW, 92);
  text(sp.list.name, P, 60, `900 36px ${F.zh9}`, C.pink); text(sp.list.type, P + tw(sp.list.name, `900 36px ${F.zh9}`) + 18, 58, `500 28px ${F.zh5}`, '#6B685F');
  text(SNAP, CW - P, 58, `500 26px ${F.n5}`, '#6B685F', 'right');
  y = 140;
  // rank badge
  ctx.fillStyle = sp.rank === 1 ? '#E2422F' : '#3A3935'; ctx.fillRect(P, y + 4, 84, 84); num(String(sp.rank), P + 42, y + 68, 54, '#fff', 'center');
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
  mark('title', tl, tf, 78, P + 110, y + 70);
  tl.forEach((ln, i) => text(ln.s, P + 110, y + 70 + i * 78, tf, C.pink));
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
const L = id => LISTS.find(l => l.id === id);
const item = (id, r) => L(id).items[r - 1];

// ---------- the wall: all 378 entries, 7 columns (one per list) ----------
const RH = 64, COLW = 1000, GAP = 70;
function wallRows() { const rows = []; LISTS.forEach((l, c) => { rows.push({ c, r: 0, h: true, l }); l.items.forEach(([rank, title, hot]) => rows.push({ c, r: rank, rank, title, hot, l })); }); return rows; }
let ROWS = null;
const WALLW = 7 * COLW + 6 * GAP, WALLH = 101 * RH;
// world → screen: camera at focus (fx, fy) in wall units, zoom z, placed at screen (sx, sy)
function wall(z, fx, fy, sx, sy, lit = () => 0, alpha = 1, mode = 'cols') {
  ctx.save(); ctx.globalAlpha = alpha; ctx.translate(sx, sy); ctx.scale(z, z); ctx.translate(-fx, -fy);
  const x0 = fx - sx / z, x1 = fx + (W - sx) / z, y0 = fy - sy / z, y1 = fy + (H - sy) / z;
  const txt = z * 30 >= 9;
  ROWS.forEach((row, i) => {
    const X = mode === 'cols' ? row.c * (COLW + GAP) : 0, Y = mode === 'cols' ? row.r * RH : i * RH;
    if (X > x1 || X + COLW < x0 || Y > y1 || Y + RH < y0) return;
    const on = lit(row);
    if (row.h) { ctx.fillStyle = C.honey; ctx.fillRect(X, Y + 10, 10, RH - 20); if (txt) { text(row.l.name, X + 28, Y + 44, `900 32px ${F.zh9}`, C.ink); text(row.l.type, X + 40 + tw(row.l.name, `900 32px ${F.zh9}`), Y + 43, `500 24px ${F.zh5}`, C.grey); } else { ctx.fillStyle = C.ink; ctx.fillRect(X + 28, Y + 18, 160, 28); } return; }
    if (on) { ctx.fillStyle = `rgba(255,194,26,${on})`; ctx.fillRect(X - 10, Y + 4, COLW + 20, RH - 8); }
    const tf = `500 30px ${F.zh5}`, maxW = COLW - 100;
    if (!row.tt) { let s = row.title; if (tw(s, tf) > maxW) { while (s.length && tw(s + '…', tf) > maxW) s = s.slice(0, -1); s += '…'; } row.tt = s; row.tw = tw(s, tf); }
    if (txt) { num(String(row.rank), X + 52, Y + 44, 26, on ? C.bg : C.grey, 'right'); text(row.tt, X + 76, Y + 43, tf, on ? C.bg : (row.rank <= 3 ? C.ink : C.dim)); }
    else { ctx.fillStyle = on ? C.bg : (row.rank <= 3 ? 'rgba(247,245,239,.85)' : 'rgba(247,245,239,.42)'); ctx.fillRect(X + 76, Y + 22, row.tw, 22); }
  });
  ctx.restore();
}
const rowXY = (id, rank) => { const c = LISTS.findIndex(l => l.id === id); return [c * (COLW + GAP), rank * RH]; };

// ---------- shots ----------
// 0–3 s: the hook is a question — the Bilibili No.1 as a document, its title highlighted on frame 4
function shotOpen(s, t) {
  const b = item('bilibili', 1);
  desk(t, s, { list: L('bilibili'), rank: 1, title: b[1], meta: '播放 ' + fmt(b[2]), marks: [[.13, .35, 'title', '折1万次，会坏吗？']] }, .96, 1.06, .40, -.025);
  shade();
  const k = seg(t, .6, .73), roll = Math.round(478 * eo(seg(t, .6, 1.05)));
  if (t > .6) {
    ctx.save(); ctx.translate(640, 1120); ctx.rotate(-.04); const sc = lerp(1.4, 1, back(k, 1.5)); ctx.scale(sc, sc); ctx.globalAlpha = clamp(k * 3);
    ctx.fillStyle = C.honey; ctx.fillRect(-40, -150, 420, 200); text('播放', -10, -100, `900 34px ${F.zh9}`, C.bg);
    const wn = num(String(roll), 0, 20, 120, C.bg); text('万', wn + 10, 14, `900 80px ${F.zh9}`, C.bg); ctx.restore();
    TX.push({ id: 'views', text: '播放478万', x0: 600, y0: 960, x1: 1030, y1: 1170 });
  }
  sourceTag(t, .3, '哔哩哔哩 热榜 · 第1');
}
// 3–7.5 s: pull out from that row to the whole wall — seven lists, 378 entries
function shotWall(s, t) {
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const [bx, by] = rowXY('bilibili', 1), k = eio(seg(t, s.a + .05, s.a + 2.6));
  const zA = 1.15, zB = W * .94 / WALLW, z = Math.exp(lerp(Math.log(zA), Math.log(zB), k));
  const fx = lerp(bx + 420, WALLW / 2, k), fy = lerp(by + RH / 2, WALLH / 2, k);
  wall(z, fx, fy, W / 2, lerp(700, 720, k), row => row.l.id === 'bilibili' && row.rank === 1 ? 1 - .6 * k : 0);
  shade();
  // the counter lands on the voice's "378"
  const t1 = 5.55, kk = seg(t, t1, t1 + .14), roll = Math.round(378 * eo(seg(t, t1, 6.2)));
  if (t > t1) {
    ctx.save(); ctx.translate(W / 2, 1310); const sc = lerp(1.45, 1, back(kk, 1.4)); ctx.scale(sc, sc); ctx.globalAlpha = clamp(kk * 3);
    const nf = 200, cw = tw('0', `800 ${nf}px ${F.n8}`), wu = tw('条', `900 110px ${F.zh9}`), w = cw * 3 + wu + 90;
    ctx.fillStyle = C.honey; ctx.fillRect(-w / 2, -186, w, 236); num(String(roll), -w / 2 + 30 + cw * 3, 0, nf, C.bg, 'right'); text('条', -w / 2 + 50 + cw * 3, -12, `900 110px ${F.zh9}`, C.bg);
    ctx.restore();
    TX.push({ id: 'n378', text: '378条', x0: 250, y0: 1110, x1: 830, y1: 1370 });
  }
  const kc = eo(seg(t, 5.0, 5.2)); if (kc > 0) {
    ctx.save(); ctx.globalAlpha = kc; const lab = '7 个平台', f = `800 30px ${F.n8}`, w = tw(lab, f) + 44;
    ctx.fillStyle = 'rgba(14,14,12,.85)'; ctx.fillRect(W / 2 - w / 2, 1022, w, 54); text(lab, W / 2, 1060, f, C.ink, 'center'); ctx.restore();
    TX.push({ id: 'n7', text: lab, x0: W / 2 - w / 2, y0: 1022, x1: W / 2 + w / 2, y1: 1076 });
  }
  sourceTag(t, s.a + .3, '7 个热榜 · DailyHotApi');
}
// 7.5–14.5 s: lit stack — four lists talk about one phone; each lights on "四个平台", counts roll, the total stamps on "十条"
const PHONE = [['36kr', 4, '我们用了一周的 iPhone Duo…'], ['ithome', 3, '苹果首款折叠屏手机 iPhone Duo…'], ['bilibili', 2, '折1万次，会坏吗？iPhone Duo…'], ['toutiao', 1, 'iPhone Duo折叠3000次后折痕加深']];
function shotGrid(s, t) {
  ledger(t, s.a); ctx.save(); camPush(t, s.a, s.b, 1, 1.025, 540, 760);
  text('跨榜最多', 72, 300, `900 64px ${F.zh9}`, C.ink); text('The story on the most lists', 74, 348, `500 26px ${F.n5}`, C.grey);
  const hit = [11.25, 11.4, 11.55, 11.7], PH_ = 196, G = 18, y0 = 400;
  PHONE.forEach(([id, n, ex], i) => {
    const t0 = s.a + .1 + i * .1, k = eo(seg(t, t0, t0 + .28)), y = y0 + i * (PH_ + G) + (1 - k) * 220, on = t >= hit[i];
    ctx.save(); ctx.globalAlpha = clamp(k * 1.5);
    ctx.fillStyle = on ? 'rgba(255,194,26,.08)' : 'rgba(255,255,255,.035)'; ctx.fillRect(72, y, 936, PH_);
    if (on) { const kf = 1 - seg(t, hit[i], hit[i] + .3); ctx.strokeStyle = `rgba(255,194,26,${.55 + .45 * kf})`; ctx.lineWidth = 6; ctx.strokeRect(75, y + 3, 930, PH_ - 6); }
    num(String(i + 1), 100, y + 52, 28, C.honey);
    const nm = L(id).name; if (on) chip(140, y + 70, nm, C.honey, 44); else text(nm, 160, y + 70, `900 44px ${F.zh9}`, C.ink);
    text(ex, 160, y + 150, `500 28px ${F.zh5}`, C.dim);
    const kr = eo(seg(t, hit[i], hit[i] + .45)), v = Math.round(n * kr);
    const wn = num(on ? String(v) : '–', 930, y + 130, 120, on && kr >= 1 ? C.honey : C.mute, 'right'); text('条', 940, y + 122, `900 40px ${F.zh9}`, C.grey);
    ctx.restore();
    if (k >= 1) TX.push({ id: 'ph' + i, text: nm, x0: 140, y0: y + 10, x1: 520, y1: y + 90 });
  });
  ctx.restore();
  // the total
  const tt = 12.05; if (t > tt) {
    const k = seg(t, tt, tt + .14); ctx.save(); ctx.translate(72, 1395); const sc = lerp(1.35, 1, back(k, 1.4)); ctx.scale(sc, sc); ctx.globalAlpha = clamp(k * 3);
    const w1 = chip(0, 0, '合计', C.ink, 44); ctx.fillStyle = C.honey; ctx.fillRect(w1, -110, 300, 150); const wn = num('10', w1 + 30, 22, 140, C.bg); text('条', w1 + 40 + wn, 10, `900 70px ${F.zh9}`, C.bg);
    text('iPhone Duo', w1 + 330, -10, `800 56px ${F.n8}`, C.ink);
    ctx.restore(); TX.push({ id: 'tot', text: '合计10条', x0: 72, y0: 1280, x1: 1000, y1: 1440 });
  }
  shade(); sourceTag(t, s.a + .3, '4 个热榜 · ' + SNAP);
}
// 14.5–19.5 s: the score — 2 : 3, punch in on the 3 as the voice says it; silver
function shotScore(s, t) {
  ledger(t, s.a); ctx.save(); camPush(t, s.a, s.b, 1, 1.03, 540, 800);
  text('女团决赛', 72, 300, `900 64px ${F.zh9}`, C.ink); text("Asian Championships · women's team final", 74, 348, `500 26px ${F.n5}`, C.grey);
  const tp = 16.85, kp = eo(seg(t, tp, tp + .3)), z = lerp(1, 1.06, kp);
  ctx.translate(820, 860); ctx.scale(z, z); ctx.translate(-820, -860);
  const rows = [['中国', 'CHN', 2, 16.55], ['日本', 'JPN', 3, 16.85]];
  rows.forEach(([zh, en, v, th], i) => {
    const y = 600 + i * 330, k = eo(seg(t, s.a + .15 + i * .1, s.a + .45 + i * .1)); ctx.save(); ctx.globalAlpha = k;
    ctx.fillStyle = 'rgba(255,255,255,.04)'; ctx.fillRect(72, y - 200, 936, 280);
    text(zh, 120, y - 40, `900 96px ${F.zh9}`, C.ink); text(en, 124, y + 30, `800 34px ${F.n8}`, C.grey);
    const on = t >= th, kk = seg(t, th, th + .14), sc = on ? lerp(1.5, 1, back(kk, 1.4)) : 1;
    ctx.save(); ctx.translate(840, y + 20); ctx.scale(sc, sc); num(on ? String(v) : '–', 0, 0, 240, on ? C.ink : C.mute, 'center'); ctx.restore();
    ctx.restore();
    if (t > th) TX.push({ id: 'sc' + i, text: zh + v, x0: 100, y0: y - 200, x1: 1000, y1: y + 80 });
  });
  if (t > tp) { ctx.strokeStyle = C.honey; ctx.lineWidth = 6; const kr = eo(seg(t, tp + .1, tp + .45)); ctx.beginPath(); ctx.arc(840, 860, 140, -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * kr); ctx.stroke(); }
  ctx.restore();
  stamp(t, 17.6, 760, 1300, '摘得银牌', -.05, 60);
  // where it ranked
  [['今日头条 第8', 15.4], ['腾讯新闻 第10', 15.6]].forEach(([lab, t0], i) => { const k = eo(seg(t, t0, t0 + .2)); if (k <= 0) return; ctx.save(); ctx.globalAlpha = k; chip(72, 1230 + i * 90 + (1 - k) * 20, lab, C.ink, 34); ctx.restore(); TX.push({ id: 'rk' + i, text: lab, x0: 72, y0: 1190 + i * 90, x1: 420, y1: 1250 + i * 90 }); });
  shade(); sourceTag(t, s.a + .3, '今日头条 · 腾讯新闻 · ' + SNAP);
}
// 19.5–24.5 s: the document says it — the Tieba entry, its first sentence highlighted as spoken; the People's Daily entry slides in
function shotCafe(s, t) {
  const e = item('tieba', 10), desc = '今日起，星巴克将在全国开始施行消费入座，门店会摆放相关提示牌。在实际的运营过程中，店员会提供统一的服务指引和必要支持。';
  desk(t, s, { list: L('tieba'), rank: 10, title: e[1], desc, meta: '讨论 ' + fmt(e[2]), marks: [[20.3, 1.25, 'desc', '今日起，星巴克将在全国开始施行消费入座']] }, .98, 1.05, .34, .018);
  const tk = 21.0, k = eo(seg(t, tk, tk + .2));
  if (k > 0) {
    ctx.save(); ctx.translate((1 - k) * 700, 0); const y = 1160, x = 120;
    ctx.shadowColor = 'rgba(0,0,0,.6)'; ctx.shadowBlur = 40; ctx.fillStyle = C.paper; ctx.fillRect(x, y, 900, 200); ctx.shadowColor = 'transparent';
    ctx.fillStyle = '#E4E0D5'; ctx.fillRect(x, y, 900, 66); text('今日头条', x + 36, y + 46, `900 30px ${F.zh9}`, C.pink); text('热榜', x + 170, y + 45, `500 24px ${F.zh5}`, '#6B685F');
    ctx.fillStyle = '#3A3935'; ctx.fillRect(x + 36, y + 90, 70, 70); num('6', x + 71, y + 143, 46, '#fff', 'center');
    text('人民日报评星巴克“消费入座”', x + 130, y + 142, `900 46px ${F.zh9}`, C.pink);
    ctx.restore(); if (k >= 1) TX.push({ id: 'rmrb', text: '人民日报评星巴克', x0: x, y0: y, x1: x + 900, y1: y + 200 });
  }
  shade(); sourceTag(t, s.a + .2, '百度贴吧 热议榜 · 第10');
}
// 24.5–29 s: the night over Asia (NASA Black Marble) — seven lists, seven different No.1s
const FIRSTS = ['toutiao', 'tieba', 'bilibili', '36kr', 'ithome', 'sina-news', 'qq-news'];
const short = s => { s = s.replace(/^8点1氪丨/, ''); return s.length > 11 ? s.slice(0, 11) + '…' : s; };
function shotGlobe(s, t) {
  const im = frame('gl', 138, t, s.a); plate(im, 0, 0, W, BAND, lerp(1.0, 1.05, eio(seg(t, s.a, s.b))), .5, .45);
  ctx.fillStyle = 'rgba(14,14,12,.35)'; ctx.fillRect(0, 0, W, BAND);
  FIRSTS.forEach((id, i) => {
    const t0 = 25.0 + i * .2, k = eo(seg(t, t0, t0 + .2)); if (k <= 0) return;
    const y = 330 + i * 128; ctx.save(); ctx.globalAlpha = k; ctx.translate((1 - k) * -60, 0);
    ctx.fillStyle = 'rgba(14,14,12,.78)'; ctx.fillRect(72, y, 936, 104);
    const w = chip(92, y + 68, L(id).name, C.ink, 32); num('1', 92 + w + 34, y + 72, 44, C.honey, 'center');
    text(short(item(id, 1)[1]), 92 + w + 70, y + 66, `500 34px ${F.zh5}`, C.ink);
    ctx.restore(); if (k >= 1) TX.push({ id: 'f' + i, text: L(id).name, x0: 92, y0: y + 20, x1: 92 + w, y1: y + 90 });
  });
  shade(); sourceTag(t, 25.0, '7 个热榜 · 第1名');
}
// 29–35 s: signature — all 378 entries race past, brake, freeze; the two No.1s that are the same story are pulled out
const TF = 31.5;
function shotScroll(s, t) {
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const total = ROWS.length * RH, k = eio(seg(t, s.a - .1, TF)), oy = lerp(-200, total - 1100, k);
  const fz = t < TF ? 1 : lerp(1, 1.08, eo(seg(t, TF, TF + .3)));
  ctx.save(); ctx.translate(W / 2, 800); ctx.scale(fz, fz); ctx.translate(-W / 2, -800);
  // motion streak: draw the wall a few times along the scroll direction while it is fast
  const v = Math.abs(lerp(-200, total - 1100, eio(seg(t + 1 / FPS, s.a - .1, TF))) - oy), n = t < TF ? clamp(Math.round(v / 60), 1, 4) : 1;
  for (let j = 0; j < n; j++) wall(.9, COLW / 2, oy + j * v / n, W / 2, 0, () => 0, (t < TF ? 1 : .22) / n * (j === 0 ? 1 : .8), 'col');
  ctx.restore();
  if (t >= TF) {
    const two = [['toutiao', '西藏那曲巴青县发生7.0级地震', '7.0级地震'], ['tieba', '愿平安!西藏那曲发生7级地震', '7级地震']];
    two.forEach(([id, title, hot], i) => {
      const t0 = TF + .05 + i * .1, kk = eo(seg(t, t0, t0 + .28)), y = 560 + i * 270 + (1 - kk) * (i ? 500 : -500);
      ctx.save(); ctx.globalAlpha = clamp(kk * 2);
      ctx.fillStyle = 'rgba(21,21,18,.96)'; ctx.fillRect(60, y, 960, 220); ctx.fillStyle = C.honey; ctx.fillRect(60, y, 10, 220);
      chip(100, y + 76, L(id).name, C.ink, 34); text(L(id).type, 100 + tw(L(id).name, `900 34px ${F.zh9}`) + 50, y + 74, `500 28px ${F.zh5}`, C.grey);
      ctx.fillStyle = '#E2422F'; ctx.fillRect(100, y + 112, 76, 76); num('1', 138, y + 170, 50, '#fff', 'center');
      const f = `900 52px ${F.zh9}`, a = title.indexOf(hot), pre = title.slice(0, a), xh = 200 + tw(pre, f), wh = tw(hot, f), kh = eo(seg(t, TF + .5 + i * .12, TF + .8 + i * .12));
      ctx.fillStyle = C.honey; ctx.fillRect(xh - 8, y + 118, (wh + 16) * kh, 66);
      text(pre, 200, y + 168, f, C.ink); text(hot, xh, y + 168, f, kh > .5 ? C.bg : C.ink); text(title.slice(a + hot.length), xh + wh, y + 168, f, C.ink);
      ctx.restore();
      if (kk >= 1) TX.push({ id: 'two' + i, text: hot, x0: xh - 8, y0: y + 118, x1: xh + wh + 8, y1: y + 184 });
    });
    // freeze furniture: brackets close in, timecode chip with a pause mark
    const kb = eo(seg(t, TF + .1, TF + .3)), bx0 = 40, bx1 = 1040, by0 = lerp(470, 530, kb), by1 = lerp(1150, 1080, kb), Lb = 60;
    ctx.save(); ctx.globalAlpha = kb; ctx.strokeStyle = C.honey; ctx.lineWidth = 6;
    for (const [x, y, dx, dy] of [[bx0, by0, 1, 1], [bx1, by0, -1, 1], [bx1, by1, -1, -1], [bx0, by1, 1, -1]]) { ctx.beginPath(); ctx.moveTo(x, y + dy * Lb); ctx.lineTo(x, y); ctx.lineTo(x + dx * Lb, y); ctx.stroke(); }
    ctx.fillStyle = 'rgba(14,14,12,.75)'; ctx.fillRect(W - 270, 140, 226, 46); ctx.fillStyle = C.loss; ctx.fillRect(W - 254, 152, 8, 22); ctx.fillRect(W - 240, 152, 8, 22);
    num(SNAP, W - 60, 175, 26, C.ink, 'right'); ctx.restore();
  }
  shade(); flash(t, TF, .14);
}
// 35–40.5 s: where — a physical locator (lakes, rivers, graticule; no borders), push to 32.40°N 93.79°E, rings, 7.0
const EPI = [93.79, 32.40], PLACES = [['那曲', 92.05, 31.48], ['拉萨', 91.13, 29.65], ['西宁', 101.78, 36.62], ['玉树', 97.01, 33.0]];
function shotMap(s, t) {
  ledger(t, s.a, false); flash(t, s.a, .1);
  const P = MAP.P, mp = (lon, lat) => [(lon - P.lon0) * P.k, (P.lat1 - lat) * P.kl];
  const [ex, ey] = mp(...EPI), k0 = W / MAP.w, kz = eio(seg(t, 36.6, 39.6)), z = k0 * lerp(1, 2.3, kz);
  const fx = lerp(MAP.w / 2, ex, kz), fy = lerp(MAP.h / 2, ey, kz), sx = W / 2, sy = 820;
  const S = (x, y) => [sx + (x - fx) * z, sy + (y - fy) * z];
  ctx.save(); ctx.beginPath(); ctx.rect(0, 240, W, BAND - 240); ctx.clip();
  // graticule every 2°
  ctx.strokeStyle = 'rgba(255,255,255,.08)'; ctx.lineWidth = 2;
  for (let lon = 84; lon <= 104; lon += 2) { const [a, b] = S(...mp(lon, 38)), [c, d] = S(...mp(lon, 26)); ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke(); }
  for (let lat = 26; lat <= 38; lat += 2) { const [a, b] = S(...mp(84, lat)), [c, d] = S(...mp(104, lat)); ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.stroke(); }
  const kr = eo(seg(t, s.a + .1, s.a + .7));
  ctx.strokeStyle = `rgba(120,150,160,${.55 * kr})`; ctx.lineWidth = 2.5;
  for (const r of MAP.rivers) { ctx.beginPath(); r.pts.forEach((p, j) => { const [x, y] = S(...p); j ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.stroke(); }
  ctx.fillStyle = `rgba(90,125,140,${.75 * kr})`;
  for (const l of MAP.lakes) { ctx.beginPath(); l.pts.forEach((p, j) => { const [x, y] = S(...p); j ? ctx.lineTo(x, y) : ctx.moveTo(x, y); }); ctx.closePath(); ctx.fill(); }
  // lake and town labels
  const kl = eo(seg(t, s.a + .4, s.a + .7));
  ctx.save(); ctx.globalAlpha = kl * (1 - .6 * kz);
  [['纳木错', 90.6, 30.7], ['色林错', 89.0, 31.8], ['青海湖', 100.2, 37.25]].forEach(([n, lo, la]) => { const [x, y] = S(...mp(lo, la)); text(n, x, y + 44, `500 24px ${F.zh5}`, 'rgba(160,190,200,.9)', 'center'); });
  PLACES.forEach(([n, lo, la]) => { const [x, y] = S(...mp(lo, la)); ctx.fillStyle = C.ink; ctx.beginPath(); ctx.arc(x, y, 7, 0, 7); ctx.fill(); text(n, x + 16, y + 10, `900 28px ${F.zh9}`, C.dim); });
  ctx.restore();
  // graticule labels at the edges
  ctx.save(); ctx.globalAlpha = 1 - kz; for (let lon = 86; lon <= 102; lon += 4) { const [x] = S(...mp(lon, 26)); text(lon + '°E', x, 1400, `500 22px ${F.n5}`, C.grey, 'center'); } ctx.restore();
  // the epicentre
  const [px, py] = S(ex, ey);
  [35.3, 35.8, 36.3, 37.35].forEach(t0 => { const pr = seg(t, t0, t0 + 1.1); if (pr <= 0 || pr >= 1) return; ctx.strokeStyle = `rgba(255,74,61,${1 - pr})`; ctx.lineWidth = 5; ctx.beginPath(); ctx.arc(px, py, 14 + pr * 240, 0, 7); ctx.stroke(); });
  if (t > 35.25) { ctx.fillStyle = C.loss; ctx.beginPath(); ctx.arc(px, py, 16, 0, 7); ctx.fill(); ctx.strokeStyle = C.ink; ctx.lineWidth = 4; ctx.stroke(); }
  ctx.restore();
  const kc = eo(seg(t, 35.8, 36.0));
  if (kc > 0) {
    ctx.save(); ctx.globalAlpha = kc; ctx.strokeStyle = C.honey; ctx.lineWidth = 4; const lx = px + 60, ly = py - 190;
    ctx.beginPath(); ctx.moveTo(px + 14, py - 14); ctx.lineTo(lx, ly + 20); ctx.lineTo(lx + 330, ly + 20); ctx.stroke();
    text('那曲 · 巴青县', lx, ly - 8, `900 48px ${F.zh9}`, C.ink); num('32.40°N 93.79°E', lx, ly + 66, 30, C.honey, 'left', 600);
    ctx.restore(); TX.push({ id: 'bq', text: '那曲 · 巴青县', x0: lx, y0: ly - 60, x1: lx + 340, y1: ly + 20 });
  }
  stamp(t, 37.35, 330, 1330, '7.0 级', -.05, 92);
  text('震中位置', 72, 300, `900 64px ${F.zh9}`, C.ink); text('Epicentre · locator, not a boundary map', 74, 348, `500 26px ${F.n5}`, C.grey);
  TX.push({ id: 'mapT', text: '震中位置', x0: 62, y0: 230, x1: 340, y1: 320 });
  text('示意图 · 湖泊河流 Natural Earth', 72, 1500, `500 22px ${F.zh5}`, C.grey);
  shade(); sourceTag(t, s.a + .3, '中国地震台网 · 据百度贴吧热议榜');
}
// 40.5–46.5 s: the entry's own words — who measured it, when, how deep — highlighted as the voice reads them
function shotQuake(s, t) {
  const e = item('tieba', 1), desc = '中国地震台网正式测定：10月22日22时33分在西藏那曲市巴青县（北纬32.40度，东经93.79度）发生7.0级地震，震源深度10千米。';
  desk(t, s, { list: L('tieba'), rank: 1, title: e[1], desc, meta: '讨论 ' + fmt(e[2]), marks: [[40.8, 1.55, 'desc', '中国地震台网正式测定'], [43.4, .85, 'desc', '10月22日22时33分'], [44.96, 1.0, 'desc', '震源深度10千米']] }, .9, .98, .30, -.014);
  const tp = 44.0, k = seg(t, tp, tp + .14);
  if (t > tp) {
    ctx.save(); ctx.translate(470, 1240); ctx.rotate(-.03); const sc = lerp(1.4, 1, back(k, 1.5)); ctx.scale(sc, sc); ctx.globalAlpha = clamp(k * 3);
    ctx.fillStyle = C.honey; ctx.fillRect(-20, -150, 540, 190); num('22:33', 16, 10, 140, C.bg); ctx.restore();
    TX.push({ id: 't2233', text: '22:33', x0: 440, y0: 1080, x1: 1020, y1: 1290 });
  }
  shade(); sourceTag(t, s.a + .2, '百度贴吧 热议榜 · 第1');
}
// 46.5–51 s: ledger split — the same story is No.1 on both lists; counters race, the stamp lands on the divider
function shotSplit(s, t) {
  ctx.fillStyle = C.panel; ctx.fillRect(0, 0, W, H);
  const kd = eo(seg(t, s.a - .1, s.a + .18)), mid = 860;
  const halves = [[230, 'toutiao', '热度', 13953302, 46.8], [mid + 30, 'tieba', '讨论', 2285310, 47.3]];
  halves.forEach(([y, id, unit, v, t0], i) => {
    const k = eo(seg(t, s.a + .1 + i * .15, s.a + .32 + i * .15)); if (k <= 0) return;
    ctx.save(); ctx.globalAlpha = k; ctx.translate(0, (1 - k) * (i ? 60 : -60));
    ctx.strokeStyle = C.rule; ctx.lineWidth = 2; for (let yy = y + 40; yy < y + 600; yy += 54) { ctx.beginPath(); ctx.moveTo(0, yy); ctx.lineTo(W, yy); ctx.stroke(); }
    const w = chip(72, y + 120, L(id).name, C.ink, 52); text(L(id).type, 72 + w + 24, y + 112, `500 36px ${F.zh5}`, C.grey);
    ctx.fillStyle = '#E2422F'; ctx.fillRect(72, y + 190, 150, 150); text('第', 92, y + 300, `900 44px ${F.zh9}`, '#fff'); num('1', 182, y + 312, 96, '#fff', 'center');
    const kr = eo(seg(t, t0, t0 + .7)), wn = num(t < t0 ? '–' : fmt(v * kr), 260, y + 300, 104, kr >= 1 ? C.honey : C.ink);
    text(unit, 262, y + 360, `900 40px ${F.zh9}`, C.grey); text('≈ ' + wan(v), 262 + tw(unit, `900 40px ${F.zh9}`) + 20, y + 360, `800 40px ${F.n8}`, kr >= 1 ? C.honey : C.grey);
    ctx.restore();
    if (t > t0 + .7) TX.push({ id: 'sp' + i, text: L(id).name + '第1', x0: 72, y0: y + 40, x1: 1000, y1: y + 380 });
  });
  ctx.fillStyle = C.honey; ctx.fillRect(0, mid - 2, W * kd, 4);
  stamp(t, 49.0, W / 2, mid + 24, '双榜第一', -.05, 70);
  shade(); sourceTag(t, s.a + .2, '今日头条 · 百度贴吧 · ' + SNAP);
}
// 51–55 s: the plateau from the space station (file photo), slow push
function shotPlateau(s, t) {
  const im = getImg('assets/img/plateau.jpg'); plate(im, 0, 0, W, BAND, lerp(1.0, 1.06, eio(seg(t, s.a, s.b + 1))), .45, .5, GRADE + ' brightness(0.86)');
  shade();
}
// 55–61 s: the wall again — every entry grey, the one story lit; pull back until it is one bright line among 378
function shotEnd(s, t) {
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const [x0, y0] = rowXY('toutiao', 1), k = eio(seg(t, s.a, s.a + 3.2));
  const zA = 1.0, zB = W * .94 / WALLW, z = Math.exp(lerp(Math.log(zA), Math.log(zB), k));
  const fx = lerp(x0 + 500, WALLW / 2, k), fy = lerp(y0 + RH / 2, WALLH / 2, k);
  const lit = row => (row.rank === 1 && (row.l.id === 'toutiao' || row.l.id === 'tieba')) ? 1 : 0;
  wall(z, fx, fy, W / 2, 700, lit, .85);
  shade(); flash(t, s.a, .08);
  const ks = eo(seg(t, 55.6, 55.9)); ctx.save(); ctx.globalAlpha = ks;
  const l1 = '数据 DailyHotApi · 截至 ' + SNAP + ' 北京时间', l2 = '画面 NASA · Natural Earth · 公有领域';
  text(l1, 72, 1450, `500 24px ${F.n5}`, C.dim); text(l2, 72, 1490, `500 24px ${F.n5}`, C.dim); ctx.restore();
  if (ks >= 1) { TX.push({ id: 'e1', text: l1, x0: 72, y0: 1425, x1: 900, y1: 1456 }); TX.push({ id: 'e2', text: l2, x0: 72, y0: 1465, x1: 900, y1: 1496 }); }
}

// ---------- main render ----------
let TX = [];
const DRAW = { open: shotOpen, wall: shotWall, grid: shotGrid, score: shotScore, cafe: shotCafe, globe: shotGlobe, scroll: shotScroll, map: shotMap, quake: shotQuake, split: shotSplit, plateau: shotPlateau, end: shotEnd };
function draw(t) {
  TX = []; ctx.setTransform(1, 0, 0, 1, 0, 0); ctx.globalAlpha = 1; ctx.filter = 'none';
  ctx.fillStyle = C.bg; ctx.fillRect(0, 0, W, H);
  const s = shotAt(t); DRAW[s.k](s, t);
  credit(s.k === 'map' ? '地图 Natural Earth · 公有领域' : s.cr);
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
    { t: .13, type: 'marker', d: .35 }, { t: .3, type: 'pop' }, { t: .6, type: 'stamp' }, { t: .6, type: 'rattle', d: .45 },
    { t: 3.0, type: 'whoosh' }, { t: 3.05, type: 'riser', d: 2.5 }, { t: 5.55, type: 'stamp' }, { t: 5.55, type: 'rattle', d: .65 }, { t: 5.0, type: 'pop' },
    { t: 7.5, type: 'whoosh' }, ...[11.25, 11.4, 11.55, 11.7].map(t => ({ t, type: 'pop' })), { t: 11.25, type: 'rattle', d: .9 }, { t: 12.05, type: 'stamp' },
    { t: 14.5, type: 'whoosh' }, { t: 16.55, type: 'pop' }, { t: 16.85, type: 'punch' }, { t: 15.4, type: 'pop' }, { t: 15.6, type: 'pop' }, { t: 17.6, type: 'stamp' },
    { t: 20.0, type: 'paper' }, { t: 20.3, type: 'marker', d: 1.25 }, { t: 21.0, type: 'whoosh' },
    { t: 24.5, type: 'whoosh' }, ...FIRSTS.map((_, i) => ({ t: 25.0 + i * .2, type: 'tick' })),
    { t: 28.9, type: 'riser', d: 2.6 }, { t: 29.0, type: 'scroll', d: 2.5 }, { t: TF, type: 'shutter' }, { t: TF + .05, type: 'whoosh' }, { t: TF + .5, type: 'marker', d: .3 },
    { t: 35.0, type: 'hit' }, ...[35.3, 35.8, 36.3, 37.35].map(t => ({ t, type: 'ring' })), { t: 35.8, type: 'pop' }, { t: 36.6, type: 'riser', d: 2.8 }, { t: 37.35, type: 'stamp' },
    { t: 40.5, type: 'paper' }, { t: 40.8, type: 'marker', d: 1.55 }, { t: 43.4, type: 'marker', d: .85 }, { t: 44.0, type: 'stamp' }, { t: 44.96, type: 'marker', d: 1.0 },
    { t: 46.5, type: 'whoosh' }, { t: 46.8, type: 'rattle', d: .7 }, { t: 47.3, type: 'rattle', d: .7 }, { t: 49.0, type: 'stamp' },
    { t: 54.0, type: 'silence', d: 1.0 }, { t: 55.0, type: 'whoosh' }, { t: 58.0, type: 'verdict' },
  ];
  return ev.sort((a, b) => a.t - b.t);
}
(async () => {
  await Promise.all([900, 800, 600, 500].map(w => Promise.all([document.fonts.load(`${w} 40px SC`, '热榜'), document.fonts.load(`${w} 40px IT`, '0A')])));
  TL = await (await fetch('timeline.json')).json(); window.DUR = TL.dur;
  SHOTS = TL.shots; CAPS = TL.caps.map(c => [c.t0, c.t1, c.zh, c.en, c.big || 1]);
  LISTS = await (await fetch('assets/lists.json')).json(); ROWS = wallRows();
  MAP = await (await fetch('assets/map.json')).json();
  window.EV = buildEV();
  await load('assets/img/plateau.jpg');
  await render(0); window.READY = true;
})();
