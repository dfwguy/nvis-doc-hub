/* Discovery browser QA. Use an isolated SQLite-backed server: reader GETs record aggregate opens.
 * Run with Playwright in NODE_PATH; NVIS_HUB_URL defaults to the isolated QA port 8001.
 */
const { chromium } = require('playwright');
const { expect } = require('playwright/test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const base = process.env.NVIS_HUB_URL || 'http://127.0.0.1:8001';
const root = path.resolve(__dirname, '..');
const output = path.join(root, '.impeccable/review');
const evidencePath = path.join(root, 'evidence/discovery-browser-review.json');
const previous = fs.existsSync(evidencePath) ? JSON.parse(fs.readFileSync(evidencePath, 'utf8')) : {};
const initialRed = previous.initialRed || (previous.phase === 'initial red' ? previous : null);
const priorEmptyHistory = previous.emptyHistoryVerification || previous.checks?.find(check => check.detail?.before?.heading === 'Explore documentation')?.detail || null;
const record = {phase:'full verification',at:new Date().toISOString(),base,initialRed,emptyHistoryVerification:priorEmptyHistory,checks:[],captures:[],pageErrors:[]};
const absolute = href => new URL(href, base).href;
const documentLinks = locator => locator.locator('a.document-card[href*="/docs/"], .document-card a[href*="/docs/"], a.document-result[href*="/docs/"]');
fs.mkdirSync(output,{recursive:true});
function checkParams(href, expected) {
  const params = new URL(href,base).searchParams;
  for(const [key,value] of Object.entries(expected)) assert.equal(params.get(key)||'',value,`${key} preserved in ${href}`);
}
(async()=>{
  const browser = await chromium.launch({headless:process.env.PW_HEADLESS==='true'});
  record.browser = browser.version();
  const context = await browser.newContext({viewport:{width:1440,height:1000}});
  const page = await context.newPage();
  page.on('pageerror',error=>record.pageErrors.push(error.message));
  const form = () => page.locator('[data-discovery-form]');
  const input = () => form().getByRole('combobox',{name:/Search.*documentation/});
  async function visit(route='/') {
    const response = await page.goto(absolute(route),{waitUntil:'load'});
    assert(response&&response.ok(),`Cannot open ${route}`);
    await page.evaluate(()=>document.fonts.ready);
  }
  async function check(name,fn) {
    try {const detail=await fn();record.checks.push({name,status:'passed',...(detail?{detail}:{})});console.log('PASS '+name);}
    catch(error){record.checks.push({name,status:'failed',error:error.message});console.error('FAIL '+name+': '+error.message);await page.screenshot({path:path.join(output,`discovery-failure-${record.checks.length}.png`)}).catch(()=>{});}
  }
  async function capture(name) {
    const file=`discovery-${name}.png`;
    await page.screenshot({path:path.join(output,file),fullPage:false});
    record.captures.push('.impeccable/review/'+file);
  }
  async function assertAvailableFilters(targetForm) {
    assert(await targetForm.getByLabel('Project',{exact:true}).isVisible(),'Project filter stays visible');
    const visible=[];
    for(const label of ['Project','Topic','Document type']) {
      const control=targetForm.getByLabel(label,{exact:true});
      if(await control.count()) {
        assert(await control.isVisible(),`${label} is visible when available or active`);
        visible.push(label);
      }
    }
    return visible;
  }
  async function cardData(scope=page) {
    return documentLinks(scope).evaluateAll(links=>links.map(link=>({
      href:link.getAttribute('href'),
      title:(link.querySelector('.document-card-title,h3,h2')||link).textContent.trim(),
      text:link.textContent.replace(/\s+/g,' ').trim(),
      kind:link.dataset.kind||link.closest('.document-card')?.dataset.kind||'',
      opens:Number(link.dataset.opens||link.dataset.openCount||link.closest('.document-card')?.dataset.opens||link.textContent.match(/(\d+)\s+(?:opens?|views?)/i)?.[1]||0),
    })));
  }
  async function firstShelfData() {
    const shelf=page.locator('[data-shelf]').first();
    return {heading:await shelf.locator('h2').first().innerText(),cards:await cardData(shelf)};
  }
  async function ensureScrollableShelf() {
    await visit('/');
    const hasOverflow = await page.locator('.document-shelf').first().evaluate(el=>el.scrollWidth>el.clientWidth+1);
    if (!hasOverflow) {
      await visit('/?view=all');
      const destinations=(await cardData(page.locator('#documents'))).slice(0,4).map(card=>card.href);
      for (const destination of destinations) {
        const response=await page.goto(absolute(destination));
        assert(response.ok(),'Real reader opens prepare a scrollable popularity fixture');
      }
      await visit('/');
    }
    return page.locator('[data-shelf]').first();
  }
  async function currentOpenCount(href) {
    await visit('/');
    const data=await firstShelfData();
    const row=data.cards.find(card=>absolute(card.href)===absolute(href));
    assert(row,'Opened document appears on the popularity shelf');
    return row.opens;
  }
  try {
    await check('Root and empty search share one discovery form and one navigation destination',async()=>{
      const states=[];
      for(const route of ['/','/search']) {
        await visit(route);
        assert.equal(await form().count(),1,'One unified discovery form');
        assert.equal(await form().getAttribute('action'),'/search');
        assert.equal(await page.locator('input#query').count(),1,'One query field');
        for(const scope of ['.sidebar .main-navigation','.mobile-menu .main-navigation']) {
          const nav=page.locator(scope);
          const browse=nav.getByRole('link',{name:'Browse documentation',exact:true,includeHidden:true});
          assert.equal(await browse.count(),1);
          assert.equal(await browse.getAttribute('aria-current'),'page');
          assert.equal(await nav.getByRole('link',{name:'Global search',exact:true,includeHidden:true}).count(),0);
        }
        await assertAvailableFilters(form());
        assert(await page.locator('.document-shelf').count()>0,'Discovery home exposes document shelves');
        assert.equal(await page.getByRole('link',{name:'Browse projects',exact:true}).count(),0);
        states.push({route,heading:await page.locator('h1').innerText(),shelves:await page.locator('[data-shelf] h2').allTextContents()});
      }
      assert.equal(states[0].heading,states[1].heading,'Root and search use the same page heading');
      assert.deepEqual(states[0].shelves,states[1].shelves,'Root and search expose the same home shelves');
      checkParams(await page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true}).getAttribute('href'),{view:'all'});
      assert.equal(await page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true}).getAttribute('href'),'/?view=all#documents');
      return states;
    });
    await check('Popularity uses real aggregate reader opens shared across browser contexts',async()=>{
      await visit('/');
      const before=await firstShelfData();
      assert(before.cards.length>0,'First shelf has real document destinations');
      assert(before.cards.every(card=>/\/projects\/[^/]+\/docs\//.test(card.href)),'Shelf cards open hosted documentation');
      assert(['Popular documents','Explore documentation'].includes(before.heading),'Top shelf honestly describes available usage');
      if(before.heading==='Explore documentation') assert(before.cards.every(card=>card.opens===0),'Fallback does not invent popularity');
      else assert(before.cards.some(card=>card.opens>0),'Popular shelf has recorded opens');
      const target=before.cards[0];
      for(let i=0;i<2;i++) {
        const separate=await browser.newContext();
        try {const reader=await separate.newPage();const response=await reader.goto(absolute(target.href));assert(response.ok());await reader.locator('.prose h1').waitFor();}
        finally {await separate.close();}
      }
      await visit('/search');
      const after=await firstShelfData();
      assert.equal(after.heading,'Popular documents');
      assert.equal(absolute(after.cards[0].href),absolute(target.href),'Additional aggregate opens rank the target first');
      assert.equal(after.cards[0].opens,target.opens+2,'Two separate browser contexts each record one open');
      assert(after.cards.every((card,index)=>index===0||after.cards[index-1].opens>=card.opens),'Popularity is sorted by aggregate opens');
      const count=after.cards[0].opens;
      await context.request.get(base+'/api/search?q=configuration');
      await context.request.get(base+'/projects/cluster-bringup/docs/not-published.md');
      await context.request.head(absolute(target.href));
      assert.equal(await currentOpenCount(target.href),count,'Search, missing documents, HEAD, and discovery reads do not record reader opens');
      const detail={before:{heading:before.heading,top:target},after:{heading:after.heading,top:after.cards[0]},browserContexts:2};
      if(before.heading==='Explore documentation')record.emptyHistoryVerification=detail;
      return detail;
    });
    await check('How-to and Reference shelves contain only explicitly classified documents',async()=>{
      await visit('/');
      const typed=[];
      for(const shelf of await page.locator('[data-shelf]').all()) {
        const heading=await shelf.locator('h2').first().innerText();
        const expected=/^How.to/i.test(heading)?'how-to':/^Reference/i.test(heading)?'reference':null;
        if(!expected)continue;
        const cards=await cardData(shelf);
        assert(cards.length>0,'Typed shelves are never empty');
        assert(cards.every(card=>card.kind===expected),`${heading} uses document classification metadata`);
        typed.push({heading,kind:expected,documents:cards.length});
      }
      return {typedShelves:typed,note:typed.length?'Each shelf card exposes its authored classification.':'No typed shelf is fabricated when published classifications are absent.'};
    });
    await check('Browse documents paginates the complete alphabetical document library',async()=>{
      const response=await context.request.get(base+'/api/projects');
      const projects=await response.json();
      const expected=projects.reduce((sum,project)=>sum+project.document_count,0);
      await visit('/');
      await page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true}).click();
      await page.waitForURL(url=>url.searchParams.get('view')==='all'&&url.hash==='#documents');
      const all=[];const pages=[];
      for(let n=0;n<100;n++) {
        const cards=await cardData(page.locator('#documents'));
        assert(cards.length>0,'Library page has published documents');
        all.push(...cards);pages.push({url:page.url(),documents:cards.length});
        const next=page.locator('.pagination').getByRole('link',{name:/next/i});
        if(await next.count()===0)break;
        const href=await next.getAttribute('href');
        assert.equal(new URL(href,base).searchParams.get('view'),'all','Library pagination retains view');
        await next.click();await page.waitForURL(absolute(href));
        assert(n<99,'Pagination terminates');
      }
      assert.equal(all.length,expected,'Every published page is available through the library');
      assert.equal(new Set(all.map(card=>card.href)).size,expected,'Pagination does not duplicate or drop documents');
      const titles=all.map(card=>card.title.toLowerCase());
      assert(titles.every((title,index)=>index===0||titles[index-1]<=title),'Library is alphabetically ordered across page boundaries');
      await capture('desktop-document-library');
      return {expected,documents:all.length,pages};
    });
    await check('Empty-query project filters auto-submit and browse real matching documents',async()=>{
      await visit('/');
      await form().getByLabel('Project',{exact:true}).selectOption('documentation-pipeline');
      await page.waitForURL(url=>url.pathname==='/search'&&url.searchParams.get('project')==='documentation-pipeline');
      assert.equal(new URL(page.url()).searchParams.get('q')||'','');
      const cards=await cardData();
      assert(cards.length>0&&cards.every(card=>card.href.includes('/projects/documentation-pipeline/docs/')),'Project-only browse shows matching documents');
      assert.equal(await page.locator('.search-result').count(),0,'Empty query browses documents rather than section matches');
      assert.equal(await page.locator('.search-start').count(),0,'Filtered browsing has no old search prompt');
      await capture('project-filtered-library');
      return {url:page.url(),documents:cards.length};
    });
    await check('Search and automatic filter navigation retain one query and matching scope',async()=>{
      await input().fill('configuration');
      await form().getByRole('button',{name:'Search',exact:true}).click();
      await page.waitForURL(url=>url.pathname==='/search'&&url.searchParams.get('q')==='configuration');
      checkParams(page.url(),{q:'configuration',project:'documentation-pipeline'});
      assert(await page.locator('.search-result').count()>0);
      assert((await page.locator('.result-context').allTextContents()).every(text=>text.includes('Documentation Pipeline')));
      await form().getByLabel('Project',{exact:true}).selectOption('cluster-bringup');
      await page.waitForURL(url=>url.searchParams.get('project')==='cluster-bringup');
      checkParams(page.url(),{q:'configuration',project:'cluster-bringup'});
      assert.equal(await input().inputValue(),'configuration');
      assert((await page.locator('.result-context').allTextContents()).every(text=>text.includes('Cluster Bringup')));
      await capture('query-and-filter-results');
      return {url:page.url(),results:await page.locator('.search-result').count()};
    });
    await check('Clear search retains filters and Clear filters retains the query',async()=>{
      await visit('/search?q=configuration&project=documentation-pipeline');
      const clearSearch=page.getByRole('link',{name:'Clear search',exact:true});
      checkParams(await clearSearch.getAttribute('href'),{q:'',project:'documentation-pipeline'});
      await clearSearch.click();
      await page.waitForURL(url=>!url.searchParams.get('q')&&url.searchParams.get('project')==='documentation-pipeline');
      assert((await cardData()).every(card=>card.href.includes('/projects/documentation-pipeline/docs/')));
      await visit('/search?q=configuration&project=documentation-pipeline');
      const clearFilters=page.getByRole('link',{name:'Clear filters',exact:true});
      checkParams(await clearFilters.getAttribute('href'),{q:'configuration',project:'',topic:'',kind:''});
      await clearFilters.click();
      await page.waitForURL(url=>url.searchParams.get('q')==='configuration'&&!url.searchParams.get('project'));
      assert.equal(await input().inputValue(),'configuration');
      assert(await page.locator('.search-result').count()>0);
      return {url:page.url()};
    });
    await check('Filter chips remove their own constraint while retaining query and other filters',async()=>{
      await visit('/search');
      const available={};
      for(const [key,label] of [['topic','Topic'],['kind','Document type']]) available[key]=await form().getByLabel(label,{exact:true}).locator('option').evaluateAll(options=>options.find(option=>option.value)?.value||'');
      const scope={q:'configuration',project:'documentation-pipeline',topic:available.topic||'qa-unavailable-topic',kind:available.kind||'qa-unavailable-type'};
      await visit('/search?'+new URLSearchParams(scope));
      const tested=[];
      for(const [key,label] of [['project','project'],['topic','topic'],['kind','document type']]) {
        if(!scope[key])continue;
        const remove=page.getByRole('link',{name:new RegExp(`remove ${label} filter`,'i')});
        assert.equal(await remove.count(),1,`${key} has an accessible removal link`);
        if(key!=='project')assert(await form().getByLabel(key==='topic'?'Topic':'Document type',{exact:true}).isVisible(),'An explicitly selected unavailable filter remains visible and removable');
        const href=await remove.getAttribute('href');
        checkParams(href,{...scope,[key]:''});
        tested.push({key,href});
      }
      const removeProject=page.getByRole('link',{name:/remove project filter/i});
      const href=await removeProject.getAttribute('href');
      await removeProject.focus();await removeProject.press('Enter');await page.waitForURL(absolute(href));
      checkParams(page.url(),{...scope,project:''});
      return {availableFacets:available,tested,note:(!available.topic&&!available.kind)?'Published sources have no topic/type facets; explicit unavailable URL values verify visible removable controls without fabricating content classifications.':undefined};
    });
    for(const viewport of [{name:'desktop',width:1440,height:1000},{name:'tablet',width:768,height:1024},{name:'phone',width:390,height:844},{name:'narrow-phone',width:320,height:844}]) {
      await check(`${viewport.name} discovery shelves, filters, cards, and navigation fit`,async()=>{
        await page.setViewportSize({width:viewport.width,height:viewport.height});await visit('/');
        await assertAvailableFilters(form());
        const browseDocuments=page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true});
        assert(await browseDocuments.isVisible(),'Browse documents remains visible at every width');
        const browseBox=await browseDocuments.boundingBox();
        assert(browseBox.x>=0&&browseBox.x+browseBox.width<=viewport.width+1,'Browse documents remains reachable inside the viewport');
        const metrics=await page.evaluate(()=>({
          width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
          cards:[...document.querySelectorAll('.document-card')].map(card=>{const box=card.getBoundingClientRect();return {height:box.height,width:box.width,clientWidth:card.clientWidth,scrollWidth:card.scrollWidth};}),
          shelves:[...document.querySelectorAll('.document-shelf')].map(rail=>({clientWidth:rail.clientWidth,scrollWidth:rail.scrollWidth,firstCardWidth:rail.querySelector('.document-card').getBoundingClientRect().width})),
          filters:[...document.querySelectorAll('[data-discovery-form] select')].map(select=>{const box=select.getBoundingClientRect();return {label:select.name,height:box.height,left:box.left,right:box.right};}),
        }));
        assert(metrics.scrollWidth<=metrics.width+1,'Document shelves do not overflow the page');
        assert(metrics.cards.length>0&&metrics.cards.every(card=>card.height>=44&&card.scrollWidth<=card.clientWidth+1),'Document cards have accessible targets and contained titles');
        assert(metrics.filters.every(filter=>filter.left>=0&&filter.right<=metrics.width+1),'All filter controls remain inside the viewport');
        if(viewport.width<=700) {
          assert(metrics.filters.every(filter=>filter.height>=44),'Phone filter targets are at least 44px');
          assert(metrics.shelves.every(shelf=>shelf.firstCardWidth>=shelf.clientWidth*.8),'Phone shelf cards retain at least 80% of the rail width instead of shrinking to fit every document');
        }
        const last=documentLinks(page.locator('.document-shelf').first()).last();
        await last.focus();await last.scrollIntoViewIfNeeded();
        const box=await last.boundingBox();assert(box.x>=0&&box.x+box.width<=viewport.width+1,'Keyboard can reach the end of a shelf');
        await page.goto('about:blank');
        await visit('/');
        assert(await page.locator('.document-shelf').evaluateAll(rails=>rails.every(rail=>rail.scrollLeft===0)),'Fresh homepage shelves start at their first document');
        assert(await page.locator('.shelf-previous').evaluateAll(buttons=>buttons.every(button=>button.disabled)),'Previous controls are disabled at the initial shelf position');
        await capture(`${viewport.name}-home`);
        if(viewport.width<=1100) {
          const menu=page.locator('.mobile-menu');await menu.locator(':scope > summary').click();
          assert(await menu.getByRole('link',{name:'Browse documentation',exact:true}).isVisible());
          assert.equal(await menu.getByRole('link',{name:'Global search',exact:true}).count(),0);
          await capture(`${viewport.name}-menu`);await page.keyboard.press('Escape');
          assert.equal(await menu.getAttribute('open'),null);
        }
        return metrics;
      });
    }
    await check('Shelf controls work with visible keyboard focus, contrast, and reduced motion',async()=>{
      await page.setViewportSize({width:390,height:844});
      await page.emulateMedia({reducedMotion:'reduce'});await visit('/');
      const section=await ensureScrollableShelf(),rail=section.locator('.document-shelf');
      const overflow=await rail.evaluate(el=>el.scrollWidth>el.clientWidth+1);
      assert(overflow,'Published shelf exercises horizontal scrolling');
      await expect(section.locator('.shelf-controls')).toBeVisible();
      const next=section.getByRole('button',{name:/^Next /});
      await page.keyboard.press('Tab');await next.focus();
      const focus=await next.evaluate(el=>({focused:el===document.activeElement,width:parseFloat(getComputedStyle(el).outlineWidth),style:getComputedStyle(el).outlineStyle}));
      assert(focus.focused&&focus.width>=2&&focus.style!=='none','Shelf controls show keyboard focus');
      await rail.evaluate(el=>{const original=el.scrollBy.bind(el);el.scrollBy=options=>{el.dataset.lastScrollBehavior=options.behavior;original(options);};});
      await next.press('Enter');
      await expect.poll(()=>rail.evaluate(el=>el.scrollLeft)).toBeGreaterThan(0);
      assert.equal(await rail.getAttribute('data-last-scroll-behavior'),'auto','Reduced motion disables smooth shelf scrolling');
      await expect(section.getByRole('button',{name:/^Previous /})).toBeEnabled();
      const contrast=await section.locator('.document-card').first().evaluate(card=>{
        function luminance(color){const channels=color.match(/\d+(?:\.\d+)?/g).slice(0,3).map(Number).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return channels[0]*.2126+channels[1]*.7152+channels[2]*.0722;}
        const background=luminance(getComputedStyle(card).backgroundColor);
        return [...card.querySelectorAll('h3,.document-card-project,.document-card-path,.document-card-opens')].map(el=>{const foreground=luminance(getComputedStyle(el).color);return {className:el.className||el.tagName,ratio:(Math.max(foreground,background)+.05)/(Math.min(foreground,background)+.05)};});
      });
      assert(contrast.every(item=>item.ratio>=4.5),'Card text and metadata meet normal-text contrast');
      await capture('phone-shelf-keyboard-reduced-motion');
      await page.emulateMedia({reducedMotion:'no-preference'});
      return {focus,contrast,scrollBehavior:'auto'};
    });
    await check('Touch swipe scrolls the shelf and a native card tap opens its document',async()=>{
      const phone=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
      try {
        const touch=await phone.newPage();await touch.goto(base);
        const rail=touch.locator('.document-shelf').first();await rail.scrollIntoViewIfNeeded();
        const box=await rail.boundingBox(),y=Math.min(800,box.y+box.height/2);
        const cdp=await phone.newCDPSession(touch);
        await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:Math.min(350,box.x+box.width-20),y}]});
        for(const x of [300,250,200,150,100,60])await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y}]});
        await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
        await expect.poll(()=>rail.evaluate(el=>el.scrollLeft)).toBeGreaterThan(0);
        const card=documentLinks(touch.locator('[data-shelf]').first()).nth(1);await card.scrollIntoViewIfNeeded();
        const href=await card.getAttribute('href');await card.tap();await touch.waitForURL(absolute(href));await touch.locator('.prose h1').waitFor();
        return {href};
      }finally{await phone.close();}
    });
    await check('JavaScript-free discovery search and visible filters submit natively',async()=>{
      const plain=await browser.newContext({javaScriptEnabled:false,viewport:{width:390,height:844}});
      try {
        const noJS=await plain.newPage();await noJS.goto(base+'/search');
        const nativeForm=noJS.locator('[data-discovery-form]');
        await assertAvailableFilters(nativeForm);
        await nativeForm.getByRole('searchbox',{name:/Search.*documentation/}).fill('configuration');
        await nativeForm.getByLabel('Project',{exact:true}).selectOption('documentation-pipeline');
        await nativeForm.getByRole('button',{name:'Apply filters',exact:true}).click();
        await noJS.waitForURL(url=>url.searchParams.get('q')==='configuration'&&url.searchParams.get('project')==='documentation-pipeline');
        assert(await noJS.locator('.search-result').count()>0);
        assert((await noJS.locator('.result-context').allTextContents()).every(text=>text.includes('Documentation Pipeline')));
        const clear=noJS.getByRole('link',{name:'Clear search',exact:true});await clear.click();
        await noJS.waitForURL(url=>!url.searchParams.get('q')&&url.searchParams.get('project')==='documentation-pipeline');
        assert((await documentLinks(noJS).count())>0,'Native filtered browsing remains available');
        return {url:noJS.url()};
      } finally {await plain.close();}
    });
    await check('Discovery interactions produce no browser JavaScript errors',async()=>assert.deepEqual(record.pageErrors,[]));
  } finally {
    record.passed=record.checks.filter(check=>check.status==='passed').length;
    record.failed=record.checks.filter(check=>check.status==='failed').length;
    fs.writeFileSync(evidencePath,JSON.stringify(record,null,2)+'\n');
    console.log(`Discovery verification: ${record.passed} passed, ${record.failed} failed.`);
    await browser.close();if(record.failed)process.exitCode=1;
  }
})().catch(error=>{console.error(error);process.exitCode=1;});
