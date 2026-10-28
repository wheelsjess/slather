const { chromium } = require('/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/t/node_modules/playwright');
const D = __dirname;
const T = (html, size) => `<div class="t" style="font-size:${size}px">${html}</div>`;
const CARDS = {
  world: T('IN A WORLD...', 64), sun: T('WHERE<br>THE SUN...', 72), friend: T('IS NOT<br>YOUR FRIEND...', 64), summer: T('THIS<br>SUMMER...', 80),
  man: T('ONE MAN', 84), tube: T('ONE TUBE OF<br>SLATHER<br>SPF 50+', 68), ready: T('ARE READY TO<br>FIGHT BACK', 64),
  fight: T('ONE FIGHT<br>TO THE DEATH', 60), w_coming: T('COMING', 120), w_this: T('THIS', 120), w_summer: T('SUMMER', 120),
};
const BOX = 'A wild ESHAY<br>appeared!';
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const page = await (await b.newContext({ viewport: { width: 1080, height: 1920 } })).newPage();
  await page.goto('file://' + D + '/cards.html');
  await page.evaluate(() => Promise.all([document.fonts.load('64px "Press Start 2P"'), document.fonts.load('200px "Metal Mania"')]));
  for (const [k, h] of Object.entries(CARDS)) { await page.evaluate(h => render(h), h); await page.waitForTimeout(40); await page.screenshot({ path: `${D}/cards/${k}.png`, omitBackground: true }); }
  if (process.argv[2] !== 'box') { await b.close(); console.log('cards done'); return; }
  // the Pokemon-style text box, typed out a character at a time
  const plain = BOX.replace('<br>', '\n');
  for (let n = 0; n <= plain.length; n++) {
    const shown = plain.slice(0, n).replace('\n', '<br>');
    await page.evaluate(h => render(h), `<div class="box">${shown}</div>`); await page.screenshot({ path: `${D}/cards/box_${String(n).padStart(2, '0')}.png`, omitBackground: true });
  }
  await b.close(); console.log('cards done', plain.length + 1, 'box frames');
})();
