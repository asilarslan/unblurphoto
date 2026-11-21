// node tools/og.js → assets/img/og.jpg (1200×630 share image)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch({ channel: process.env.PW_CHANNEL || undefined });
  const p = await b.newPage({ viewport: { width: 1200, height: 630 } });
  await p.goto('file://' + path.join(__dirname, 'og.html'));
  await p.waitForTimeout(300);
  await p.screenshot({ path: path.join(__dirname, '../assets/img/og.jpg'), type: 'jpeg', quality: 85 });
  await b.close();
})();
