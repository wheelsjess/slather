const { chromium } = require('/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/t/node_modules/playwright');
const fs = require('fs'); const D = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
  await page.goto('file://' + D + '/cards.html');
  await page.evaluate(() => Promise.all(['96px Cinzel', '100px Anton', '40px "Press Start 2P"'].map(f => document.fonts.load(f))));
  const cards = JSON.parse(fs.readFileSync(D + '/cards.json'));
  for (const [k, blocks] of Object.entries(cards)) {
    await page.evaluate(b => render({ blocks: b }), blocks); await page.waitForTimeout(50);
    await page.screenshot({ path: `${D}/cards/${k}.png`, omitBackground: true });
  }
  await b.close(); console.log(Object.keys(cards).length, 'cards');
})();
