// Records gameplay clips for the trailer. Each clip is its own browser context (= its own video); marks are ms since the context opened.
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const OUT = '/tmp/claude-0/-home-user-slather/21d9a6bc-cd97-5e18-a54d-642d51bfb159/scratchpad/trailer5/clips';
const HTMLX = { glare: h => h.replace('  else if (S.mode !== \'credits\') {\n    drawHUD();', '  else if (S.mode !== \'credits\') {'), beachsun: h => h.replace('const TITLE_T = { gull: 0.4, shine: 3.6, rise: 1.0, risen: 3.0, slam: 3.2,', 'const TITLE_T = { gull: 0.4, shine: 6.6, rise: 4.0, risen: 6.0, slam: 99,').replace('run: 4.0, arrive: 5.3, flip: 5.5, write: 6.0, written: 7.2, coin: 7.6, oldIn: 8.4, oldStop: 10.2, say: 10.3, toss: 13.0, catch: 13.7 }', 'run: 99, arrive: 99, flip: 99, write: 99, written: 99, coin: 99, oldIn: 99, oldStop: 99, say: 99, toss: 99, catch: 99 }') };
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
    const html2 = HTMLX[name] ? HTMLX[name](html) : html;
    await page.route('http://trailer.local/**', r => r.fulfill({ body: html2, contentType: 'text/html' }));
    await page.goto('http://trailer.local/'); await page.waitForTimeout(1500);
    const cdp = await ctx.newCDPSession(page), frames = [];
    cdp.on('Page.screencastFrame', async f => { const n = frames.length; fs.writeFileSync(`${dir}/${String(n).padStart(5, '0')}.jpg`, Buffer.from(f.data, 'base64')); frames.push(f.metadata.timestamp); cdp.send('Page.screencastFrameAck', { sessionId: f.sessionId }).catch(() => {}); });
    await cdp.send('Page.startScreencast', { format: 'jpeg', quality: 92, maxWidth: 1920, maxHeight: 1080, everyNthFrame: 1 });
    const t0 = Date.now() / 1000; const mark = k => { m[k] = Date.now() / 1000 - t0; };
    await page.evaluate(() => { window.__trk = []; setInterval(() => { const g = window.__slather; if (!g || !g.player) return;
      window.__trk.push({ t: Date.now() / 1000, p: [g.player.x, g.player.y - (g.player.liftZ || 0)], hands: g.boss.hands.map(h => [h.x, h.fy - h.z]),
        npcs: g.npcs.filter(n => n.kind === 'eshay' || n.state === 'burn' || n.state === 'held' || n.tag).map(n => [n.kind, n.state, n.x, n.y - (n.liftZ || 0), n.tag || '']),
        vans: g.vehicles.map(v => [v.x, v.y, v.state]) }); }, 40); });
    await fn(page, mark);
    fs.writeFileSync(`${dir}/track.json`, JSON.stringify((await page.evaluate(() => window.__trk)).map(o => ({ ...o, t: o.t - t0 }))));
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

  await clip('beachsun', async (page, mark) => { await page.keyboard.press('KeyA'); mark('open'); await page.waitForTimeout(8500); mark('end'); });
  await clip('glare', async (page, mark) => {
    await fight(page); await page.waitForTimeout(2600);
    await page.evaluate(() => { const g = window.__slather; const t0 = performance.now(); setInterval(() => { const k = Math.min(1, (performance.now() - t0) / 2600); g.boss.face = 'rage'; g.boss.eyeGlow = k; g.boss.headGlow = k * 0.6; }, 16); });
    mark('go'); await page.waitForTimeout(3200); await page.evaluate(() => { const g = window.__slather; g.boss.attack = g.ATTACKS.laser(); }); mark('fire'); await page.waitForTimeout(2500); mark('end');
  });
  await clip('roll', async (page, mark) => {
    await fight(page); await page.waitForTimeout(2600); mark('go');
    await page.evaluate(() => { const g = window.__slather; g.boss.attack = g.ATTACKS.laser(); });
    for (const [k, ms] of [['KeyA', 500], ['KeyD', 700], ['KeyA', 600], ['KeyD', 600]]) { await page.keyboard.down(k); await page.waitForTimeout(80); await page.keyboard.press('Space'); await page.waitForTimeout(ms); await page.keyboard.up(k); }
    mark('end');
  });
  await clip('slam', async (page, mark) => {
    await fight(page); await page.waitForTimeout(2600); mark('go');
    for (let i = 0; i < 3; i++) { await page.evaluate(() => { const g = window.__slather; g.boss.attack = g.ATTACKS.slam(); }); await page.waitForTimeout(2200); }
    mark('end');
  });
  fs.writeFileSync(OUT + '/marks.json', JSON.stringify(marks, null, 1));
  await b.close();
})();
