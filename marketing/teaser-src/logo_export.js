// pulls the title logo art (SLATHER chrome + SUN FIGHTER brush) out of the game as transparent PNGs
const { chromium } = require('/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/t/node_modules/playwright'); const fs = require('fs');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await (await b.newContext({ viewport: { width: 960, height: 540 } })).newPage();
  const html = fs.readFileSync('/home/user/slather/index.html', 'utf8').replace('  TITLE_ART = { sky, land, slat, fight, sheen, aura, embers: [] };', '  TITLE_ART = { sky, land, slat, fight, sheen, aura, embers: [] }; window.__TA = TITLE_ART;');
  await page.route('http://trailer.local/**', r => r.fulfill({ body: html, contentType: 'text/html' }));
  await page.goto('http://trailer.local/'); await page.keyboard.press('KeyA'); await page.waitForTimeout(3000);
  const urls = await page.evaluate(() => ({ slat: window.__TA.slat.toDataURL(), fight: window.__TA.fight.toDataURL() }));
  for (const [k, u] of Object.entries(urls)) fs.writeFileSync(`${__dirname}/${k}.png`, Buffer.from(u.split(',')[1], 'base64'));
  await b.close(); console.log('logo saved');
})();
