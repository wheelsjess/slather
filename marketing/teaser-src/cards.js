const { chromium } = require('/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/t/node_modules/playwright');
const fs = require('fs'); const D = __dirname;
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await (await b.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
  await page.goto('file://' + D + '/cards.html'); await page.evaluate(() => document.fonts.load('64px "Press Start 2P"'));
  for (const [k, spec] of Object.entries(JSON.parse(fs.readFileSync(D + '/cards.json')))) {
    await page.evaluate(s => render(s), spec); await page.waitForTimeout(40);
    await page.screenshot({ path: `${D}/cards/${k}.png`, omitBackground: true });
  }
  await b.close(); console.log('cards done');
})();
