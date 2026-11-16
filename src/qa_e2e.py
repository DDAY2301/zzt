#!/usr/bin/env python3
"""Browser QA of the generated ZZT website; also probes the real custom domain."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import subprocess,time,json,sys,re

BASE=Path(__file__).resolve().parents[1]
OUT=BASE/'qa_artifacts';OUT.mkdir(exist_ok=True)
server=subprocess.Popen([sys.executable,'-m','http.server','8765','--directory',str(BASE/'site')],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
report={'local':{},'live':{},'errors':[]}
try:
    time.sleep(1.2)
    with sync_playwright() as p:
        browser=p.chromium.launch(headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        for label,width,height in [('desktop',1440,900),('tablet',820,1000),('small_tablet',768,1024),('mobile',390,844),('small_mobile',360,780)]:
            context=browser.new_context(viewport={'width':width,'height':height},device_scale_factor=1)
            page=context.new_page()
            errors=[]
            page.on('pageerror',lambda error:errors.append(str(error)))
            response=page.goto('http://127.0.0.1:8765/',wait_until='networkidle',timeout=30000)
            assert response.status==200,(label,response.status)
            assert page.locator('h1').count()==1,label
            assert page.locator('a[href="/projekti/"]').count()>=1,label
            measured=page.evaluate('({scroll:document.documentElement.scrollWidth,viewport:innerWidth})')
            if measured['scroll']>width+1:
                offenders=page.evaluate("""() => [...document.querySelectorAll('body *')].map(el => {let r=el.getBoundingClientRect(); return {tag:el.tagName, cls:String(el.className).slice(0,110), text:(el.textContent||'').trim().slice(0,75), left:Math.round(r.left),right:Math.round(r.right),width:Math.round(r.width)} }).filter(x => x.right>innerWidth+1 || x.left < -2).slice(0,20)""")
                print('OVERFLOW DETAILS',label,json.dumps(offenders,ensure_ascii=False),flush=True)
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
            assert sizes[0]['src'].endswith('.webp'), (label, 'responsive homepage photo not selected')
            caption = page.locator('.front-hero-photo figcaption')
            assert caption.evaluate("(el) => el.getBoundingClientRect().top >= el.previousElementSibling.getBoundingClientRect().bottom - 1"), (label, 'credit overlays photograph')
            caption.locator('a').click(trial=True, timeout=5000)
            if width<=1180:
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
                photo_frame = page.locator('.front-intro-photo .photo-frame')
                photo = photo_frame.locator('img').element_handle()
                page.wait_for_function("(el) => getComputedStyle(el).opacity === '0.78'", arg=photo, timeout=5000)
                photo_frame.scroll_into_view_if_needed()
                page.wait_for_function("(el) => getComputedStyle(el).opacity === '1'", arg=photo, timeout=5000)
                page.evaluate("window.scrollTo({top: 0, behavior: 'instant'})")
                page.wait_for_function("(el) => getComputedStyle(el).opacity === '0.78'", arg=photo, timeout=5000)
                page.emulate_media(reduced_motion='reduce')
                assert photo.evaluate("(el) => getComputedStyle(el).opacity === '1' && getComputedStyle(el).transitionDuration === '0s'")
                page.emulate_media(reduced_motion='no-preference')
                report['local']['photo_fade_and_reduced_motion'] = True

                page.locator('nav.main-nav a[href="/projekti/"]').click()
                assert page.url.endswith('/projekti/'),'Project navigation failed'
                assert page.locator('h1').count()==1,'Projects h1'
                for title in ('Okolje in primerljivi podatki', 'Razumljive okoljske odločitve', 'Dediščina in lokalni materiali'):
                    page.goto('http://127.0.0.1:8765/', wait_until='domcontentloaded')
                    page.get_by_role('link', name=f'Metoda in ozadje: {title}', exact=True).click()
                    assert '/projekti/#' in page.url, (title, page.url)
                    assert page.locator('h2:target').inner_text() == title, (title, page.url)
                    assert page.locator('h2:target').locator('xpath=..').get_by_text('Predvidena metoda:', exact=True).is_visible(), title
                report['local']['research_method_links'] = 3
                page.goto('http://127.0.0.1:8765/kontakt/',wait_until='domcontentloaded')
                assert page.locator('a.contact-mail').get_attribute('href')=='mailto:dan.grmusa@gmail.com','Contact email'
                page.goto('http://127.0.0.1:8765/', wait_until='domcontentloaded')
                page.get_by_role('link', name='Osebne reference in organizacije').click()
                assert page.locator('#organizacije .organisation-list li').count() >= 7
            context.close()
        context=browser.new_context(viewport={'width':1280,'height':800})
        page=context.new_page()
        for slug in ['','o-zavodu','raziskave-in-razvoj','izobrazevanje-in-mladi','projekti','ekipa-in-izkusnje','sodelovanje','publikacije-in-objave','kontakt','zasebnost','viri-fotografij']:
            resp=page.goto('http://127.0.0.1:8765/'+(slug+'/' if slug else ''),wait_until='domcontentloaded',timeout=20000)
            assert resp and resp.status==200,(slug,resp.status if resp else None)
            assert page.locator('h1').count()==1,slug
        report['local']['routes']=11
        # Production must show the actual homepage, not a README auto-page.
        try:
            live_ok=False
            for attempt in range(6):
                resp=page.goto('https://zavod-zzt.eu/',wait_until='domcontentloaded',timeout=20000)
                h1=page.locator('h1').first.inner_text() if page.locator('h1').count()==1 else ''
                live_ok=bool(resp and resp.status==200 and 'Razumeti okolje.' in h1)
                if live_ok:
                    break
                page.wait_for_timeout(2500)
            report['live']={'status':resp.status if resp else None,'title':page.title(),'hasZZT':live_ok,'url':page.url,'h1':h1,'attempts':attempt+1}
            if not live_ok:
                report['errors'].append('Production homepage is not the actual ZZT website')
            else:
                for slug in ('projekti','kontakt'):
                    visit=page.goto('https://zavod-zzt.eu/'+slug+'/',wait_until='domcontentloaded',timeout=20000)
                    if not (visit and visit.status==200 and page.locator('h1').count()==1):
                        report['errors'].append('Production route failed: '+slug)
                    visible=page.locator('body').inner_text()
                    if slug=='projekti':
                        if 'Okolje in primerljivi podatki' not in visible or 'Hipoteza za preverjanje' not in visible:
                            report['errors'].append('Production research topics are not current')
                        if any(x in visible for x in ('Prijava v pripravi','RISTANC','Living Legacy','CSF —')):
                            report['errors'].append('Unfunded project cards still shown on production')
                    if slug=='kontakt':
                        if 'dan.grmusa@gmail.com' not in visible:
                            report['errors'].append('Founder contact missing from production')
                        if re.search(r'(?i)(?:matična številka|\bPIC\s+\d{9}\b|\bOID\s+E\d{8}\b|\bSlavski Laz\s+\d+\b)',visible):
                            report['errors'].append('Unnecessary registration identifiers remain on production')
                report['live']['checked_routes']=['/','/projekti/','/kontakt/']
        except Exception as exc:
            report['live']={'status':'unverified','reason':str(exc)[:300]}
            report['errors'].append('Production verification failed: '+str(exc)[:150])
        browser.close()
    (OUT/'browser qa.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    assert not report['errors'], report['errors']
finally:
    server.terminate()
    try:server.wait(timeout=5)
    except:server.kill()
