#!/usr/bin/env python3
"""ZZT static publication contract: verified, reproducible checks."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
import xml.etree.ElementTree as ET
import re

ROOT=Path(__file__).resolve().parents[1]/'site'
PAGES=sorted(ROOT.rglob('index.html'))
assert len(PAGES)==11, f'Expected 11 pages; found {len(PAGES)}'

class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links=[]
        self.images=[]
        self.headings=0
        self.titles=0
        self.desc=0
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if tag in ('a','link') and d.get('href'):
            self.links.append(d['href'])
        if tag=='img':
            self.images.append(d)
        if tag=='h1':
            self.headings+=1
        if tag=='title':
            self.titles+=1
        if tag=='meta' and d.get('name')=='description' and d.get('content'):
            self.desc+=1

for f in PAGES:
    html=f.read_text(encoding='utf-8')
    parsed=Links();parsed.feed(html)
    assert parsed.headings==1,(f,'h1 count',parsed.headings)
    assert parsed.titles==1,(f,'title count',parsed.titles)
    assert parsed.desc==1,(f,'description count',parsed.desc)
    assert 'zavod-zzt.eu' in html,(f,'canonical missing')
    for href in parsed.links:
        if not href.startswith('/'):continue
        path=unquote(urlsplit(href).path.lstrip('/'))
        target=(ROOT/path)
        if path.endswith('/') or not path:
            target=target/'index.html'
        assert target.exists(),(f,'broken internal link',href)
    for img in parsed.images:
        assert img.get('alt'),(f,'image alt missing')
        assert img.get('src','').startswith(('https://commons.wikimedia.org/','/assets/')),(f,'unknown photo origin',img.get('src'))

home=(ROOT/'index.html').read_text(encoding='utf-8')
assert home.count('commons.wikimedia.org/wiki/File:Kolpa')>=3,'Homepage needs three authentic Kolpa photos'
assert 'dan.grmusa@gmail.com' in home,'Real contact absent'
assert 'Dan Fredi Grmuša' in home,'Founder absent'
for disallowed in ('14+ izvedenih projektov','20+ strokovnjakov','Sofinancira Evropska unija','lorem ipsum'):
    assert disallowed.lower() not in home.lower(),('Invented claim',disallowed)
robots=(ROOT/'robots.txt').read_text(encoding='utf-8')
assert 'User-agent: *\nAllow: /\nSitemap:' in robots,'Robots formatting invalid'
assert '\\n' not in robots,'Robots contains escaped newlines'
assert (ROOT/'CNAME').read_text(encoding='utf-8').strip()=='zavod-zzt.eu'
tree=ET.parse(ROOT/'sitemap.xml')
entries=tree.findall('{http://www.sitemaps.org/schemas/sitemap/0.9}url')
assert len(entries)==len(PAGES),(len(entries),len(PAGES))
for page in PAGES:
    html=page.read_text(encoding='utf-8')
    for marker in ('Matična številka','<dt>PIC</dt>','<dt>OID</dt>','"streetAddress"'):
        assert marker not in html,(page,'unnecessary registration field',marker)
    assert not re.search(r'(?<![0-9])(?:[0-9]{9,10}|E[0-9]{8})(?![0-9])',html),(page,'unexpected registration identifier')
    for withdrawn in ('projekti/obala-v-podatkih/','projekti/mladi-za-pregledne-odlocitve/','projekti/graditeljska-dediscina-kostela/','Prijava v pripravi'):
        assert withdrawn not in html,(page,'withdrawn proposal still visible',withdrawn)
assert (ROOT/'assets'/'research-areas.json').is_file()
assert not (ROOT/'assets'/'projects.json').exists()
assert 'Hipoteza' in (ROOT/'projekti'/'index.html').read_text(encoding='utf-8')
print(f'QA PASS: {len(PAGES)} pages, links, canonical tags, 3 Kolpa photos, attribution source pattern, sitemap and robots')
