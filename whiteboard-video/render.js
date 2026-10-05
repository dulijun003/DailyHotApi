// Usage:
//   node render.js stills <outDir> t1 t2 ...     -> PNG stills at given times
//   node render.js video <out.mp4> [fps]         -> silent H.264 video
//   node render.js events <out.json>             -> pencil stroke timings (for SFX)
const { chromium } = require('playwright-core');
const { spawn } = require('child_process');
const fs = require('fs');
const path = require('path');

const CHROME = process.env.CHROME || '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';

(async () => {
  const [mode, out, ...rest] = process.argv.slice(2);
  const browser = await chromium.launch({ executablePath: CHROME, args: ['--font-render-hinting=none', '--disable-lcd-text'] });
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => console.error('PAGE ERROR', e));
  page.on('console', m => m.type() === 'error' && console.error('console:', m.text()));
  await page.goto('file://' + path.join(__dirname, 'index.html'));
  const duration = await page.evaluate(() => window.setup());
  const stage = await page.$('#stage');

  if (mode === 'stills') {
    fs.mkdirSync(out, { recursive: true });
    for (const t of rest.map(Number)) {
      await page.evaluate(t => window.renderAt(t), t);
      await stage.screenshot({ path: path.join(out, `${t.toFixed(2)}.png`) });
    }
  } else if (mode === 'events') {
    fs.writeFileSync(out, JSON.stringify(await page.evaluate(() => window.penEvents())));
  } else if (mode === 'video') {
    const fps = Number(rest[0] || 30);
    const n = Math.round(duration * fps);
    const ff = spawn('ffmpeg', ['-loglevel', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '16', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'inherit', 'inherit'] });
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.renderAt(t), i / fps);
      const buf = await stage.screenshot({ type: 'jpeg', quality: 95 });
      if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
      if (i % 60 === 0) process.stdout.write(`frame ${i}/${n}  ${((Date.now() - t0) / 1000).toFixed(0)}s\n`);
    }
    ff.stdin.end();
    await new Promise(r => ff.on('close', r));
  }
  await browser.close();
})();
