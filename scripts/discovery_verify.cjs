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
const evidencePath = path.join(root, 'evidence/discovery-simplification-browser.json');
const previous = fs.existsSync(evidencePath) ? JSON.parse(fs.readFileSync(evidencePath, 'utf8')) : {};
const initialRed = previous.initialRed || (previous.phase === 'initial red' ? previous : null);
const priorEmptyHistory = previous.emptyHistoryVerification || null;
const record = {phase:'full verification',at:new Date().toISOString(),base,initialRed,correctionRed:previous.correctionRed||null,preCorrectionVerification:previous.preCorrectionVerification||null,emptyHistoryVerification:priorEmptyHistory,checks:[],captures:[],pageErrors:[]};
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
    catch(error){record.checks.push({name,status:'failed',error:error.message});console.error('FAIL '+name+': '+error.message);await page.screenshot({path:path.join(output,`simplification-failure-${record.checks.length}.png`)}).catch(()=>{});}
  }
  async function capture(name) {
    const file=`simplification-${name}.png`;
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
        assert.equal(await page.locator('.sidebar .project-nav-link,.mobile-menu .project-nav-link').count(),0,'Discovery navigation has no global project list');
        assert.equal(await page.locator('.nav-heading').filter({hasText:'Projects'}).count(),0,'Global Projects headings are removed');
        assert.equal(await page.locator('[data-shelf]').count(),1,'Default discovery has one popular section');
        assert.equal(await page.getByRole('link',{name:'Browse projects',exact:true}).count(),0);
        states.push({route,heading:await page.locator('h1').innerText(),shelves:await page.locator('[data-shelf] h2').allTextContents()});
      }
      assert.equal(states[0].heading,states[1].heading,'Root and search use the same page heading');
      assert.deepEqual(states[0].shelves,states[1].shelves,'Root and search expose the same home shelves');
      checkParams(await page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true}).getAttribute('href'),{view:'all'});
      assert.equal(await page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true}).getAttribute('href'),'/?view=all#documents');
      return states;
    });
    await check('Default discovery is one honest popular carousel without extra project shelves',async()=>{
      await visit('/');
      assert.equal(await page.locator('[data-shelf]').count(),1);
      const state=await firstShelfData();
      assert.equal(state.heading,'Explore popular documentation');
      assert(await page.locator('.shelf-controls').count()<=1,'Only one carousel control group exists');
      assert.equal(await page.getByRole('heading',{name:/^From /}).count(),0,'Project shelves are removed');
      assert(state.cards.length<=6&&state.cards.every(card=>card.opens>0),'Only actually opened documents appear');
      if(state.cards.length===0){
        assert.equal(await page.locator('.shelf-controls:visible').count(),0,'An empty popular section has no active carousel controls');
        const text=await page.locator('[data-shelf]').innerText();
        assert(/No popular documentation yet|appear as people open/i.test(text),'Empty history is explained honestly');
        record.emptyHistoryVerification={at:new Date().toISOString(),heading:state.heading,cards:0,text};
        await capture('empty-history');
      }
      return state;
    });
    await check('Popularity uses real aggregate reader opens shared across browser contexts',async()=>{
      await visit('/');
      const before=await firstShelfData();
      let target=before.cards[0];
      if(!target){await visit('/?view=all');target={...(await cardData(page.locator('#documents')))[0],opens:0};}
      assert(target&&/\/projects\/[^/]+\/docs\//.test(target.href),'A genuine published document supplies the usage probe');
      for(let i=0;i<2;i++){
        const separate=await browser.newContext();
        try{const reader=await separate.newPage();const response=await reader.goto(absolute(target.href));assert(response.ok());await reader.locator('.prose h1').waitFor();}
        finally{await separate.close();}
      }
      await visit('/search');
      const after=await firstShelfData();
      assert.equal(after.heading,'Explore popular documentation');
      assert.equal(absolute(after.cards[0].href),absolute(target.href),'Additional opens rank the target first');
      assert.equal(after.cards[0].opens,target.opens+2,'Two separate browser contexts each record one open');
      assert(after.cards.every((card,index)=>card.opens>0&&(index===0||after.cards[index-1].opens>=card.opens)),'Actual popularity remains ordered');
      const count=after.cards[0].opens;
      await context.request.get(base+'/api/search?q=configuration');
      await context.request.get(base+'/projects/cluster-bringup/docs/not-published.md');
      await context.request.head(absolute(target.href));
      assert.equal(await currentOpenCount(target.href),count,'Search, missing documents, HEAD and discovery reads do not count');
      return {before:{heading:before.heading,cards:before.cards.length,target},after:{heading:after.heading,top:after.cards[0]},browserContexts:2};
    });
    await check('The popular carousel contains at most six genuinely opened documents',async()=>{
      await visit('/?view=all');
      const destinations=(await cardData(page.locator('#documents'))).slice(0,8).map(card=>card.href);
      assert.equal(destinations.length,8,'Eight different published documents exercise the six-card limit');
      for(const href of destinations){const response=await page.goto(absolute(href));assert(response.ok());await page.locator('.prose h1').waitFor();}
      await visit('/');
      const grid=await firstShelfData();
      assert.equal(grid.cards.length,6,'The default carousel is bounded to six popular documents');
      assert.equal(new Set(grid.cards.map(card=>card.href)).size,6);
      assert(grid.cards.every(card=>card.opens>0),'No unopened recommendations are fabricated');
      return {actualReaderOpens:destinations.length,popularCards:grid.cards};
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
      assert.equal(await page.locator('[data-shelf],.document-card').count(),0,'A selected project uses the vertical library without a carousel');
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
    await check('Active-project-only navigation retains sentence-style names and command spelling',async()=>{
      await visit('/projects/cluster-bringup');
      const examples=[
        {href:'/projects/cluster-bringup/docs/docs/omnistation_gitlab_credentials/how-to/launch-codex-for-existing-repository.md',title:'Launch Codex for an existing group repository'},
        {href:'/projects/cluster-bringup/docs/docs/cmsh_setup/tutorial.md',title:'Connect cmsh from a non-BCM host'},
      ];
      for(const example of examples){
        assert.equal(await page.locator(`.document-row[href="${example.href}"] .category-entry-title`).textContent(),example.title);
        assert.equal(await page.locator(`.sidebar .tree-link[href="${example.href}"] > span`).first().textContent(),example.title);
      }
      async function assertActiveProjectContext(){
        for(const scope of ['.sidebar','.mobile-menu']){
          const context=page.locator(scope);
          assert.equal(await context.locator('.nav-heading').innerText(),'Document sections');
          const links=await context.locator('.project-nav-link').evaluateAll(nodes=>nodes.map(node=>node.getAttribute('href')));
          assert.equal(links.length,0,'Document-section navigation contains no project-name list');
        }
      }
      await assertActiveProjectContext();
      await visit(examples[0].href);await assertActiveProjectContext();
      const current=page.locator('.sidebar .tree-link[aria-current="page"]');
      assert(await current.isVisible());
      assert.equal(await current.locator('xpath=ancestor::details[contains(@class,"nav-category")][@open]').count(),1);
      return examples;
    });
    for(const viewport of [{name:'desktop',width:1440,height:1000},{name:'compact-desktop',width:1280,height:900},{name:'tablet',width:768,height:1024},{name:'phone',width:390,height:844},{name:'narrow-phone',width:320,height:844}]){
      await check(`${viewport.name} single popular carousel remains readable and contained`,async()=>{
        await page.setViewportSize({width:viewport.width,height:viewport.height});await visit('/');
        await assertAvailableFilters(form());
        const browse=page.locator('.page-heading').getByRole('link',{name:'Browse documents',exact:true});
        assert(await browse.isVisible());const browseBox=await browse.boundingBox();
        assert(browseBox.x>=0&&browseBox.x+browseBox.width<=viewport.width+1,'Browse documents is reachable');
        const metrics=await page.evaluate(()=>({
          width:innerWidth,scrollWidth:document.documentElement.scrollWidth,
          cards:[...document.querySelectorAll('.document-card')].map(card=>{const box=card.getBoundingClientRect();return {height:box.height,width:box.width,left:box.left,right:box.right,clientWidth:card.clientWidth,scrollWidth:card.scrollWidth};}),
          grids:[...document.querySelectorAll('.document-shelf')].map(grid=>({clientWidth:grid.clientWidth,scrollWidth:grid.scrollWidth,overflowX:getComputedStyle(grid).overflowX})),
          filters:[...document.querySelectorAll('[data-discovery-form] select')].map(select=>{const box=select.getBoundingClientRect();return {label:select.name,height:box.height,left:box.left,right:box.right};}),
        }));
        assert(metrics.scrollWidth<=metrics.width+1,'The page has no horizontal overflow');
        assert(metrics.cards.length===6&&metrics.cards.every(card=>card.height>=44&&card.width>=Math.min(200,metrics.width-40)&&card.scrollWidth<=card.clientWidth+1),'All six popular cards remain readable in the contained carousel');
        assert.equal(metrics.grids.length,1);
        assert(metrics.grids[0].scrollWidth>metrics.grids[0].clientWidth,'The popular list scrolls horizontally inside its own region');
        const section=page.locator('[data-shelf]'),rail=section.locator('.document-shelf');
        assert.equal(await section.locator('.shelf-controls').count(),1);
        await expect(section.locator('.shelf-controls')).toBeVisible();
        await expect(section.locator('.shelf-previous')).toBeDisabled();
        const controls=await section.locator('.shelf-controls button').evaluateAll(buttons=>buttons.map(button=>{const box=button.getBoundingClientRect();return {width:box.width,height:box.height};}));
        assert(controls.length===2&&controls.every(control=>control.width>=44&&control.height>=44),'Carousel controls provide44px targets');
        const next=section.getByRole('button',{name:'Next popular documents',exact:true});
        assert.equal(await next.getAttribute('aria-controls'),await rail.getAttribute('id'));
        await next.click();
        await expect.poll(()=>rail.evaluate(el=>el.scrollLeft)).toBeGreaterThan(0);
        await expect(section.locator('.shelf-previous')).toBeEnabled();
        assert(metrics.filters.every(filter=>filter.left>=0&&filter.right<=metrics.width+1));
        if(viewport.width<=700)assert(metrics.filters.every(filter=>filter.height>=44));
        const last=documentLinks(page.locator('[data-shelf]')).last();await last.focus();await last.scrollIntoViewIfNeeded();
        const box=await last.boundingBox();assert(box.x>=0&&box.x+box.width<=viewport.width+1,'Keyboard reaches the last card through contained carousel scrolling');
        await page.goto('about:blank');await visit('/');
        assert.equal(await page.locator('.document-shelf').evaluate(el=>el.scrollLeft),0,'Carousel starts at its first document');
        await expect(page.locator('.shelf-previous')).toBeDisabled();
        await capture(`${viewport.name}-home`);
        if(viewport.width<=1100){const menu=page.locator('.mobile-menu');await menu.locator(':scope > summary').click();assert(await menu.getByRole('link',{name:'Browse documentation',exact:true}).isVisible());await page.keyboard.press('Escape');assert.equal(await menu.getAttribute('open'),null);}
        return metrics;
      });
    }
    await check('Native carousel controls and cards retain keyboard focus, contrast and reduced-motion support',async()=>{
      await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'reduce'});await visit('/');
      const rail=page.locator('.document-shelf');
      await rail.evaluate(el=>{const original=el.scrollBy.bind(el);el.scrollBy=options=>{el.dataset.lastScrollBehavior=options.behavior;original(options);};});
      const next=page.locator('.shelf-next');await next.focus();await next.press('Enter');
      await expect.poll(()=>rail.evaluate(el=>el.scrollLeft)).toBeGreaterThan(0);
      assert.equal(await rail.getAttribute('data-last-scroll-behavior'),'auto','Reduced motion uses instant carousel scrolling');
      const card=page.locator('.document-card').first();await page.keyboard.press('Tab');await card.focus();
      const focus=await card.evaluate(el=>({focused:el===document.activeElement,width:parseFloat(getComputedStyle(el).outlineWidth),style:getComputedStyle(el).outlineStyle,animation:getComputedStyle(el).animationName}));
      assert(focus.focused&&focus.width>=2&&focus.style!=='none');assert.equal(focus.animation,'none');
      const contrast=await card.evaluate(card=>{
        function luminance(color){const channels=color.match(/\d+(?:\.\d+)?/g).slice(0,3).map(Number).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return channels[0]*.2126+channels[1]*.7152+channels[2]*.0722;}
        const background=luminance(getComputedStyle(card).backgroundColor);
        return [...card.querySelectorAll('h3,.document-card-project,.document-card-path,.document-card-opens')].map(el=>{const foreground=luminance(getComputedStyle(el).color);return {className:el.className||el.tagName,ratio:(Math.max(foreground,background)+.05)/(Math.min(foreground,background)+.05)};});
      });
      assert(contrast.every(item=>item.ratio>=4.5));await capture('phone-carousel-keyboard-reduced-motion');
      const href=await card.getAttribute('href');await card.press('Enter');await page.waitForURL(absolute(href));await page.locator('.prose h1').waitFor();await page.emulateMedia({reducedMotion:'no-preference'});
      return {focus,contrast,href};
    });
    await check('Native touch swiping moves the carousel and a card tap opens its document',async()=>{
      const phone=await browser.newContext({viewport:{width:390,height:844},isMobile:true,hasTouch:true});
      try{
        const touch=await phone.newPage();await touch.goto(base);
        const rail=touch.locator('.document-shelf');await rail.scrollIntoViewIfNeeded();
        const box=await rail.boundingBox(),y=Math.min(800,box.y+box.height/2);
        const cdp=await phone.newCDPSession(touch);
        await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:Math.min(350,box.x+box.width-20),y}]});
        for(const x of [300,250,200,150,100,60])await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y}]});
        await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});
        await expect.poll(()=>rail.evaluate(el=>el.scrollLeft)).toBeGreaterThan(0);
        const card=touch.locator('.document-card').nth(1);await card.scrollIntoViewIfNeeded();const href=await card.getAttribute('href');await card.tap();await touch.waitForURL(absolute(href));await touch.locator('.prose h1').waitFor();return {href};
      }finally{await phone.close();}
    });
    await check('Theme switch supports keyboard selection and persists across reloads and routes',async()=>{
      const isolated=await browser.newContext({viewport:{width:320,height:844},colorScheme:'light'});
      try{
        const themed=await isolated.newPage();await themed.goto(base);
        const toggle=themed.locator('[data-theme-toggle]');
        assert.equal(await themed.locator('html').getAttribute('data-theme'),'dark','Dark is the default without a saved preference');
        assert.equal(await toggle.getAttribute('role'),'switch');
        assert.equal(await toggle.getAttribute('aria-checked'),'true');
        assert(await toggle.getAttribute('aria-label'),'The switch has an accessible label');
        await themed.keyboard.press('Tab');await toggle.focus();await toggle.press('Enter');
        assert.equal(await themed.locator('html').getAttribute('data-theme'),'light');
        assert.equal(await toggle.getAttribute('aria-checked'),'false');
        await themed.reload();assert.equal(await themed.locator('html').getAttribute('data-theme'),'light','Light preference survives reload');
        await themed.goto(base+'/search?q=configuration');assert.equal(await themed.locator('html').getAttribute('data-theme'),'light','Light preference survives route changes');
        await themed.locator('[data-theme-toggle]').focus();await themed.locator('[data-theme-toggle]').press('Space');
        assert.equal(await themed.locator('html').getAttribute('data-theme'),'dark');
        await themed.reload();assert.equal(await themed.locator('html').getAttribute('data-theme'),'dark','Dark preference also persists');
        return {default:'dark',keyboard:['Enter','Space'],reloads:['light','dark'],routePersistence:true};
      }finally{await isolated.close();}
    });
    for(const theme of ['dark','light']){
      await check(`${theme} theme keeps discovery, search and reader contrast and responsive header containment`,async()=>{
        const isolated=await browser.newContext({viewport:{width:320,height:844}});
        const states=[];
        try{
          const themed=await isolated.newPage();await themed.goto(base);
          if(await themed.locator('html').getAttribute('data-theme')!==theme)await themed.locator('[data-theme-toggle]').click();
          for(const viewport of [{width:1440,height:1000},{width:1280,height:900},{width:768,height:1024},{width:390,height:844},{width:320,height:844}]){
            await themed.setViewportSize(viewport);
          for(const route of ['/','/search?q=configuration','/projects/cluster-bringup/docs/docs/cmsh_setup/how-to/troubleshoot-connection.md']){
            await themed.goto(absolute(route));await themed.evaluate(()=>document.fonts.ready);
            assert.equal(await themed.locator('html').getAttribute('data-theme'),theme);
            const metrics=await themed.evaluate(()=>{
              function rgb(color){return color.match(/\d+(?:\.\d+)?/g).map(Number);}
              function luminance(color){const channels=rgb(color).slice(0,3).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return channels[0]*.2126+channels[1]*.7152+channels[2]*.0722;}
              function background(el){for(let node=el;node;node=node.parentElement){const color=getComputedStyle(node).backgroundColor,parts=rgb(color);if(parts.length<4||parts[3]>0)return color;}return 'rgb(255,255,255)';}
              const selectors=['h1','.document-card h3','.document-card-project','.document-card-opens','.document-card-path','.search-result h3 a','.prose p','.prose a','.prose code','[data-theme-toggle]'];
              const contrast=selectors.map(selector=>{const el=document.querySelector(selector);if(!el)return null;const foreground=luminance(getComputedStyle(el).color),back=luminance(background(el));return {selector,ratio:(Math.max(foreground,back)+.05)/(Math.min(foreground,back)+.05)};}).filter(Boolean);
              const header=[...document.querySelectorAll('.topbar .desktop-context > a,.topbar .mobile-brand .brand,.topbar .mobile-menu > summary,.topbar [data-theme-toggle],.topbar .topbar-help')].map(el=>{const box=el.getBoundingClientRect();return {tag:el.tagName,className:el.className,left:box.left,right:box.right,top:box.top,bottom:box.bottom,width:box.width,height:box.height};}).filter(box=>box.width&&box.height);
              const headerBox=document.querySelector('.topbar').getBoundingClientRect();
              return {width:innerWidth,clientWidth:document.documentElement.clientWidth,scrollWidth:document.documentElement.scrollWidth,headerTop:headerBox.top,headerBottom:headerBox.bottom,contrast,header};
            });
            assert(metrics.scrollWidth<=metrics.width+1,'Theme changes never add page-wide horizontal overflow');
            assert(metrics.header.every(item=>item.left>=0&&item.right<=metrics.clientWidth+1&&item.top>=metrics.headerTop-1&&item.bottom<=metrics.headerBottom+1),'Logo, menu and theme switch fit the header');
            assert(metrics.contrast.every(item=>item.ratio>=4.5),`${theme} text contrast stays readable: ${JSON.stringify(metrics.contrast)}`);
            if(viewport.width<=1100){
              const menu=themed.locator('.mobile-menu');await menu.locator(':scope > summary').click();
              const bounds=await menu.locator('.mobile-menu-body').evaluate(el=>{const box=el.getBoundingClientRect();return {left:box.left,right:box.right,top:box.top,bottom:box.bottom,scrollWidth:el.scrollWidth,clientWidth:el.clientWidth};});
              assert(bounds.left>=0&&bounds.right<=metrics.clientWidth+1&&bounds.top>=0&&bounds.bottom<=viewport.height+1,'Open navigation remains inside the visible viewport after adding the theme switch');
              assert(bounds.scrollWidth<=bounds.clientWidth+1,'Open navigation has no horizontal overflow');
              metrics.menu=bounds;await themed.keyboard.press('Escape');assert.equal(await menu.getAttribute('open'),null);
            }
            const headerTarget=viewport.width<=1100?themed.locator('.mobile-menu > summary'):themed.locator('.desktop-context > a');
            await themed.keyboard.press('Tab');await headerTarget.focus();
            const headerFocus=await headerTarget.evaluate(el=>{
              function lum(color){const c=color.match(/\d+(?:\.\d+)?/g).slice(0,3).map(Number).map(v=>v/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722;}
              const style=getComputedStyle(el),a=lum(style.outlineColor),b=lum(getComputedStyle(el.closest('.topbar')).backgroundColor);
              return {width:parseFloat(style.outlineWidth),style:style.outlineStyle,ratio:(Math.max(a,b)+.05)/(Math.min(a,b)+.05)};
            });
            assert(headerFocus.width>=2&&headerFocus.style!=='none'&&headerFocus.ratio>=3,'Header keyboard focus remains visible with sufficient contrast in both themes');
            metrics.headerFocus=headerFocus;
            const toggle=themed.locator('[data-theme-toggle]');await themed.keyboard.press('Tab');await toggle.focus();
            const focus=await toggle.evaluate(el=>({focused:el===document.activeElement,width:parseFloat(getComputedStyle(el).outlineWidth),style:getComputedStyle(el).outlineStyle}));
            assert(focus.focused&&focus.width>=2&&focus.style!=='none','The theme switch has visible keyboard focus');
            const label=route==='/'?'home':route.startsWith('/search')?'search':'reader';
            const file=`simplification-${theme}-${label}-${viewport.width}.png`;await themed.screenshot({path:path.join(output,file),fullPage:false});record.captures.push('.impeccable/review/'+file);
            states.push({viewport,route,metrics,focus});
          }
          }
          return states;
        }finally{await isolated.close();}
      });
    }
    await check('Blocked browser storage falls back to dark and leaves the theme switch usable',async()=>{
      const isolated=await browser.newContext({viewport:{width:320,height:844}});
      try{
        await isolated.addInitScript(()=>{for(const name of ['getItem','setItem'])Object.defineProperty(Storage.prototype,name,{value(){throw new Error('QA storage unavailable');},configurable:true});});
        const themed=await isolated.newPage(),errors=[];themed.on('pageerror',error=>errors.push(error.message));await themed.goto(base);
        assert.equal(await themed.locator('html').getAttribute('data-theme'),'dark');
        await themed.locator('[data-theme-toggle]').click();assert.equal(await themed.locator('html').getAttribute('data-theme'),'light','The current page can switch without storage');
        await themed.reload();assert.equal(await themed.locator('html').getAttribute('data-theme'),'dark','Unavailable persistence safely returns to dark');
        assert.deepEqual(errors,[]);return {fallback:'dark',inPageToggle:'light',errors};
      }finally{await isolated.close();}
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
