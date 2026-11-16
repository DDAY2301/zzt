"""Isolated DOM/CSS browser checks. Browser policy disallows file/http navigation."""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json,re
OUT=Path(__file__).resolve().parents[1]
ROOT=OUT/'site'
CSS=(ROOT/'assets/site.css').read_text(encoding='utf8')
CSS=re.sub(r'@import\s+url\([^)]*\);','',CSS)
JS=(ROOT/'assets/site.js').read_text(encoding='utf8')
report={'browser_environment':'Browser blocks file/http navigation (ERR_BLOCKED_BY_ADMINISTRATOR); DOM render checks use set_content','results':{},'errors':[]}
def content(slug):
 p=ROOT/(slug.strip('/')+'/' if slug else '')/'index.html'
 html=p.read_text(encoding='utf8')
 html=html.replace('</head>',f'<style>{CSS}</style></head>')
 # external font and Wikimedia images cannot be loaded in this environment; CSS fallbacks tested
 return html
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path='/usr/bin/chromium',args=['--no-sandbox','--disable-dev-shm-usage'])
 for label,size in [('desktop',{'width':1440,'height':900}),('mobile',{'width':390,'height':844}),('tablet',{'width':820,'height':1000})]:
  ctx=browser.new_context(viewport=size,device_scale_factor=1)
  page=ctx.new_page()
  page.set_content(content(''),wait_until='domcontentloaded')
  page.add_script_tag(content=JS)
  page.wait_for_timeout(250)
  page.screenshot(path=str(OUT/f'ZZT predogled {label}.png'),full_page=True,animations='disabled')
  info=page.evaluate('''() => ({width:document.documentElement.scrollWidth, view:innerWidth, title:document.title, main:!!document.querySelector('main'), heading:document.querySelector('h1')?.innerText, nav:document.querySelectorAll('.main-nav a').length})''')
  if info['width']>info['view']+1:report['errors'].append(f'{label}: horizontal overflow {info}')
  report['results'][label]=info
  if label=='mobile':
   b=page.locator('.menu-toggle')
   b.click()
   assert b.get_attribute('aria-expanded')=='true','mobile menu should open'
   assert page.locator('#main-nav a[href="/projekti/"]').is_visible()
   b.press('Escape')
   assert b.get_attribute('aria-expanded')=='false','escape should close'
   b.click()
   assert page.locator('.main-nav').evaluate("e => getComputedStyle(e).display")!='none'
   report['results']['mobile']['interactions']=['menu open','ESC closes','navigation is visible when opened']
  if label=='desktop':
   page.set_content(content('kontakt'),wait_until='domcontentloaded')
   ml=page.locator('a.contact-mail')
   assert ml.count()==1
   assert ml.get_attribute('href').startswith('mailto:')
   report['results']['desktop']['contact']='mailto link verified; email delivery not tested'
  ctx.close()
 # Render each page in DOM to confirm headings/JS (not actual route networking)
 ctx=browser.new_context(viewport={'width':1024,'height':768})
 page=ctx.new_page()
 for f in ROOT.rglob('index.html'):
  slug=str(f.relative_to(ROOT).parent).replace('.','')
  page.set_content(content(slug),wait_until='domcontentloaded')
  h=page.locator('h1')
  assert h.count()==1,(slug,h.count())
 report['results']['page_dom']=14
 ctx.close();browser.close()
(OUT/'QA Browser Results.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf8')
print(json.dumps(report,ensure_ascii=False,indent=2))
