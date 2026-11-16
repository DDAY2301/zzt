#!/usr/bin/env python3
"""Browser QA of the generated ZZT website; also probes the real custom domain."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import subprocess,time,json,sys

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'qa_artifacts';OUT.mkdir(exist_ok=True)
server=subprocess.Popen([sys.executable,'-m','http.server','8765','--directory',str(BASE/'site')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
report={'local':{},'live':{},'errors':[]}
try:
    time.sleep(1.2)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for label,width,height in [('desktop',1440,900),('tablet',820,1000),('mobile',390,844)]:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
            page=context.new_page()
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            response=page.goto('http://127.0.0.1:8765/',wait_until='networkidle',timeout=30000)
            assert response.status==200,(label,response.status)
            assert page.locator('h1').count()==1,label
            assert page.locator('a[href="/projekti/"]').count()>=1,label
            measured=page.evaluate('({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
            assert measured['scroll']<=width+1,(label,'horizontal overflow',measured)
            imgs=page.locator('.front-hero-photo img, .front-intro-photo img, .front-kolpa-photo img')
            assert imgs.count()==3,(label,'missing Kolpa photography',imgs.count())
            # Lazy-loaded pictures below the fold must be scrolled into view first.
            for i in range(imgs.count()):
                image=imgs.nth(i)
                image.scroll_into_view_if_needed()
                page.wait_for_function('(el) => el.complete && el.naturalWidth > 0',arg=image.element_handle(),timeout=15000)
            sizes=imgs.evaluate_all('es => es.map(e => ({loaded:e.complete && e.naturalWidth>0,width:e.naturalWidth,src:e.currentSrc}))')
            assert all(v['loaded'] for v in sizes),(label,'Kolpa image failed to render',sizes)
            if label in ('tablet','mobile'):
                toggle=page.locator('.menu-toggle')
                toggle.click()
                assert toggle.get_attribute('aria-expanded')=='true','menu did not open'
                assert page.locator('nav.main-nav a[href="/projekti/"]').is_visible(),'projects link hidden'
                toggle.press('Escape')
                assert toggle.get_attribute('aria-expanded')=='false','escape did not close menu'
            else:
                assert page.locator('.main-nav').is_visible(),label
            page.screenshot(path=str(OUT/f'ZZT {label}.png'),full_page=True,animations='disabled')
            assert not errors,(label,errors)
            report['local'][label]={'width':width,'scrollWidth':measured['scroll'],'kolpaPhotosLoaded':len(sizes),'jsErrors':len(errors),'pass':True}
            if label=='desktop':
                page.locator('nav.main-nav a[href="/projekti/"]').click()
                assert page.url.endswith('/projekti/'),'Project navigation failed'
                assert page.locator('h1').count()==1,'Projects h1'
                page.goto('http://127.0.0.1:8765/kontakt/',wait_until='domcontentloaded')
                assert page.locator('a.contact-mail').get_attribute('href')=='mailto:dan.grmusa@gmail.com','Contact email'
            context.close()
        context=browser.new_context(viewport={'width':1280,'height':800})
        page=context.new_page()
        for slug in ['','o-zavodu','raziskave-in-razvoj','izobrazevanje-in-mladi','projekti','ekipa-in-izkusnje','sodelovanje','publikacije-in-objave','kontakt','zasebnost','viri-fotografij','projekti/obala-v-podatkih','projekti/mladi-za-pregledne-odlocitve','projekti/graditeljska-dediscina-kostela']:
            resp=page.goto('http://127.0.0.1:8765/'+(slug+'/' if slug else ''),wait_until='domcontentloaded',timeout=20000)
            assert resp and resp.status==200,(slug,resp.status if resp else None)
            assert page.locator('h1').count()==1,slug
        report['local']['routes']=14
        try:
            resp=page.goto('https://zavod-zzt.eu/',wait_until='domcontentloaded',timeout=20000)
            report['live']={'status':resp.status if resp else None,'title':page.title(),'hasZZT':page.locator('h1').count()==1,'url':page.url}
        except Exception as exc:
            report['live']={'status':'unverified','reason':str(exc)[:300]}
        browser.close()
    (OUT/'browser qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
finally:
    server.terminate()
    try:server.wait(timeout=5)
    except:server.kill()
