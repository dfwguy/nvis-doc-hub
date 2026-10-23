/** Meaningful live search browser tests. Real published content; timing/transport alone mocked for async edge cases. */
const { chromium, devices } = require('playwright');
const { expect } = require('playwright/test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const BASE = process.env.NVIS_HUB_URL || process.env.TARGET_URL || 'http://127.0.0.1:8000';
const ROOT = path.resolve(__dirname, '..');
const CAP = path.join(ROOT, '.impeccable/review');
const EVIDENCE = path.join(ROOT, 'evidence/live-search-browser-review.json');
const oldEvidence = fs.existsSync(EVIDENCE) ? JSON.parse(fs.readFileSync(EVIDENCE, 'utf8')) : {};
const red = oldEvidence.initialRed || (oldEvidence.phase === 'initial red' ? oldEvidence : null);
fs.mkdirSync(CAP, { recursive: true });
const record = { phase: 'full verification', at: new Date().toISOString(), target: BASE, initialRed: red, tests: [], captures: [], pageErrors: [], layout: [] };
const absolute = href => new URL(href, BASE).toString();
const deferred = () => { let resolve; const promise = new Promise(r => { resolve = r; }); return {promise, resolve}; };
(async () => {
  const browser = await chromium.launch({ headless: process.env.PW_HEADLESS === 'true' });
  record.browser = browser.version();
  const context = await browser.newContext({ viewport: { width: 1440, height: 1000 } });
  const page = await context.newPage();
  page.on('pageerror', error => record.pageErrors.push(error.message));
  const input = () => page.getByRole('combobox', { name: /Search.*documentation/ });
  const options = () => page.getByRole('listbox', { name: 'Matching documentation' }).getByRole('option');
  const popup = () => page.locator('.search-suggestions');
  const all = () => page.locator('.search-suggestions-all');
  async function visit(route = '/') {
    const response = await page.goto(BASE + route);
    assert(response.ok(), `HTTP ${response.status()} at ${route}`);
    await page.evaluate(() => document.fonts.ready);
  }
  async function type(q = 'slur') {
    await input().fill('');
    await input().pressSequentially(q, { delay: 25 });
    await options().first().waitFor({ state: 'visible' });
  }
  async function optionURLs() { return options().evaluateAll(nodes => nodes.map(node => node.getAttribute('href'))); }
  async function check(name, fn) {
    try { const detail = await fn(); record.tests.push({ name, status: 'passed', ...(detail ? { detail } : {}) }); console.log('PASS ' + name); }
    catch (error) { record.tests.push({ name, status: 'failed', error: error.message }); console.error('FAIL ' + name + ': ' + error.message); await page.screenshot({ path: path.join(CAP, 'live-search-failure-' + record.tests.length + '.png'), fullPage: true }).catch(() => {}); }
  }
  async function capture(name) { await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)))); await page.screenshot({ path: path.join(CAP, 'live-search-' + name + '.png'), fullPage: false }); record.captures.push('.impeccable/review/live-search-' + name + '.png'); }
  async function layout(name) {
    const metrics = await popup().evaluate(element => {
      const r = element.getBoundingClientRect(), field = document.querySelector('.search-field').getBoundingClientRect();
      const style = getComputedStyle(element), vv = window.visualViewport;
      return { x: r.x, top: r.top, bottom: r.bottom, width: r.width, height: r.height, fieldX: field.x, fieldWidth: field.width, fieldTop: field.top, fieldBottom: field.bottom, viewportWidth: innerWidth, viewportHeight: vv ? vv.height : innerHeight, viewportTop: vv ? vv.offsetTop : 0, scrollWidth: document.documentElement.scrollWidth, background: style.backgroundColor, border: style.borderColor, font: style.fontFamily, options: [...element.querySelectorAll('[role=option]')].map(option => ({ height: option.getBoundingClientRect().height, leftInset: parseFloat(getComputedStyle(option).paddingLeft), text: option.textContent.trim().slice(0, 160), href: option.getAttribute('href') })) };
    });
    record.layout.push({ name, ...metrics });
    assert(metrics.scrollWidth <= metrics.viewportWidth + 1, name + ': page must not overflow horizontally');
    assert(metrics.x >= 0 && metrics.x + metrics.width <= metrics.viewportWidth + 1, name + ': popup must fit viewport width');
    assert(metrics.top >= metrics.viewportTop - 1 && metrics.bottom <= metrics.viewportTop + metrics.viewportHeight + 1, name + ': popup must fit visible viewport height');
    assert(Math.abs(metrics.x - metrics.fieldX) <= 2 && Math.abs(metrics.width - metrics.fieldWidth) <= 2, name + ': popup aligns to input assembly');
    assert(metrics.options.every(option => option.height >= 44 && option.leftInset >= 12), name + ': options need touch targets and readable text inset');
    assert(metrics.font.includes('IBM Plex Sans'), name + ': font matches design system');
    assert(['rgb(26, 26, 26)', 'rgb(17, 17, 17)'].includes(metrics.background), name + ': popup is a neutral charcoal surface');
    return metrics;
  }
  try {
    await check('Real typing partial word opens accessible native section links', async () => {
      await visit(); await type();
      const data = await options().evaluateAll(nodes => nodes.map(n => ({ tag: n.tagName, href: n.getAttribute('href'), id: n.id, text: n.textContent.trim() })));
      assert(data.length > 0 && data.length <= 5);
      assert(data.every(n => n.tag === 'A' && /\/docs\/.+#.+/.test(n.href) && n.id && n.text.length > 30));
      await expect(input()).toHaveAttribute('aria-expanded', 'true');
      const listbox = page.getByRole('listbox', { name: 'Matching documentation' });
      await expect(listbox).toBeVisible();
      assert.equal(await input().getAttribute('aria-controls'), await listbox.getAttribute('id'));
      assert.equal(await input().evaluate(el => el === document.activeElement), true, 'typing retains focus');
      await expect(all()).toBeVisible();
      await expect(page.locator('.search-combobox [role=status]')).toContainText(/matching.*sections?/i);
      await expect(page.locator('.search-combobox [role=status]')).toHaveAttribute('aria-live', 'polite');
      assert(await input().getAttribute('aria-describedby'), 'combobox has keyboard help');
      const endpoint = await context.request.get(BASE + '/api/search/suggestions?q=slur');
      assert.equal(endpoint.status(), 200);
      const real = await endpoint.json();
      assert.deepEqual(data.map(n => n.href), real.map(n => absolute(n.url)));
      return data;
    });
    await check('Pointer click opens the actual indexed section anchor', async () => {
      await visit(); await type(); const href = await options().first().getAttribute('href');
      await options().first().click(); await page.waitForURL(absolute(href));
      const hash = decodeURIComponent(new URL(page.url()).hash.slice(1));
      assert(hash && await page.locator('[id]').evaluateAll((nodes, id) => nodes.some(n => n.id === id), hash));
      return { href, hash };
    });
    await check('Arrow keys select without moving input focus and Enter follows selection', async () => {
      await visit(); await type();
      await input().press('ArrowDown');
      const selectedId = await input().getAttribute('aria-activedescendant'); assert(selectedId);
      const selected = page.locator('[id=' + JSON.stringify(selectedId) + ']');
      await expect(selected).toHaveAttribute('aria-selected', 'true');
      assert.equal(await selected.evaluate(el => getComputedStyle(el).backgroundColor), 'rgb(38, 38, 38)', 'keyboard selection uses established active neutral');
      assert.equal(await selected.locator('.search-suggestion-title').evaluate(el => getComputedStyle(el).color), 'rgb(118, 185, 0)', 'result titles use NVIDIA Green');
      await capture('keyboard-selected');
      assert.equal(await input().evaluate(el => el === document.activeElement), true);
      await input().press('ArrowDown'); await input().press('ArrowUp');
      const selectedAfter = page.locator('[id=' + JSON.stringify(await input().getAttribute('aria-activedescendant')) + ']');
      const href = await selectedAfter.getAttribute('href');
      await input().press('Enter'); await page.waitForURL(absolute(href)); return { href };
    });
    await check('Unselected Enter preserves ordinary full search', async () => {
      await visit(); await type();
      assert(!await input().getAttribute('aria-activedescendant'));
      await input().press('Enter'); await page.waitForURL(url => url.pathname === '/search' && url.searchParams.get('q') === 'slur');
      assert.equal(new URL(page.url()).hash, '');
    });
    await check('Escape, Tab, clear, outside click and blur dismiss stale choices', async () => {
      for (const action of ['Escape', 'Tab', 'clear', 'outside', 'blur']) {
        await visit(); await type();
        if (action === 'clear') await input().fill('');
        else if (action === 'outside') await page.locator('h1').click();
        else if (action === 'blur') await page.locator('.sidebar').getByRole('link', { name: 'Source status', exact: true }).focus();
        else await input().press(action);
        await expect(popup(), action + ' dismisses suggestions').toBeHidden(); await expect(input()).toHaveAttribute('aria-expanded', 'false');
        assert(!await input().getAttribute('aria-activedescendant'), action + ' clears active selection');
      }
    });
    await check('One character stays quiet and typing is debounced', async () => {
      await visit(); const requests = [];
      const listener = request => { if (request.url().includes('/api/search/suggestions')) requests.push(new URL(request.url()).searchParams.get('q')); };
      page.on('request', listener);
      await input().fill('s'); await page.waitForTimeout(250);
      assert.deepEqual(requests, []); await expect(popup()).toBeHidden();
      await input().pressSequentially('lurm', { delay: 20 }); await options().first().waitFor({ state: 'visible' });
      page.off('request', listener); assert.deepEqual(requests, ['slurm']);
      return { requests };
    });
    await check('Full-search footer preserves query and available active filters', async () => {
      await visit('/search');
      const topic = await page.getByLabel('Topic', { exact: true }).locator('option').evaluateAll(nodes => nodes.find(n => /slurm|observability|compute/i.test(n.value))?.value || nodes.find(n => n.value)?.value || '');
      const kind = await page.getByLabel('Document type', { exact: true }).locator('option').evaluateAll(nodes => nodes.find(n => n.value === 'how-to')?.value || nodes.find(n => n.value)?.value || '');
      const scope = new URLSearchParams({project: 'cluster-bringup', ...(topic ? {topic} : {}), ...(kind ? {kind} : {})});
      await visit('/search?' + scope);
      await input().fill('slur');
      await expect(popup()).toBeVisible(); await expect(all()).toBeVisible();
      const href = await all().getAttribute('href'), url = new URL(href, BASE);
      for (const [key, value] of Object.entries({ q: 'slur', project: 'cluster-bringup', topic, kind })) assert.equal(url.searchParams.get(key) || '', value);
      const actual = await context.request.get(BASE + '/api/search/suggestions?' + url.searchParams.toString());
      const expected = await actual.json();
      await expect(options()).toHaveCount(expected.length);
      assert.deepEqual(await optionURLs(), expected.map(row => absolute(row.url)));
      await all().click(); await page.waitForURL(url.toString());
      return { href, returned: expected.length, topicAndKindFixture: topic || kind ? 'available' : 'Published sources have no topic/type facets; all-filter backend fixtures cover these constraints.' };
    });
    await check('Changing active filters clears old choices and uses updated scope', async () => {
      await visit('/search'); await type('configur'); const old = await optionURLs(); assert(old.length);
      await page.getByLabel('Project', { exact: true }).selectOption('documentation-pipeline');
      await page.waitForURL(url => url.pathname === '/search' && url.searchParams.get('project') === 'documentation-pipeline');
      assert.equal(new URL(page.url()).searchParams.get('q'), 'configur', 'auto-submitting a filter preserves the current query');
      assert.equal(await options().count(), 0, 'filter navigation clears stale choices');
      const requested = page.waitForRequest(request => request.url().includes('/api/search/suggestions') && new URL(request.url()).searchParams.get('project') === 'documentation-pipeline');
      await input().fill('');
      await input().fill('configur');
      await requested;
      await options().first().waitFor({ state: 'visible' });
      const actual = await context.request.get(BASE + '/api/search/suggestions?q=configur&project=documentation-pipeline');
      await expect.poll(optionURLs).toEqual((await actual.json()).map(row => absolute(row.url)));
      assert((await optionURLs()).every(url => url.includes('/projects/documentation-pipeline/')));
    });
    await check('Project index suggestions and full-search footer keep project scope', async () => {
      await visit('/projects/documentation-pipeline'); await type('configur');
      assert((await optionURLs()).every(url => url.includes('/projects/documentation-pipeline/')));
      assert.equal(new URL(await all().getAttribute('href'), BASE).searchParams.get('project'), 'documentation-pipeline');
    });
    await check('No-match feedback stays readable with full search available', async () => {
      await visit(); await input().fill('zzzz-no-documentation-matches');
      await expect(popup()).toBeVisible();
      await expect(page.locator('.search-suggestions-message')).toContainText(/no matching documentation/i);
      await expect(popup()).not.toHaveAttribute('aria-busy', 'true');
      await expect(options()).toHaveCount(0); await expect(all()).toBeVisible(); await capture('no-match');
      return { message: await page.locator('.search-suggestions-message').textContent() };
    });
    await check('Loading clears stale options, announces progress, and recovers to real results', async () => {
      await visit(); await type();
      const pending = deferred(), release = deferred();
      await page.route('**/api/search/suggestions**', async route => { const response = await route.fetch(); pending.resolve(); await release.promise; await route.fulfill({ response }); });
      await input().fill('configur');
      assert.equal(await options().count(), 0, 'query changes clear stale options before the next request');
      assert(!await input().getAttribute('aria-activedescendant'));
      await pending.promise;
      await expect(popup()).toContainText(/searching|loading/i); await expect(options()).toHaveCount(0); await expect(all()).toBeVisible();
      await capture('loading'); release.resolve(); await options().first().waitFor({ state: 'visible' });
      await page.unroute('**/api/search/suggestions**');
    });
    await check('Transport failure preserves full search and next typing recovers', async () => {
      await visit(); await page.route('**/api/search/suggestions**', route => route.abort('failed'));
      await input().fill('slur');
      await expect(popup()).toContainText(/unable|unavailable|couldn.t|failed|try.*again/i);
      await expect(options()).toHaveCount(0); await expect(all()).toBeVisible(); await capture('request-error');
      const href = await all().getAttribute('href'); assert.equal(new URL(href, BASE).searchParams.get('q'), 'slur');
      await page.unroute('**/api/search/suggestions**'); await type('slurm');
    });
    await check('A late old response cannot replace newer results even if transport ignores abort', async () => {
      const racePage = await context.newPage();
      try {
        await racePage.addInitScript(() => {
          const original = window.fetch;
          window.fetch = async function(resource, init) {
            const url = new URL(resource, location.href);
            if (!url.pathname.endsWith('/api/search/suggestions')) return original.call(this, resource, init);
            const response = await original.call(this, resource, { ...init, signal: undefined });
            if (url.searchParams.get('q') === 'slur') await new Promise(resolve => setTimeout(resolve, 650));
            return response;
          };
        });
        await racePage.goto(BASE);
        const oldRequest = racePage.waitForResponse(response => response.url().includes('/api/search/suggestions') && new URL(response.url()).searchParams.get('q') === 'slur');
        await racePage.getByRole('combobox', { name: /Search.*documentation/ }).fill('slur'); await oldRequest;
        await racePage.getByRole('combobox', { name: /Search.*documentation/ }).fill('configur');
        const response = await context.request.get(BASE + '/api/search/suggestions?q=configur'); const expected = (await response.json()).map(row => absolute(row.url));
        const urls = () => racePage.getByRole('listbox', { name: 'Matching documentation' }).getByRole('option').evaluateAll(nodes => nodes.map(n => n.getAttribute('href')));
        await expect.poll(urls).toEqual(expected); await racePage.waitForTimeout(750); assert.deepEqual(await urls(), expected);
        return { newerQuery: 'configur', urls: expected, delayedOldResponseMs: 650 };
      } finally { await racePage.close(); }
    });
    await check('IME composition waits for commit and composing Enter keeps the page', async () => {
      await visit(); const requests = []; const listener = request => { if (request.url().includes('/api/search/suggestions')) requests.push(request.url()); }; page.on('request', listener);
      await input().dispatchEvent('compositionstart'); await input().fill('slur');
      await input().dispatchEvent('keydown', { key: 'Enter', code: 'Enter', isComposing: true, bubbles: true, cancelable: true });
      await page.waitForTimeout(270); assert.equal(requests.length, 0); assert.equal(new URL(page.url()).pathname, '/');
      await input().dispatchEvent('compositionend', { data: 'slur' }); await options().first().waitFor({ state: 'visible' });
      page.off('request', listener); assert.equal(requests.length, 1);
    });
    for (const viewport of [ { name: 'desktop', width: 1440, height: 1000 }, { name: 'tablet', width: 768, height: 1024 }, { name: 'phone', width: 390, height: 844 } ]) {
      for (const route of [ { name: 'catalog', path: '/', q: 'slur' }, { name: 'search', path: '/search', q: 'slur' }, { name: 'project', path: '/projects/cluster-bringup', q: 'slur' } ]) {
        await check(viewport.name + ' ' + route.name + ' popup layout', async () => {
          await page.setViewportSize({ width: viewport.width, height: viewport.height }); await visit(route.path); await type(route.q);
          await input().scrollIntoViewIfNeeded(); await capture(viewport.name + '-' + route.name); const metrics = await layout(viewport.name + '-' + route.name);
          const last = options().last(); await last.scrollIntoViewIfNeeded();
          const href = await last.getAttribute('href'); await last.click(); await page.waitForURL(absolute(href));
          return { width: metrics.width, height: metrics.height, options: metrics.options.length, lastOptionHref: href };
        });
      }
    }
    await check('Short viewport flips popup above field and caps scrolling', async () => {
      await page.setViewportSize({ width: 1440, height: 500 }); await visit('/projects/cluster-bringup'); await type();
      const metrics = await layout('short-viewport-above');
      assert(metrics.bottom <= metrics.fieldTop + 1, 'popup should use larger available area above field');
      await capture('short-viewport-above');
      await options().last().scrollIntoViewIfNeeded(); await expect(options().last()).toBeVisible();
    });
    await check('Phone visible viewport resize preserves bounded popup and reachable footer', async () => {
      await page.setViewportSize({ width: 390, height: 844 }); await visit('/'); await type();
      await page.setViewportSize({ width: 390, height: 420 });
      await expect.poll(() => popup().evaluate(el => el.getBoundingClientRect().bottom <= innerHeight + 1)).toBe(true);
      await layout('phone-keyboard-sized-viewport'); await capture('phone-short-viewport');
      await all().scrollIntoViewIfNeeded(); await capture('phone-short-viewport-footer'); const href = await all().getAttribute('href'); await all().click(); await page.waitForURL(absolute(href));
    });
    await check('Touch selects a native result on a phone', async () => {
      const phone = await browser.newContext(devices['iPhone 13']); const touch = await phone.newPage();
      try {
        await touch.goto(BASE); await touch.getByRole('combobox', { name: /Search.*documentation/ }).tap(); await touch.getByRole('combobox', { name: /Search.*documentation/ }).fill('slur');
        const option = touch.getByRole('listbox', { name: 'Matching documentation' }).getByRole('option').first(); await option.waitFor({ state: 'visible' }); const href = await option.getAttribute('href');
        await option.tap(); await touch.waitForURL(absolute(href)); return { href };
      } finally { await phone.close(); }
    });
    await check('JavaScript-free form and filters preserve full search fallback', async () => {
      const plain = await browser.newContext({ javaScriptEnabled: false, viewport: { width: 1440, height: 900 } }); const noJS = await plain.newPage();
      try {
        await noJS.goto(BASE); await noJS.getByRole('searchbox', { name: /Search.*documentation/ }).fill('slurm');
        await noJS.getByRole('button', { name: 'Search', exact: false }).click(); await noJS.waitForURL(url => url.pathname === '/search' && url.searchParams.get('q') === 'slurm');
        assert(await noJS.locator('.search-result').count() > 0);
        await noJS.getByLabel('Project', { exact: true }).selectOption('cluster-bringup');
        await noJS.getByRole('button', { name: 'Apply filters' }).click(); await noJS.waitForURL(/project=cluster-bringup/);
        assert((await noJS.locator('.result-context').allTextContents()).every(text => text.includes('Cluster Bringup')));
      } finally { await plain.close(); }
    });
    await check('No browser script errors during live search interactions', async () => { assert.deepEqual(record.pageErrors, []); });
  } finally {
    record.passed = record.tests.filter(t => t.status === 'passed').length;
    record.failed = record.tests.filter(t => t.status === 'failed').length;
    fs.writeFileSync(EVIDENCE, JSON.stringify(record, null, 2) + '\n');
    console.log(`Live search verification: ${record.passed} passed, ${record.failed} failed.`);
    await browser.close(); if (record.failed) process.exitCode = 1;
  }
})().catch(error => { console.error(error); process.exitCode = 1; });
