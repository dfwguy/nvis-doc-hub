/* Native category navigation browser verification. Run with Playwright in NODE_PATH. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { chromium } = require('playwright');
const base = process.env.NVIS_HUB_URL || 'http://127.0.0.1:8000';
const root = process.env.NVIS_HUB_ROOT || path.resolve(__dirname, '..');
const output = path.join(root, '.impeccable/review');
const evidencePath = path.join(root, 'evidence/collapsible-navigation-browser.json');
const checks = [];
const pageErrors = [];
fs.mkdirSync(output, { recursive: true });
const record = (name, detail) => checks.push({ name, detail });
const valueSet = values => [...new Set(values)].sort();
const projectRoute = slug => `/projects/${slug}`;
async function openAll(groups) {
  for (const group of await groups.all()) {
    if (await group.getAttribute('open') === null) await group.locator('summary').first().click();
  }
}
async function menuMetrics(menu) {
  return menu.locator('.mobile-menu-body').evaluate(panel => {
    const box = panel.getBoundingClientRect();
    return {
      left: box.left, right: box.right, top: box.top, bottom: box.bottom,
      width: box.width, scrollWidth: panel.scrollWidth, clientWidth: panel.clientWidth,
      overflowingDescendants: [...panel.querySelectorAll('*')]
        .filter(el => el instanceof HTMLElement && el.scrollWidth > el.clientWidth + 1)
        .map(el => ({tag: el.tagName, className: el.className,
          scrollWidth: el.scrollWidth, clientWidth: el.clientWidth})),
    };
  });
}
function assertMenuContained(bounds, viewportWidth, name) {
  assert(bounds.left >= 0 && bounds.right <= viewportWidth + 1,
    `${name}: menu stays within viewport`);
  assert(bounds.scrollWidth <= bounds.clientWidth + 1,
    `${name}: menu scroll container has no horizontal overflow`);
  assert.deepEqual(bounds.overflowingDescendants, [],
    `${name}: menu descendants have no horizontal overflow`);
}
async function checkDisclosure(group, input, prefix) {
  const summary = group.locator('summary').first();
  const firstLink = group.locator('a[href*="/docs/"]').first();
  assert.equal(await group.getAttribute('open'), null, `${prefix}: starts collapsed`);
  assert.equal(await firstLink.isVisible(), false, `${prefix}: hidden links stay hidden`);
  if (input === 'mouse') await summary.click();
  else { await summary.focus(); await summary.press('Enter'); }
  await firstLink.waitFor({state: 'visible'});
  assert.notEqual(await group.getAttribute('open'), null, `${prefix}: expands`);
  if (input === 'mouse') await summary.click();
  else await summary.press('Space');
  assert.equal(await group.getAttribute('open'), null, `${prefix}: collapses`);
  record(prefix, `${input}: hidden links become visible; disclosure closes again`);
}
(async () => {
  const browser = await chromium.launch({headless: process.env.PW_HEADLESS === 'true'});
  const context = await browser.newContext({viewport: {width: 1440, height: 1000}});
  const page = await context.newPage();
  page.on('pageerror', error => pageErrors.push(error.message));
  async function visit(route, target = page) {
    const response = await target.goto(base + route, {waitUntil: 'load'});
    assert(response && response.ok(), `Cannot open ${route}`);
    await target.evaluate(() => document.fonts.ready);
  }
  async function capture(name, target = page) {
    await target.evaluate(() => window.scrollTo(0, 0));
    await target.screenshot({path: path.join(output, `categories-${name}.png`), fullPage: name.endsWith('index-expanded')});
    if (name.endsWith('index-expanded')) await target.screenshot({path: path.join(output, `categories-${name}-fold.png`), fullPage: false});
  }
  try {
    const projectResponse = await context.request.get(base + '/api/projects');
    assert(projectResponse.ok(), 'Project count API responds');
    const projects = await projectResponse.json();
    assert.equal(projects.length, 2, 'Both registered projects remain available');
    const inventories = [];
    for (const project of projects) {
      await visit(projectRoute(project.slug));
      const groups = page.locator('details.document-category');
      assert(await groups.count() > 0, `${project.slug}: native document disclosures exist`);
      assert.equal(await groups.locator('summary').count(), await groups.count(), 'Each category has one native summary');
      assert(await groups.evaluateAll(items => items.every(item => !item.open)), 'Project categories start closed');
      const groupData = await groups.evaluateAll(items => items.map(item => ({
        label: item.querySelector('summary').innerText.replace(/\s+/g, ' ').trim(),
        count: item.querySelectorAll('a[href*="/docs/"]').length,
      })));
      assert(groupData.every(item => item.count > 0), 'No empty categories are rendered');
      for (const item of groupData) assert(new RegExp(`\\b${item.count}\\b`).test(item.label), `${item.label}: visible count matches links`);
      const urls = await groups.locator('a[href*="/docs/"]').evaluateAll(links => links.map(link => link.getAttribute('href')));
      const indexContexts = await groups.locator('a[href*="/docs/"]').evaluateAll(links => links.map(link => ({href:link.getAttribute('href'),context:link.querySelector('.document-context')?.textContent.trim() || ''})).sort((a,b)=>a.href.localeCompare(b.href)));
      if (project.slug === 'cluster-bringup') {
        const labels = await groups.locator('.category-title').allTextContents();
        for (const label of ['Tutorials — learning by doing','How-to guides — getting something done','Reference — the machinery, described','Explanation — why it is like this']) assert(labels.includes(label), `Reference category caption retained: ${label}`);
        assert(indexContexts.some(item=>item.context==='GitLab group credentials'), 'Authored source-topic caption remains visible beside its documents');
      }
      assert.equal(urls.length, project.document_count, `${project.slug}: every published document appears`);
      assert.equal(valueSet(urls).length, urls.length, `${project.slug}: each document appears exactly once`);
      for (const nav of ['.sidebar', '.mobile-menu']) {
        const navUrls = await page.locator(`${nav} details.nav-category a[href*="/docs/"]`).evaluateAll(links => links.map(link => link.getAttribute('href')));
        assert.deepEqual(navUrls.sort(), [...urls].sort(), `${project.slug}: ${nav} preserves every project link exactly once`);
        const navContexts = await page.locator(`${nav} details.nav-category a[href*="/docs/"]`).evaluateAll(links => links.map(link=>({href:link.getAttribute('href'),context:link.querySelector('.tree-context')?.textContent.trim() || ''})).sort((a,b)=>a.href.localeCompare(b.href)));
        assert.deepEqual(navContexts,indexContexts,`${project.slug}: ${nav} retains source-topic context for every document`);
        const navLabels = await page.locator(`${nav} details.nav-category .category-title`).allTextContents();
        assert(navLabels.every(label=>['Tutorials','How-to guides','Reference','Explanation','Other documentation'].includes(label)), 'Navigation uses the short category labels');
        assert.equal(await page.locator(`${nav} details.nav-category[open]`).count(), 0, `${nav} groups start collapsed on project index`);
      }
      for (const url of urls) {
        const response = await context.request.get(base + url);
        assert(response.ok(), `Published URL resolves: ${url}`);
      }
      if (project.slug === 'documentation-pipeline') {
        assert.equal(groupData.length, 1, 'Unclassified pipeline has one honest category');
        assert(groupData[0].label.includes('Other documentation'), 'Unclassified pipeline stays under Other documentation');
      }
      inventories.push({slug: project.slug, expected: project.document_count, groups: groupData, urls});
      record(`source-context-${project.slug}`, {entriesWithContext:indexContexts.filter(item=>item.context).length,desktopAndMobileContextParity:true});
      record(`coverage-${project.slug}`, {publishedPages: project.document_count, uniqueIndexLinks: urls.length, allURLsRespond: true, desktopAndMobileParity: true, categories: groupData});
    }
    record('total-published-coverage', inventories.reduce((sum, item) => sum + item.urls.length, 0));
    await visit(projectRoute('cluster-bringup'));
    const howto = page.locator('details.document-category').filter({has: page.locator('summary').filter({hasText: 'How-to guides — getting something done'})});
    assert.equal(await howto.count(), 1, 'Full reference How-to caption is retained');
    await checkDisclosure(howto, 'mouse', 'desktop-index-mouse');
    await checkDisclosure(howto, 'keyboard', 'desktop-index-keyboard');
    const keyboardFocus = await howto.locator('summary').evaluate(el => ({focused:el===document.activeElement,outlineStyle:getComputedStyle(el).outlineStyle,outlineWidth:getComputedStyle(el).outlineWidth,outlineColor:getComputedStyle(el).outlineColor}));
    assert(keyboardFocus.focused && keyboardFocus.outlineStyle !== 'none' && parseFloat(keyboardFocus.outlineWidth) >= 2, 'Category summary has visible keyboard focus');
    record('keyboard-focus',keyboardFocus);
    await capture('desktop-keyboard-focus');
    const desktopNav = page.locator('.sidebar details.nav-category').filter({has: page.locator('summary').filter({hasText: 'How-to guides'})});
    await checkDisclosure(desktopNav, 'mouse', 'desktop-navigation-mouse');
    await checkDisclosure(desktopNav, 'keyboard', 'desktop-navigation-keyboard');
    const representatives = await page.locator('details.document-category').evaluateAll(groups => groups.map(group => ({
      label: group.querySelector('summary').innerText.replace(/\s+/g, ' ').trim(),
      url: [...group.querySelectorAll('a[href*="/docs/"]')].at(-1).getAttribute('href'),
    })));
    for (const representative of representatives) {
      await visit(representative.url);
      const current = page.locator('.sidebar .tree-link[aria-current="page"]');
      assert.equal(await current.count(), 1, `${representative.label}: one active document`);
      assert.equal(await current.getAttribute('href'), representative.url);
      assert(await current.isVisible(), `${representative.label}: active link visible`);
      assert.equal(await current.locator('xpath=ancestor::details[contains(@class,"nav-category")][@open]').count(), 1, `${representative.label}: active category is server-open`);
      assert.equal(await page.locator('.sidebar details.nav-category[open]').count(), 1, `${representative.label}: only active category opens`);
      const visibility = await current.evaluate(link => {
        const box = link.getBoundingClientRect();
        const rail = link.closest('.sidebar-scroll').getBoundingClientRect();
        return {top: box.top, bottom: box.bottom, railTop: rail.top, railBottom: rail.bottom};
      });
      assert(visibility.top >= visibility.railTop - 1 && visibility.bottom <= visibility.railBottom + 1, `${representative.label}: active link scrolls into desktop rail view`);
      record(`reader-active-${representative.label}`, {url: representative.url, ...visibility});
    }
    for (const viewport of [{name:'desktop',width:1440,height:1000},{name:'tablet',width:768,height:1024},{name:'mobile',width:390,height:844}]) {
      await page.setViewportSize({width:viewport.width,height:viewport.height});
      await visit(projectRoute('cluster-bringup'));
      await capture(`${viewport.name}-index-collapsed`);
      await openAll(page.locator('details.document-category'));
      const metrics = await page.evaluate(() => {
        const main = document.querySelector('main').getBoundingClientRect();
        const groups = [...document.querySelectorAll('details.document-category')].map(group => {
          const summary = group.querySelector('summary');
          const box = summary.getBoundingClientRect();
          return {label:summary.innerText.replace(/\s+/g, ' ').trim(),width:box.width,clientWidth:summary.clientWidth,scrollWidth:summary.scrollWidth,left:box.left,right:box.right,paddingLeft:parseFloat(getComputedStyle(summary).paddingLeft),paddingRight:parseFloat(getComputedStyle(summary).paddingRight)};
        });
        const rows = [...document.querySelectorAll('.document-category .document-row')].map(row => ({title:row.textContent.replace(/\s+/g, ' ').trim(),clientWidth:row.clientWidth,scrollWidth:row.scrollWidth}));
        return {width:innerWidth,scrollWidth:document.documentElement.scrollWidth,mainLeft:main.left,mainRight:main.right,groups,overflowRows:rows.filter(row=>row.scrollWidth>row.clientWidth+1),longestRow:rows.sort((a,b)=>b.title.length-a.title.length)[0]};
      });
      assert(metrics.scrollWidth <= metrics.width + 1, `${viewport.name}: page has no horizontal overflow`);
      assert.equal(metrics.overflowRows.length, 0, `${viewport.name}: long document labels remain contained`);
      assert(metrics.groups.every(group => group.scrollWidth <= group.clientWidth + 1 && group.left >= metrics.mainLeft && group.right <= metrics.mainRight), `${viewport.name}: summary labels and counts remain inside sheet`);
      assert(metrics.groups.every(group => group.paddingLeft >= 12 && group.paddingRight >= 12), `${viewport.name}: category controls retain readable insets`);
      record(`layout-${viewport.name}`, metrics);
      await capture(`${viewport.name}-index-expanded`);
      if (viewport.width <= 1100) {
        const menu = page.locator('.mobile-menu');
        const menuSummary = menu.locator(':scope > summary');
        await menuSummary.click();
        const mobileGroup = menu.locator('details.nav-category').filter({has: page.locator('summary').filter({hasText:'How-to guides'})});
        await checkDisclosure(mobileGroup, 'mouse', `${viewport.name}-menu-category-mouse`);
        await checkDisclosure(mobileGroup, 'keyboard', `${viewport.name}-menu-category-keyboard`);
        await mobileGroup.locator('summary').click();
        const bounds = await menuMetrics(menu);
        assertMenuContained(bounds, viewport.width, `${viewport.name} project menu`);
        await capture(`${viewport.name}-menu-expanded`);
        await page.keyboard.press('Escape');
        assert.equal(await menu.getAttribute('open'), null, `${viewport.name}: Escape closes menu`);
        assert(await menuSummary.evaluate(el=>el===document.activeElement), `${viewport.name}: Escape restores menu focus`);
        record(`${viewport.name}-menu-bounds-and-escape`, bounds);
        await menuSummary.click();
        const destination = mobileGroup.locator('a[href*="/docs/"]').first();
        const href = await destination.getAttribute('href');
        await destination.click();
        await page.waitForURL(base + href);
        await menuSummary.click();
        const current = menu.locator('.tree-link[aria-current="page"]');
        assert(await current.isVisible(), `${viewport.name}: active reader link visible after opening menu`);
        assert.equal(await current.locator('xpath=ancestor::details[contains(@class,"nav-category")][@open]').count(), 1, `${viewport.name}: active reader category is open`);
        const readerBounds = await menuMetrics(menu);
        assertMenuContained(readerBounds, viewport.width, `${viewport.name} reader menu`);
        record(`${viewport.name}-menu-reader-link`, {href, bounds: readerBounds});
        await capture(`${viewport.name}-reader-menu-active`);
      }
    }
    await page.setViewportSize({width:1440,height:1000});
    await visit(projectRoute('cluster-bringup'));
    const search = page.getByRole('combobox', {name:'Search project documentation'});
    await search.fill('slurm');
    const suggestion = page.locator('.search-suggestion').first();
    await suggestion.waitFor({state:'visible'});
    const liveContexts = await page.locator('.search-suggestion-context').allTextContents();
    assert(liveContexts.length > 0 && liveContexts.every(text=>text.includes('Cluster Bringup')), 'Project live search remains scoped');
    const liveHref = await suggestion.getAttribute('href');
    assert(liveHref.includes('#'), 'Live suggestion points to authored section');
    await search.press('ArrowDown');
    await search.press('Enter');
    await page.waitForURL(new URL(liveHref, base).href);
    const anchor = decodeURIComponent(new URL(page.url()).hash.slice(1));
    assert(await page.locator(`[id=${JSON.stringify(anchor)}]`).count(), 'Live search anchor resolves');
    record('live-search-regression', {contexts:liveContexts,url:liveHref,keyboardSelection:true});
    await visit(projectRoute('cluster-bringup'));
    await page.getByRole('combobox', {name:'Search project documentation'}).fill('slurm');
    await page.getByRole('button', {name:'Search',exact:false}).click();
    await page.waitForURL(/\/search\?.*q=slurm/);
    assert(new URL(page.url()).searchParams.get('project') === 'cluster-bringup', 'Normal project search retains scope');
    await page.locator('.search-result').first().waitFor();
    record('normal-search-regression', {url:page.url(),results:await page.locator('.search-result').count()});
    const noJS = await browser.newContext({javaScriptEnabled:false,viewport:{width:1440,height:1000}});
    const noJSPage = await noJS.newPage();
    try {
      await visit(projectRoute('cluster-bringup'), noJSPage);
      const noJSGroup = noJSPage.locator('details.document-category').filter({has:noJSPage.locator('summary').filter({hasText:'How-to guides — getting something done'})});
      await checkDisclosure(noJSGroup,'mouse','no-javascript-index-mouse');
      await checkDisclosure(noJSGroup,'keyboard','no-javascript-index-keyboard');
      const noJSNav = noJSPage.locator('.sidebar details.nav-category').filter({has:noJSPage.locator('summary').filter({hasText:'How-to guides'})});
      await checkDisclosure(noJSNav,'keyboard','no-javascript-navigation-keyboard');
      await noJSGroup.locator('summary').click();
      const link = noJSGroup.locator('a[href*="/docs/"]').first();
      const href = await link.getAttribute('href');
      await link.click();
      await noJSPage.waitForURL(base + href);
      const active = noJSPage.locator('.sidebar .tree-link[aria-current="page"]');
      assert(await active.isVisible(), 'No JavaScript reader current document is visible');
      assert.equal(await active.locator('xpath=ancestor::details[contains(@class,"nav-category")][@open]').count(),1,'No JavaScript reader category is server-open');
      record('no-javascript-reader',href);
      await capture('desktop-no-javascript-reader',noJSPage);
      await visit(projectRoute('documentation-pipeline'),noJSPage);
      const plainInput = noJSPage.getByRole('searchbox',{name:'Search project documentation'});
      await plainInput.fill('configuration');
      await noJSPage.getByRole('button',{name:'Search',exact:false}).click();
      await noJSPage.waitForURL(/\/search\?.*q=configuration/);
      assert(new URL(noJSPage.url()).searchParams.get('project') === 'documentation-pipeline');
      assert(await noJSPage.locator('.search-result').count() > 0,'No JavaScript normal search remains functional');
      record('no-javascript-normal-search',noJSPage.url());
      await noJSPage.setViewportSize({width:390,height:844});
      await visit(projectRoute('cluster-bringup'),noJSPage);
      const nativeMenu = noJSPage.locator('.mobile-menu');
      await nativeMenu.locator(':scope > summary').click();
      const nativeCategory = nativeMenu.locator('details.nav-category').filter({has:noJSPage.locator('summary').filter({hasText:'How-to guides'})});
      await checkDisclosure(nativeCategory,'keyboard','no-javascript-mobile-navigation');
    } finally {await noJS.close();}
    assert.deepEqual(pageErrors,[],'No browser JavaScript errors');
    fs.writeFileSync(evidencePath,JSON.stringify({base,at:new Date().toISOString(),browser:browser.version(),checks,pageErrors},null,2)+'\n');
    console.log(`Category browser verification passed: ${checks.length} checks, ${inventories.reduce((sum,item)=>sum+item.urls.length,0)} published document URLs, 3 viewport widths, Chromium ${browser.version()}`);
  } finally {await browser.close();}
})().catch(error=>{console.error(error);process.exitCode=1;});
