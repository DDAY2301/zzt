#!/usr/bin/env python3
"""Cache approved Wikimedia Commons photographs in the Pages artifact.

Original source/author/licence links stay in HTML. On network failure, the
original public Commons image URL is retained and a fallback is shown by JS.
This operation does not modify originals or erase provenance.
"""
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlsplit,unquote
from hashlib import sha256
import json,re

OUT=Path(__file__).resolve().parents[1]/'site'
ASSETS=OUT/'assets'/'photos'
ASSETS.mkdir(parents=True,exist_ok=True)
pages=list(OUT.rglob('*.html'))
pattern=re.compile(r'<img\s+src="(https://commons\.wikimedia\.org/wiki/Special:FilePath/[^"]+)"')
urls=sorted({m for page in pages for m in pattern.findall(page.read_text(encoding='utf-8'))})
manifest=[]
for url in urls:
  name=unquote(urlsplit(url).path.rsplit('/',1)[-1])
  # The image catalogue is maintained in src/build_site.py; no other URLs allowed.
  if not name.lower().endswith(('.jpg','.jpeg','.png','.webp')):
    print('SKIP unsupported image extension:',name)
    continue
  ext=Path(name).suffix.lower()
  asset_name=sha256(url.encode()).hexdigest()[:16]+ext
  dest=ASSETS/asset_name
  try:
    req=Request(url,headers={'User-Agent':'Mozilla/5.0 (compatible; ZZTPublicWebsite/1.0; +https://zavod-zzt.eu/)', 'Accept':'image/jpeg,image/png,image/webp,*/*;q=0.8'})
    with urlopen(req,timeout=24) as response:
      mime=response.headers.get('Content-Type','')
      data=response.read(9_000_001)
    if not mime.startswith('image/') or not 1000<len(data)<=9_000_000:
      raise ValueError(f'Unexpected image response: type={mime}, size={len(data)}')
    if ext in ('.jpg','.jpeg') and data[:2]!=bytes([0xff,0xd8]):
      raise ValueError('Not a JPEG')
    dest.write_bytes(data)
    local='/assets/photos/'+asset_name
    for page in pages:
      html=page.read_text(encoding='utf-8')
      if f'src="{url}"' in html:
        page.write_text(html.replace(f'src="{url}"',f'src="{local}"'),encoding='utf-8')
    manifest.append({'source':url,'asset':local,'bytes':len(data),'status':'cached'})
    print('CACHED',name,len(data),'bytes')
  except Exception as exc:
    manifest.append({'source':url,'status':'remote-fallback','reason':str(exc)[:180]})
    print('WARNING photo remains externally hosted:',name,str(exc)[:160])
(ASSETS/'manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2),encoding='utf-8')
print('Photographs:',len(manifest),'cached:',sum(r['status']=='cached' for r in manifest))
