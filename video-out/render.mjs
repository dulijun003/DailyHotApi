import { createRequire } from 'module';
import http from 'http'; import fs from 'fs'; import path from 'path'; import { spawn } from 'child_process';
const require = createRequire('/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const root = path.dirname(new URL(import.meta.url).pathname);
const types = { '.html':'text/html', '.css':'text/css', '.woff2':'font/woff2', '.woff':'font/woff' };
const srv = http.createServer((q, r) => { const p = path.join(root, decodeURIComponent(q.url.split('?')[0])); fs.readFile(p, (e, d) => { if (e) { r.writeHead(404); r.end(); return; } r.writeHead(200, { 'content-type': types[path.extname(p)] || 'application/octet-stream' }); r.end(d); }); }).listen(8765);
const [mode, arg] = process.argv.slice(2); // "stills 1,2,3" | "video out.mp4"
const browser = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto('http://localhost:8765/index.html?render', { waitUntil: 'networkidle' });
await page.evaluate(() => document.fonts.ready);
await page.waitForTimeout(500);
if (mode === 'stills') {
  for (const t of arg.split(',')) { await page.evaluate(t => seek(t), +t); await page.screenshot({ path: `still_${t}.png` }); }
} else {
  const fps = 30, total = await page.evaluate(() => TOTAL);
  const ff = spawn('ffmpeg', ['-y','-f','image2pipe','-framerate',String(fps),'-c:v','mjpeg','-i','-','-c:v','libx264','-pix_fmt','yuv420p','-crf','18','-preset','medium','-movflags','+faststart', arg], { stdio: ['pipe','ignore','inherit'] });
  for (let i = 0; i < total * fps; i++) {
    await page.evaluate(t => seek(t), i / fps);
    const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
    if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
    if (i % 300 === 0) console.log('frame', i);
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
}
await browser.close(); srv.close();
