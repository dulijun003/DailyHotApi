const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
const FPS = 30, DUR = 10, only = process.argv[2];
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + __dirname + '/index.html');
  require('fs').mkdirSync(__dirname + '/frames', { recursive: true });
  const list = only ? only.split(',').map(Number) : [...Array(FPS * DUR).keys()];
  for (const i of list) {
    await p.evaluate(t => window.render(t), i / FPS);
    await p.screenshot({ path: `${__dirname}/frames/f${String(i).padStart(4, '0')}.png` });
  }
  await b.close();
})();
