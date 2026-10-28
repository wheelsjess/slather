// Records gameplay clips for the trailer. Each clip is its own browser context (= its own video); marks are ms since the context opened.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const OUT = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer2/clips';
const only = process.argv[2];
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const marks = fs.existsSync(OUT + '/marks.json') ? JSON.parse(fs.readFileSync(OUT + '/marks.json')) : {};
  async function clip(name, fn) {
    if (only && only !== name) return;
    const ctx = await b.newContext({ viewport: { width: 1920, height: 1080 } });
    const page = await ctx.newPage(), m = {}, dir = `${OUT}/${name}`; fs.rmSync(dir, { recursive: true, force: true }); fs.mkdirSync(dir);
    page.on('pageerror', e => console.log(name, 'ERR', e.message));
    // serve the game with the on-screen chrome stripped (buttons, "ENTER TO SKIP") so the footage is clean
    const html = fs.readFileSync('/home/user/slather/index.html', 'utf8').replace(/'ENTER TO SKIP'/g, "''").replace(/'TAP TO SKIP'/g, "''").replace("'HIT ENTER TO INSERT COIN'", "''")
      .replace('</style>', '.ui{display:none!important}</style>');
    await page.route('http://trailer.local/**', r => r.fulfill({ body: html, contentType: 'text/html' }));
    await page.goto('http://trailer.local/'); await page.waitForTimeout(1500);
    const cdp = await ctx.newCDPSession(page), frames = [];
    cdp.on('Page.screencastFrame', async f => { const n = frames.length; fs.writeFileSync(`${dir}/${String(n).padStart(5, '0')}.jpg`, Buffer.from(f.data, 'base64')); frames.push(f.metadata.timestamp); cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
    await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });
    const t0 = Date.now() / 1000; const mark = k => { m[k] = Date.now() / 1000 - t0; };
    await fn(page, mark);
    await cdp.send('Page.stopScreencast'); await page.waitForTimeout(300); await ctx.close();
    fs.writeFileSync(`${dir}/times.json`, JSON.stringify(frames.map(t => t - t0)));
    marks[name] = m; console.log(name, frames.length, 'frames', JSON.stringify(m));
  }
  const fight = async page => {
    await page.evaluate(() => { const g = window.__slather; g.S.ttl.t = 99; g.startLoading(); g.S.load.t = 99; });
    await page.keyboard.press('Enter'); await page.waitForTimeout(200); await page.keyboard.press('Enter'); await page.waitForTimeout(600);
    await page.evaluate(() => { const g = window.__slather; g.boss.cooldown = 99999; setInterval(() => { g.player.hp = 100; g.player.burn = 0; }, 100); });
  };
  const atk = (page, a) => page.evaluate(a => { const g = window.__slather; g.boss.attack = g.ATTACKS[a](); }, a);

  await clip('title', async (page, mark) => {
    await page.keyboard.press('KeyA'); mark('open'); await page.waitForTimeout(17500); mark('end');
  });
  await clip('lasers', async (page, mark) => {
    await fight(page); await page.waitForTimeout(1200); mark('go'); await atk(page, 'laser'); await page.waitForTimeout(3500);
    mark('rays'); await atk(page, 'rays'); await page.waitForTimeout(3500); mark('end');
  });
  await clip('phase3', async (page, mark) => {
    await fight(page); await page.evaluate(() => { const g = window.__slather; g.boss.hp = 1700; g.hurtBoss(10); }); await page.waitForTimeout(3500);
    await page.evaluate(() => { const g = window.__slather; g.boss.hp = 700; g.boss.invuln = 0; g.hurtBoss(10); }); mark('p3'); await page.waitForTimeout(4500);
    mark('flare'); await atk(page, 'flare'); await page.waitForTimeout(4500); mark('slam'); await atk(page, 'slam'); await page.waitForTimeout(2500); mark('end');
  });
  await clip('grab', async (page, mark) => {
    await fight(page); await page.waitForTimeout(800);
    await page.evaluate(() => { const g = window.__slather; g.player.hurtT = 0; g.player.iframe = 0; const R = Math.random; Math.random = () => 0.9; g.boss.attack = g.ATTACKS.grab(); setTimeout(() => Math.random = R, 120); });
    mark('go'); await page.waitForTimeout(6000); mark('end');
  });
  await clip('eshay', async (page, mark) => {
    await fight(page); await page.waitForTimeout(800); mark('go'); await page.evaluate(() => window.__slather.spawnEshay()); await page.waitForTimeout(7000); mark('end');
  });
  await clip('van', async (page, mark) => {
    await fight(page); await page.waitForTimeout(600);
    await page.evaluate(() => { const g = window.__slather; g.spawnVan(); const v = g.vehicles[0]; v.dir = 1; v.x = 60; }); mark('go');
    await page.waitForTimeout(2600); await page.evaluate(() => { const g = window.__slather; g.igniteVan(g.vehicles[0]); }); mark('boom'); await page.waitForTimeout(4000); mark('end');
  });
  await clip('finish', async (page, mark) => {
    await fight(page); await page.evaluate(() => { const g = window.__slather; g.S.phase = 3; });
    const M = 3300; await page.evaluate(m => { const g = window.__slather; g.boss.hp = m * 0.065; g.boss.trail = m * 0.065; }, M); await page.waitForTimeout(1500);
    mark('hit'); await page.evaluate(m => { const g = window.__slather; g.boss.invuln = 0; g.hurtBoss(m * 0.05); }, M); await page.waitForTimeout(3500);
    mark('kill'); await page.evaluate(() => { const g = window.__slather; g.boss.invuln = 0; g.boss.hp = 5; g.hurtBoss(10); }); await page.waitForTimeout(9000); mark('end');
  });
  await clip('attack', async (page, mark) => {
    await fight(page); await page.evaluate(() => { const g = window.__slather; setInterval(() => { g.player.dual = 99; }, 100); });
    await page.waitForTimeout(2600); mark('go');
    const moves = [['KeyA', 900], ['KeyD', 1600], ['KeyA', 1300], ['KeyD', 1200]];
    for (const [k, ms] of moves) { await page.keyboard.down(k); const until = Date.now() + ms; while (Date.now() < until) { await page.keyboard.press('KeyJ'); await page.waitForTimeout(90); } await page.keyboard.up(k); }
    mark('end');
  });
  await clip('burnt', async (page, mark) => {
    await fight(page); await page.waitForTimeout(800);
    await page.evaluate(() => { for (const id of Array(9999).keys()) clearInterval(id); const g = window.__slather; g.player.hp = 1; g.player.hurtT = 0; g.player.iframe = 0; g.hurt(50, {}); });
    mark('die'); await page.waitForTimeout(7000); mark('end');
  });
  fs.writeFileSync(OUT + '/marks.json', JSON.stringify(marks, null, 1));
  await b.close();
})();
