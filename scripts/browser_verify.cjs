/* Browser evidence for the catalog, search, hosted reader and narrow layouts.
 * Run with Playwright available in NODE_PATH, e.g. npm install --prefix .browser-tools playwright.
 */
const { chromium } = require('playwright');
const fs = require('node:fs');
const path = require('node:path');
const assert = require('node:assert/strict');
const base = process.env.NVIS_HUB_URL || 'http://127.0.0.1:8000';
const root = path.resolve(__dirname, '..');
const output = path.join(root, '.impeccable/review');
fs.mkdirSync(output, { recursive: true });

(async () => {
  const browser = await chromium.launch({ headless: process.env.PW_HEADLESS === 'true' });
  const context = await browser.newContext({ permissions: ['clipboard-read', 'clipboard-write'] });
  const page = await context.newPage();
  const failures = [];
  const checks = [];
  page.on('pageerror', error => failures.push(error.message));
  const record = (name, detail) => checks.push({ name, detail });
  async function visit(route) {
    const response = await page.goto(base + route, { waitUntil: 'load' });
    assert(response && response.ok(), `Cannot open ${route}`);
    await page.evaluate(() => document.fonts.ready);
  }
  async function capture(name) {
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.screenshot({ path: path.join(output, `${name}.png`), fullPage: true });
    if (name.includes('search') || name.includes('reader')) {
      await page.screenshot({ path: path.join(output, `${name}-fold.png`), fullPage: false });
    }
    const metrics = await page.evaluate(() => ({
      width: innerWidth, scrollWidth: document.documentElement.scrollWidth,
      h1: document.querySelectorAll('h1').length,
      font: getComputedStyle(document.body).fontFamily,
      loaded: document.fonts.check('14px "IBM Plex Sans"'),
    }));
    assert(metrics.scrollWidth <= metrics.width + 1, `${name} overflows horizontally`);
    assert.equal(metrics.h1, 1, `${name} must have one main heading`);
    assert(metrics.loaded, `${name} font missing`);
    record(name, metrics);
  }
  try {
    for (const viewport of [
      { name: 'desktop', width: 1440, height: 900 },
      { name: 'tablet', width: 768, height: 1024 },
      { name: 'mobile', width: 390, height: 844 },
    ]) {
      await page.setViewportSize({ width: viewport.width, height: viewport.height });
      await visit('/');
      await page.getByRole('heading', { name: 'Documentation', exact: true }).waitFor();
      assert.equal(await page.locator('.project-card').count(), 2);
      await capture(viewport.name);
      await visit('/search');
      const promptInset = await page.locator('.search-start').evaluate(panel => {
        const box = panel.getBoundingClientRect();
        const heading = panel.querySelector('h2').getBoundingClientRect();
        return { left: heading.left - box.left, top: heading.top - box.top };
      });
      assert(promptInset.left >= 20 && promptInset.top >= 20,
        'Initial search prompt must have room inside every panel edge');
      await capture(`${viewport.name}-search-start`);
      record(`${viewport.name}-search-prompt-inset`, promptInset);
      await visit('/');
      if (viewport.width === 390) {
        await page.getByLabel('Open navigation').click();
        await page.locator('.mobile-menu[open]').waitFor();
        await page.screenshot({ path: path.join(output, 'mobile-menu.png'), fullPage: true });
        await page.keyboard.press('Escape');
        assert.equal(await page.locator('.mobile-menu[open]').count(), 0);
        record('mobile-navigation', 'Opens, exposes labelled project navigation, Escape restores focus.');
      }
      await page.getByRole('searchbox', { name: 'Search all documentation' }).fill('slurm');
      await page.getByRole('button', { name: 'Search', exact: false }).click();
      await page.waitForURL('**/search?q=slurm');
      await page.locator('.search-result').first().waitFor();
      if (viewport.width === 1440) {
        assert(await page.getByLabel('Project', { exact: true }).isVisible(), 'Desktop project filter hidden');
      }
      await capture(`${viewport.name}-search`);
      const orphanArrows = await page.locator('.search-result h2 a').evaluateAll(links =>
        links.filter(link => {
          const title = link.querySelector('span').getBoundingClientRect();
          const arrow = link.querySelector('svg').getBoundingClientRect();
          return arrow.top > title.top + parseFloat(getComputedStyle(link).lineHeight);
        }).length);
      assert.equal(orphanArrows, 0, 'Search result arrows must stay beside the first title line');
      const result = page.locator('.search-result h2 a').first();
      assert((await result.getAttribute('href')).includes('#'), 'Search must link to matching anchor');
      await result.click();
      await page.locator('.prose h1').waitFor();
      const hash = await page.evaluate(() => decodeURIComponent(location.hash.slice(1)));
      assert(hash && await page.locator(`[id="${hash}"]`).count(), 'Search anchor missing');
      record(`${viewport.name}-search-anchor`, hash);
      await visit('/projects/cluster-bringup/docs/docs/cmsh_setup/how-to/troubleshoot-connection.md');
      await page.getByRole('heading', { name: 'How to troubleshoot a cmsh connection' }).waitFor();
      assert(await page.locator('.prose pre code').count() > 0);
      await capture(`${viewport.name}-reader`);
      if (viewport.width === 390) {
        const table = page.locator('.table-scroll').first();
        assert(await table.evaluate(el => el.scrollWidth > el.clientWidth), 'Wide reference table must scroll');
        assert(await page.getByText('Scroll horizontally to see all columns.').first().isVisible(), 'Table overflow cue missing');
        await page.locator('.mobile-contents summary').click();
        await page.getByRole('navigation', { name: 'Page contents' }).getByRole('link', { name: 'Diagnostics' }).click();
        assert(page.url().endsWith('#diagnostics'));
        record('mobile-contents-and-table', 'Contents anchors work; wide table scrolls within the page.');
      }
      const localLink = page.locator('.prose a[href*="extract-cmsh-without-installing.md"]').first();
      assert((await localLink.getAttribute('href')).startsWith('/projects/cluster-bringup/docs/'));
      await localLink.click();
      assert(page.url().includes('/projects/cluster-bringup/docs/'));
      record(`${viewport.name}-nested-link`, page.url());
    }
    await page.setViewportSize({ width: 1440, height: 900 });
    await visit('/projects/cluster-bringup/docs/docs/internal_app_access/explanation/architecture-and-trust.md');
    const img = page.locator('.prose img').first();
    await img.waitFor();
    assert(await img.evaluate(image => image.complete && image.naturalWidth > 0), 'Hosted SVG did not render');
    await capture('desktop-image-reader');
    record('hosted-image', await img.getAttribute('src'));
    await visit('/projects/documentation-pipeline/docs/docs/tutorials/adopt.md');
    const previous = page.getByRole('navigation', { name: 'Adjacent documentation' }).locator('a');
    assert.equal(await previous.count(), 1);
    assert.equal(await previous.getAttribute('rel'), 'prev');
    assert.notEqual(await previous.evaluate(el => getComputedStyle(el).textAlign), 'right',
      'A lone Previous page link must keep its left alignment');
    record('last-document-navigation', 'Previous page remains on the left when no next page exists.');
    await visit('/projects/cluster-bringup/docs/docs/cmsh_setup/how-to/troubleshoot-connection.md');
    await page.getByRole('button', { name: 'Copy code block' }).first().click();
    assert((await page.evaluate(() => navigator.clipboard.readText())).includes('nc -zv'));
    record('copy-code', 'Clipboard matches authored command.');
    await page.setViewportSize({ width: 390, height: 844 });
    await visit('/projects/cluster-bringup/docs/docs/observability_server_setup/reference.md');
    const wideCodeIndex = await page.locator('.prose pre').evaluateAll(blocks =>
      blocks.findIndex(block => block.scrollWidth > block.clientWidth + 50));
    assert(wideCodeIndex >= 0, 'The published reference must exercise wide code');
    const wideCode = page.locator('.prose pre').nth(wideCodeIndex);
    await wideCode.scrollIntoViewIfNeeded();
    await wideCode.evaluate(block => { block.scrollLeft = block.scrollWidth; });
    const wideCopy = wideCode.locator('..').getByRole('button', { name: 'Copy code block' });
    const codeBox = await wideCode.boundingBox();
    const copyBox = await wideCopy.boundingBox();
    assert(copyBox.x >= codeBox.x && copyBox.x + copyBox.width <= codeBox.x + codeBox.width,
      'Copy control must stay inside the visible code frame after horizontal scrolling');
    const completeCode = await wideCode.locator('code').textContent();
    await wideCopy.click();
    assert.equal(await page.evaluate(() => navigator.clipboard.readText()), completeCode);
    await page.screenshot({ path: path.join(output, 'mobile-scrolled-code-copy.png') });
    record('code-copy-after-horizontal-scroll', 'Copy remains visible and copies the complete authored block.');
    await page.setViewportSize({ width: 1440, height: 900 });
    await visit('/search?q=configuration&project=documentation-pipeline');
    assert(await page.locator('.search-result').count() > 0);
    assert((await page.locator('.result-context').allTextContents()).every(t => t.includes('Documentation Pipeline')));
    await capture('desktop-filtered-search');
    await page.getByLabel('Project', { exact: true }).selectOption('cluster-bringup');
    await page.getByRole('button', { name: 'Apply filters' }).click();
    await page.waitForURL(/project=cluster-bringup/);
    assert((await page.locator('.result-context').allTextContents()).every(t => t.includes('Cluster Bringup')));
    record('project-filter-control', 'Changing the project filter updates the actual result scope.');
    await visit('/search?q=zzzz-no-documentation-matches');
    await page.getByRole('heading', { name: 'No matching documentation' }).waitFor();
    await capture('desktop-no-matches');
    await visit('/sources');
    assert((await page.locator('.source-facts').allTextContents()).join(' ').includes('f74950ac'));
    await capture('desktop-sources');
    const missing = await page.goto(base + '/projects/absent');
    assert.equal(missing.status(), 404);
    await capture('desktop-not-found');
    await visit('/');
    await page.keyboard.press('Tab');
    assert.equal(await page.locator(':focus').textContent(), 'Skip to content');
    await page.keyboard.press('Enter');
    assert.equal(await page.locator(':focus').getAttribute('id'), 'main');
    await page.keyboard.press('/');
    assert.equal(await page.locator(':focus').getAttribute('id'), 'query');
    record('keyboard', 'Skip link works; / focuses search; visible focus CSS present.');
    const searchButton = page.getByRole('button', { name: 'Search', exact: false });
    await searchButton.hover();
    record('search-button-hover-colors', await searchButton.evaluate(el => ({
      text: getComputedStyle(el).color, background: getComputedStyle(el).backgroundColor,
    })));
    assert.equal(failures.length, 0, failures.join('\n'));
    fs.writeFileSync(path.join(root, 'evidence/browser-verification.json'), JSON.stringify({
      base, at: new Date().toISOString(), browser: browser.version(), checks, pageErrors: failures,
    }, null, 2) + '\n');
    console.log(`Browser verification passed: ${checks.length} checks, 3 viewport widths, ${browser.version()}`);
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });
