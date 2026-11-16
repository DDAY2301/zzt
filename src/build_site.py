#!/usr/bin/env python3
"""Compile the ZZT public institutional website. No third-party dependencies."""
from pathlib import Path
from hashlib import sha256
from html import escape
from urllib.parse import quote
import json

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'site'
AS=OUT/'assets'
AS.mkdir(parents=True,exist_ok=True)
STYLE_REVISION = sha256((AS / 'site.css').read_bytes()).hexdigest()[:12]
SCRIPT_REVISION = sha256((AS / 'site.js').read_bytes()).hexdigest()[:12]
TITLE='ZZT – Zavod za zeleno tehnologijo'
EMAIL='dan.grmusa@gmail.com'
HERO_SRCSET='/assets/photos/kolpa-960.webp 960w, /assets/photos/kolpa-1600.webp 1600w'
HERO_SIZES='(max-width: 760px) 100vw, 50vw'
MAIL=f'mailto:{EMAIL}?subject='+quote('Sodelovanje z ZZT – povpraševanje')
PHOTOS={
 'kolpa_kuzelj': {'src':'https://commons.wikimedia.org/wiki/Special:FilePath/Kolpa_a.k.a_Kupa_between_Kuzelj_and_Gasparci_15.jpg?width=1600','file':'Kolpa a.k.a Kupa between Kuzelj and Gasparci 15.jpg','name':'Reka Kolpa med Kužljem in Gašparci (2026)','author':'Ajznponar','licence':'CC0 1.0','url':'https://commons.wikimedia.org/wiki/File:Kolpa_a.k.a_Kupa_between_Kuzelj_and_Gasparci_15.jpg'},
 'kolpa_bosljiva': {'src':'https://commons.wikimedia.org/wiki/Special:FilePath/Kolpa_at_the_Na_gricku_park_in_Bosljiva_Loka_03.jpg?width=1400','file':'Kolpa at the Na gricku park in Bosljiva Loka 03.jpg','name':'Kolpa pri Bosljivi Loki (2026)','author':'Ajznponar','licence':'CC0 1.0','url':'https://commons.wikimedia.org/wiki/File:Kolpa_at_the_Na_gricku_park_in_Bosljiva_Loka_03.jpg'},
 'kolpa': {'src':'https://commons.wikimedia.org/wiki/Special:FilePath/KolpaRiver-Slovenia.JPG?width=1400', 'file':'KolpaRiver-Slovenia.JPG', 'name':'Reka Kolpa, Slovenija','author':'Žiga','licence':'Public domain','url':'https://commons.wikimedia.org/wiki/File:KolpaRiver-Slovenia.JPG'},
 'kostel': {'src':'https://commons.wikimedia.org/wiki/Special:FilePath/Kostel_Castle.jpg?width=1200','file':'Kostel Castle.jpg','name':'Grad Kostel','author':'Miran Hladnik','licence':'CC BY-SA 2.5 SI','url':'https://commons.wikimedia.org/wiki/File:Kostel_Castle.jpg'},
 'izola': {'src':'https://commons.wikimedia.org/wiki/Special:FilePath/Izola_-_Petelinji_rt_s_svetilnikom_(2014).jpg?width=1200','file':'Izola – Petelinji rt s svetilnikom (2014).jpg','name':'Izola, Svetilnik','author':'Wikimedia Commons / izvirnik Pixabay','licence':'CC0 1.0','url':'https://commons.wikimedia.org/wiki/File:Izola_-_Petelinji_rt_s_svetilnikom_(2014).jpg'},
 'ankaran': {'src':'https://commons.wikimedia.org/wiki/Special:FilePath/Ankaran_(13470221084).jpg?width=1200','file':'Ankaran (13470221084).jpg','name':'Debeli rtič pri Ankaranu','author':'Andrea Skerlavaj','licence':'CC BY-SA 2.0','url':'https://commons.wikimedia.org/wiki/File:Ankaran_(13470221084).jpg'},
}
# The Koper image is deliberately not displayed: its rights were not sufficiently cross-checked.
NAV=[('','Domov'),('o-zavodu','O zavodu'),('raziskave-in-razvoj','Raziskave in razvoj'),('izobrazevanje-in-mladi','Izobraževanje in mladi'),('projekti','Raziskovalne smeri'),('ekipa-in-izkusnje','Ekipa in izkušnje'),('sodelovanje','Sodelovanje'),('publikacije-in-objave','Publikacije in objave'),('kontakt','Kontakt')]

AREAS=[
 dict(id='okolje-in-primerljivi-podatki',title='Okolje in primerljivi podatki',tag='Okoljske raziskave',photo='izola',link='raziskave-in-razvoj',question='Kako se opaženi odpadki razlikujejo med obalnimi lokacijami?',hypothesis='Na opaženo količino in sestavo lahko vplivajo dostopnost, raba prostora in čas opazovanja. To je hipoteza, ne ugotovitev.',method='Predvideni so ponovljivi popisi enako dolgih odsekov, enotne kategorije in zapis okoliščin.',source='JRC: spremljanje morskih odpadkov',source_url='https://publications.jrc.ec.europa.eu/repository/handle/JRC133594'),
 dict(id='razumljive-okoljske-odlocitve',title='Razumljive okoljske odločitve',tag='Sodelovanje javnosti',photo='ankaran',link='izobrazevanje-in-mladi',question='Ali jasni povzetki uradnih gradiv olajšajo sodelovanje prebivalcev?',hypothesis='Razlaga dokumentov lahko izboljša razumevanje možnosti za sodelovanje. Dejanski učinek bi bilo treba preveriti.',method='Pregled uradnih virov, nevtralni povzetki in prostovoljna ocena njihove razumljivosti.',source='UNECE: Aarhuška konvencija',source_url='https://unece.org/environment-policy/public-participation/aarhus-convention/text'),
 dict(id='dediscina-in-lokalni-materiali',title='Dediščina in lokalni materiali',tag='Trajnost in dediščina',photo='kostel',link='raziskave-in-razvoj',question='Kaj lahko preverjene tradicionalne gradbene prakse prispevajo k sodobni uporabi materialov?',hypothesis='Izbrane tradicionalne rešitve so lahko koristno izhodišče, vendar jih je treba preveriti glede na današnje zahteve.',method='Pregled registrov in literature, dokumentiranje s soglasji ter neodvisen strokovni pregled.',source='UNESCO: etika varovanja dediščine',source_url='https://ich.unesco.org/en/ethics-and-ich-00866')
]

def url(slug=''):
 return '/' + (slug.strip('/')+'/' if slug else '')

def link(slug,label,cls='',extra=''):
 return f'<a href="{url(slug)}" class="{cls}" {extra}>{label}</a>'

def ext(href,title,cls='text-link'):
 return f'<a class="{cls}" href="{escape(href,quote=True)}" target="_blank" rel="noopener noreferrer">{escape(title)} <span aria-hidden="true">↗</span></a>'

def photo(key, cls='', loading='lazy'):
 p = PHOTOS[key]
 priority = ' fetchpriority="high"' if loading == 'eager' else ''
 responsive = f' srcset="{HERO_SRCSET}" sizes="{HERO_SIZES}"' if key == 'kolpa_kuzelj' else ''
 name = escape(p['name'])
 credit = ext(p['url'], f'{p["author"]} / {p["licence"]}', 'source-link')
 return f'''<figure class="photo {cls}" data-photo="{key}">
  <div class="photo-frame">
   <img src="{escape(p['src'], quote=True)}"{responsive} alt="{name}" loading="{loading}" decoding="async" referrerpolicy="no-referrer"{priority}>
   <div class="photo-fallback" role="status">Fotografija trenutno ni dosegljiva.</div>
  </div>
  <figcaption><span>{name}</span>{credit}</figcaption>
 </figure>'''

def eyebrow(t):
 return f'<p class="eyebrow">{escape(t)}</p>'

def hero(kicker, title, lead, side=''):
 image_class = ' page-hero-grid--image' if side else ''
 label = eyebrow(kicker) if kicker.casefold() != title.casefold() else ''
 return f'''<section class="page-hero">
  <div class="wrap page-hero-grid{image_class}">
   <div>{label}<h1>{title}</h1><p class="lead">{lead}</p></div>
   {side}
  </div>
 </section>'''

def band(t): return f'<div class="section-heading">{eyebrow(t)}</div>'
def wrap(section):return f'<div class="wrap">{section}</div>'

def home():
 cards = ''.join(
  f'''<article class="visual-project research-area">
   {photo(a["photo"], "tile-photo")}
   <div class="visual-project-body">
    {eyebrow(a["tag"])}<h3>{escape(a["title"])}</h3>
    <p>{escape(a["question"])}</p>
    <a href="{url('projekti')}#{escape(a["id"], quote=True)}" class="text-link" aria-label="Metoda in ozadje: {escape(a["title"], quote=True)}">Metoda in ozadje</a>
   </div>
  </article>'''
  for a in AREAS
 )
 fields = [
  ('raziskave-in-razvoj', 'Okolje in podatki', 'Primerljivi terenski popisi, pregled virov in analiza okoljskih podatkov.'),
  ('izobrazevanje-in-mladi', 'Izobraževanje in mladi', 'Učne vsebine o okoljskih dokumentih, digitalni pismenosti in sodelovanju.'),
  ('sodelovanje', 'Projektno sodelovanje', 'Priprava projektnih predlogov s šolami, raziskovalci in lokalnimi skupnostmi.'),
 ]
 field_links = ''.join(
  f'<article><h3>{link(slug, title)}</h3><p>{description}</p></article>'
  for slug, title, description in fields
 )
 return f'''<section class="front-hero">
  <div class="wrap front-hero-grid">
   <div class="front-content">
    {eyebrow('Kostel, Slovenija')}
    <h1>Razumeti okolje. <em>Razvijati uporabne rešitve.</em></h1>
    <p class="front-lead">V Kostelu razvijamo raziskovalne in izobraževalne pobude o zelenih tehnologijah, rabi virov in lokalnem okolju.</p>
    <div class="hero-actions">{link('projekti', 'Raziskovalne smeri', 'btn primary')}{link('o-zavodu', 'Spoznajte zavod', 'text-link')}</div>
   </div>
   {photo('kolpa_kuzelj', 'front-hero-photo', 'eager')}
  </div>
 </section>
 <section class="section front-focus">
  <div class="wrap">
   <h2>Področja dela</h2>
   <div class="front-focus-grid">{field_links}</div>
  </div>
 </section>
 <section class="section cream-section front-projects">
  <div class="wrap">
   <div class="front-section-title">
    <div><h2>Raziskovalne smeri</h2><p>Vprašanja in metode za raziskave, ki jih šele načrtujemo.</p></div>
    {link('projekti', 'Vse raziskovalne smeri', 'text-link')}
   </div>
   <div class="visual-project-grid">{cards}</div>
  </div>
 </section>
 <section class="section front-intro">
  <div class="wrap front-intro-grid">
   <div><h2>Zavod iz Kostela</h2><p class="big-paragraph">ZZT je zasebni nepridobitni zavod, ustanovljen leta 2026.</p><p>Pri načrtovanju pobud izhajamo iz raziskovalnih virov in potreb ljudi, ki jih posamezna tema zadeva.</p>{link('o-zavodu', 'Poslanstvo in podatki o zavodu', 'text-link')}</div>
   {photo('kolpa_bosljiva', 'front-intro-photo')}
  </div>
 </section>
 <section class="section cream-section front-kolpa">
  <div class="wrap front-kolpa-grid">
   {photo('kolpa', 'front-kolpa-photo')}
   <div><h2>Kolpa in lokalno okolje</h2><p>Kostel je izhodišče za delo o lokalni dediščini, rabi materialov in vprašanjih trajnostnega razvoja.</p>{link('sodelovanje', 'Predlagajte sodelovanje', 'text-link')}</div>
  </div>
 </section>
 <section class="section front-experience">
  <div class="wrap two-col">
   <h2>Izkušnje ustanovitelja</h2>
   <div><p>Dan Fredi Grmuša ima izkušnje s pripravo evropskih prijav in koordinacijo slovenske mladinske skupine v projektu DCYDE!.</p>{link('ekipa-in-izkusnje', 'Osebne reference in organizacije', 'text-link')}</div>
  </div>
 </section>
 <section class="section olive-section front-cta">
  <div class="wrap front-cta-grid">
   <div><h2>Sodelujte z ZZT</h2><p>Za projektne predloge in vprašanja o našem delu.</p></div>
   <a class="btn primary" href="{MAIL}">Pišite: {EMAIL}</a>
  </div>
 </section>'''

def about():
 return hero('O zavodu / ZZT','Zavod za zeleno tehnologijo','Ustanovljeni smo z namenom povezovanja raziskav, zelenih tehnologij in izobraževanja mladih.',photo('kostel','page-hero-photo'))+f'''<section class="section"><div class="wrap two-col">{band('Pravna podlaga')}<div><h2>Nepridobitni zasebni zavod.</h2><p>ZZT – Zavod za zeleno tehnologijo je bil ustanovljen 29. septembra 2026, vpis v sodni register pa je bil opravljen 21. oktobra 2026. Poslanstvo je opredeljeno v ustanovitvenem aktu.</p><p>Temeljni namen je spodbujanje mladih pri razvoju, razumevanju in uporabi novih zelenih tehnologij, trajnostnih rešitev, digitalnih orodij ter zelenih in prihodnostnih kompetenc.</p><p>Pri javni predstavitvi ločujemo dejansko registrirane dejavnosti od rezultatov, ki jih bomo šele ustvarili.</p></div></div></section>
 <section class="section cream-section"><div class="wrap"><div class="section-title-row">{band('Organizacija')}<h2>Dejavnosti po ustanovitvenem aktu</h2></div><div class="facts-grid"><div><h3>Raziskave in razvoj</h3><p>Zelene tehnologije, krožno gospodarstvo, energetska učinkovitost, okoljske inovacije (7. in 8. člen).</p></div><div><h3>Izobraževanje in mladi</h3><p>Neformalno izobraževanje, mentorstvo, delavnice, socialno vključevanje in medgeneracijsko sodelovanje.</p></div><div><h3>Digitalno delo</h3><p>Programska in spletna orodja, založništvo, javne publikacije ter digitalna gradiva.</p></div><div><h3>Mednarodni projekti</h3><p>Priprava, prijava, upravljanje in izvajanje domačih, evropskih ter Erasmus+ projektov.</p></div></div></div></section>
 <section class="section"><div class="wrap two-col">{band('Podatki')}<div><h2>Pravna identiteta</h2><dl class="dl"><div><dt>Naziv</dt><dd>ZZT – Zavod za zeleno tehnologijo</dd></div><div><dt>Območje sedeža</dt><dd>Kostel, Slovenija</dd></div><div><dt>Pravna oblika</dt><dd>Zasebni nepridobitni zavod</dd></div><div><dt>Ustanovitev</dt><dd>September 2026</dd></div><div><dt>Ustanovitelj in projektni kontakt</dt><dd>Dan Fredi Grmuša</dd></div><div><dt>E-pošta</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div></dl><p class="note">Zavod je registriran kot zasebna nepridobitna pravna oseba. Na javni strani ne predstavljamo upravnih oznak, razvojnih idej ali prijav kot dokaz pridobljenega financiranja.</p></div></div></section>'''

def research():
 topics=''.join(f'''<article class="research-topic"><span class="eyebrow">{escape(a["tag"])}</span><h3>{escape(a["question"])}</h3><p><strong>Hipoteza:</strong> {escape(a["hypothesis"])}</p><p><strong>Možen pristop:</strong> {escape(a["method"])}</p>{ext(a["source_url"],a["source"])}</article>''' for a in AREAS)
 return hero('Raziskave in razvoj','Okoljske raziskave in razvoj','Predstavljamo strokovna izhodišča in hipoteze, za katere je treba podatke še pridobiti.',photo('ankaran','page-hero-photo'))+f'''<section class="section"><div class="wrap two-col">{band('Raziskovalni pristop')}<div><h2>Primerljivost ni samoumevna.</h2><p>Podatki iz dveh lokacij niso neposredno primerljivi, če so bili zbrani z različnimi merili. Zato najprej določimo raziskovalno vprašanje, enote opazovanja, popisne kategorije in način preverjanja zapisov.</p><ol class="method-list"><li><strong>Vprašanje in literatura</strong><span>Pregledamo obstoječe raziskave, opredelimo hipotezo ter neznanke.</span></li><li><strong>Protokol</strong><span>Načrtujemo ponovljiv postopek, okoliščine vzorčenja in minimalno dokumentacijo.</span></li><li><strong>Preverjanje</strong><span>Ugotavljamo morebitne napake, omejitve in odstopanja med popisi.</span></li><li><strong>Interpretacija</strong><span>Če bo zbiranje izvedeno, bomo ločili izmerjeno dejstvo od sklepa in javno navedli omejitve.</span></li></ol></div></div></section><section class="section cream-section"><div class="wrap"><div class="section-title-row">{band('Raziskovalna vprašanja')}<h2>Možne smeri nadaljnjega dela.</h2></div><div class="research-topics">{topics}</div><p class="note">To niso ugotovitve zaključenih projektov ZZT. Namen je razviti strokovno izvedljive raziskovalne naloge.</p></div></section>'''

def education():
 return hero('Izobraževanje in mladi','Izobraževanje in mladinsko delo','Učna vprašanja povezujemo s podatki, viri in sposobnostjo argumentirane presoje.')+f'''<section class="section"><div class="wrap two-col">{band('Izobraževanje')}<div><h2>Od vira do razumljive razlage.</h2><p>Predlagamo kratke učne enote, v katerih mladi primerjajo trditve z izvirnimi dokumenti, prepoznajo negotovosti in svoje ugotovitve predstavijo drugim.</p><div class="stack-items"><article><h3>Okoljska pismenost</h3><p>Kako ločiti opažanje od meritve? Katere podatke potrebujemo, preden primerjamo dve obalni lokaciji?</p></article><article><h3>Digitalna pismenost</h3><p>Preverjanje izvora podatkov, osnovna evidenca, zanesljivost grafov in odgovorna uporaba digitalnih orodij.</p></article><article><h3>Projektno sodelovanje</h3><p>Razdelitev nalog, posvetovanje z javnostjo ter priprava kratkega poročila z jasno navedenimi viri.</p></article></div></div></div></section><section class="section olive-section"><div class="wrap two-col">{band('Predvideni preizkus')}<div><h2>Bi lahko iz strokovnega gradiva nastalo uporabno učno orodje?</h2><p>Možna delavnica bi uporabila javno objavljen okoljski dokument. Udeleženci bi izluščili dejstva, zapisali odprta vprašanja in sestavili kratek nevtralen povzetek. Razumevanje bi bilo mogoče preveriti s prostovoljnim vprašalnikom pred in po dejavnosti.</p><p>Gre za predlog, ne za že izvedeno delavnico. Izkušnje ustanovitelja v projektih DCYDE, VIBE in drugih mladinskih dejavnostih lahko prispevajo k organizaciji in pripravi gradiv.</p>{link('ekipa-in-izkusnje','Osebne izkušnje ustanovitelja','text-link')}</div></div></section>'''

def projects():
 cards=''.join(f'''<article class="visual-project research-area"><div class="visual-project-media">{photo(a["photo"],"tile-photo")}</div><div class="visual-project-body"><p class="status">Področje v razvoju</p><h2 id="{escape(a["id"],quote=True)}" tabindex="-1">{escape(a["title"])}</h2><p class="research-question">{escape(a["question"])}</p><p><strong>Hipoteza za preverjanje:</strong> {escape(a["hypothesis"])}</p><p><strong>Predvidena metoda:</strong> {escape(a["method"])}</p>{ext(a["source_url"],a["source"])}<a href="{url(a["link"])}" class="text-link">Več o delu ↗</a></div></article>''' for a in AREAS)
 return hero('Raziskovalne smeri','Tri raziskovalna vprašanja','To so načrtovane raziskovalne smeri, ne financirani projekti ali že opravljene študije.')+f'''<section class="section"><div class="wrap"><div class="front-section-title"><div>{eyebrow('Predlagana področja dela')}<h2>Predlagane metode</h2><p>Pred začetkom vsake raziskave potrebujemo pregled virov, strokovno metodo, izvedbeno ekipo, ustrezna dovoljenja in financiranje. Nobena od spodnjih hipotez še ni potrjen rezultat.</p></div></div><div class="visual-project-grid project-list">{cards}</div></div></section><section class="section olive-section"><div class="wrap two-col">{band('Nadaljnji koraki')}<div><h2>Kako bi iz zamisli nastal projekt?</h2><ol class="method-list"><li><strong>Vprašanje</strong><span>Preverimo, kaj je že znano in katera pojasnila manjkajo.</span></li><li><strong>Protokol</strong><span>Vnaprej določimo metodo, obseg, etična pravila in način preverjanja.</span></li><li><strong>Viri</strong><span>Pridobimo potrebna soglasja, strokovnjake ter razpoložljiva sredstva.</span></li><li><strong>Rezultati</strong><span>Šele izvedeno delo lahko postane javno poročilo ali referenca ZZT.</span></li></ol></div></div></section>'''

def team():
 rows = [
  ('2026', 'GREENCULTLABS', 'Creative Europe — priprava dokumentacije in oddaja prijave', 'Oddana prijava'),
  ('2026', 'CARESHIFT', 'CERV — zbiranje profilov, referenc in podatkov partnerjev', 'Oddana prijava'),
  ('2026', 'GREEN ROOTS YOUTH', 'Priprava partnerskih povzetkov in usklajevanje nalog', 'Priprava prijave'),
  ('2026', 'EKOfeed', 'Razvoj zasnove in komunikacija s potencialnimi partnerji', 'Razvoj predloga'),
  ('2026', 'DCYDE!: New Methods of Agro in Croatia', 'Vodenje devetčlanske slovenske skupine in priprava priročnika', 'Izvedba'),
  ('2026', 'DCYDE!: Cookbook from Leftovers', 'Urejanje prispevkov in projektne dokumentacije', 'Izvedba'),
  ('2026', 'DCYDE!: Youth Survival Guide', 'Uredništvo in dokumentiranje priprave gradiva', 'Izvedba'),
  ('2025', 'VIBE / The Power Within / The Future We Want', 'Sodelovanje na mladinskih usposabljanjih in izmenjavah', 'Udeležba'),
  ('2025', 'MEGAPHONE', 'Udeležba kot predstavnik organizacije Povod', 'Udeležba'),
 ]
 table = ''.join(
  f'<tr><td>{year}</td><td><strong>{escape(name)}</strong><span>{escape(description)}</span></td><td>{escape(status)}</td></tr>'
  for year, name, description, status in rows
 )
 organisations = [
  ('Povod, so. p.', 'Slovenija', 'Projektna koordinacija in zastopanje na MEGAPHONE 2025.', 'https://povod.si/contact/'),
  ('Zavod medgeneracijske vzajemnosti', 'Slovenija', 'Priprava evropskih projektnih prijav, med njimi GREENROOTS.', 'https://zmv.si/o-zmv/'),
  ('ISCOMET – Inštitut za etnične in regionalne študije', 'Slovenija', 'Sodelovanje pri mladinskih dejavnostih DCYDE!.', 'https://iscomet.org/projekti/dcyde/'),
  ('Zavod LokalPatriot', 'Slovenija', 'Slovenski partner usposabljanja VIBE, na katerem je sodeloval ustanovitelj.', 'https://lokalpatriot.si/mednarodno-usposabljanje-vibe/'),
  ('Zavod Reka Si, so. p.', 'Slovenija', 'Mladinska izmenjava The Future We Want, na kateri je sodeloval ustanovitelj.', 'https://sloga-platform.org/mednarodna-mladinska-izmenjava-the-future-we-want-bo-septembra-v-zrecah/'),
  ('Agenzia Promozione Giovani (APG)', 'Italija', 'Organizator usposabljanja VIBE.', 'https://www.salto-youth.net/tools/toy/roberto-rossetto.4639/'),
  ('TechSoup Europe', 'Mednarodno', 'Organizator dogodka MEGAPHONE 2025.', 'https://megaphone2025.techsoupeurope.org/'),
  ('Soċjetà Mużikali San Pawl', 'Malta', 'Prijavitelj usposabljanja The Power Within, na katerem je sodeloval ustanovitelj.', 'https://fondi.eu/wp-content/uploads/2026/02/MT-NA-Erasmus-Results-2025.pdf'),
  ('Centar za razvoj demokratskog društva Europolis', 'Srbija', 'Projektna komunikacija in izmenjava dokumentacije pri zasnovi EKOfeed.', 'https://www.ekapija.com/company/view/180714/centar-za-razvoj-demokratskog-drustva-europolis'),
 ]
 organisation_list = ''.join(
  f'<li><h3>{ext(href, name)}</h3><span class="location">{country}</span><p>{description}</p></li>'
  for name, country, description, href in organisations
 )
 return hero('Ekipa in izkušnje', 'Osebne projektne izkušnje', 'Projektno delo ustanovitelja ZZT v Sloveniji in mednarodnem okolju.') + f'''
 <section class="section">
  <div class="wrap two-col">
   {band('Ustanovitelj')}
   <div><h2>Dan Fredi Grmuša</h2><p class="lead">Projektna koordinacija in priprava evropskih prijav</p><p>Njegovo delo vključuje usklajevanje partnerjev, vodenje mladinskih skupin ter pripravo dokumentacije in digitalnih izobraževalnih gradiv.</p></div>
  </div>
 </section>
 <section class="section cream-section">
  <div class="wrap">
   <h2 id="osebne-reference">Dokumentirano sodelovanje.</h2>
   <p>Pregled osebnih referenc ustanovitelja ter njegove vloge pri izvedbi, oddaji prijave ali udeležbi.</p>
   <div class="table-scroller" tabindex="0" role="region" aria-labelledby="osebne-reference">
    <table class="experience-table"><thead><tr><th scope="col">Leto</th><th scope="col">Projekt in naloga</th><th scope="col">Vrsta reference</th></tr></thead><tbody>{table}</tbody></table>
   </div>
  </div>
 </section>
 <section class="section" id="organizacije">
  <div class="wrap two-col">
   <h2>Organizacije iz preteklih projektov</h2>
   <div>
    <ul class="organisation-list">{organisation_list}</ul>
    <p class="note">{ext('https://capacity4dev.europa.eu/projects/dcyde-digital-global-citizenship-youngsters-educators-partnership/info/project-consortium_en', 'Javni seznam širšega konzorcija DCYDE!')}</p>
   </div>
  </div>
 </section>
 <section class="section cream-section">
  <div class="wrap two-col">
   <h2>Upravljanje zavoda</h2>
   <div><p>Ustanovitelj je projektna kontaktna oseba. Pravno zastopanje določata ustanovitveni akt in vpis v register. Akt predvideva svet zavoda in strokovni svet.</p>{link('o-zavodu', 'Podatki o zavodu', 'text-link')}</div>
  </div>
 </section>'''

def cooperation():
 return hero('Sodelovanje','Strokovno sodelovanje','Povezujemo izvajalce, izobraževalne ustanove in organizacije okoli preverljivih ciljev.')+f'''<section class="section"><div class="wrap two-col">{band('Za koga')}<div><h2>Strokovno sodelovanje brez odvečne administracije.</h2><div class="stack-items"><article><h3>Raziskovalci in univerze</h3><p>Metodološki pregled, analiza podatkov, dostop do strokovne literature in kakovostna interpretacija.</p></article><article><h3>Šole in učitelji</h3><p>Razvoj učnih gradiv, mentorska podpora in praktična okoljska izobraževanja.</p></article><article><h3>Občine in nevladne organizacije</h3><p>Lokalno okoljsko spremljanje, vključevanje javnosti in uporaba rezultatov za odločanje.</p></article><article><h3>Mednarodni projektni partnerji</h3><p>Projektni koncepti, vsebinski prispevki, koordinacija in priprava prijavne dokumentacije.</p></article></div><a class="btn outline" href="{MAIL}">Predlagajte sodelovanje <span aria-hidden="true">↗</span></a></div></div></section><section class="section olive-section"><div class="wrap"><div class="section-title-row">{band('Načelo')}<h2>Partnerstvo potrdimo z dogovorom.</h2></div><p>Pretekli stiki ustanovitelja z organizacijami ne pomenijo, da so te organizacije formalni partnerji ZZT. Na tej strani navajamo možnosti sodelovanja, ne izmišljenih institucionalnih zavez.</p></div></section>'''

def publications():
 sources=[('Joint Research Centre — Guidance on the Monitoring of Marine Litter in European Seas (2023)','https://publications.jrc.ec.europa.eu/repository/handle/JRC133594','Metodologija spremljanja morskih odpadkov'),('Čista obala 2021 — Direkcija RS za vode','https://www.gov.si/novice/2021-09-18-cista-obala-2021/','Pretekli rezultati javne akcije in spremljanja'),('OSPAR — Beach Litter','https://www.ospar.org/work-areas/eiha/marine-litter/assessment-of-marine-litter/beach-litter','Primerljive kategorije in popisni okvir'),('ICOMOS — mednarodne strokovne listine','https://openarchive.icomos.org/','Dokumentiranje grajene dediščine'),('UNECE — Aarhuška konvencija','https://unece.org/environment-policy/public-participation/aarhus-convention/text','Dostop do informacij in vključevanje javnosti'),('OECD — Guidelines for Citizen Participation','https://www.oecd.org/en/publications/2022/09/oecd-guidelines-for-citizen-participation-processes_63b34541.html','Zasnova sodelovanja državljanov')]
 rows=''.join(f'<article class="resource"><div><h3>{escape(t)}</h3><p>{escape(d)}</p></div>{ext(u,"Odpri vir")}</article>' for t,u,d in sources)
 return hero('Objave in viri','Publikacije in strokovni viri','Ločujemo lastne bodoče projektne publikacije od raziskav in poročil drugih ustanov.')+f'''<section class="section"><div class="wrap two-col">{band('Publikacije ZZT')}<div><h2>Lastna zbirka je v nastajanju.</h2><p>ZZT kot novoustanovljeni zavod še nima javno objavljene in preverjene lastne raziskovalne publikacije. Ko bodo prve študije zaključene, bomo tukaj objavili metodologijo, rezultate, bibliografijo in pogoje ponovne uporabe.</p></div></div></section><section class="section cream-section"><div class="wrap"><div class="section-title-row">{band('Bibliografija')}<h2>Viri, na katere se opiramo.</h2></div>{rows}</div></section>'''

def contact():
 return hero('Kontakt','Kontakt za projektne pobude','Za strokovna vprašanja, projektne ideje in pobude za sodelovanje uporabite preverjeni projektni kontakt.')+f'''<section class="section"><div class="wrap contact-grid"><div>{eyebrow('Projektni kontakt')}<h2>Pišite ustanovitelju.</h2><p>Kontaktna oseba je ustanovitelj Dan Fredi Grmuša. Pišete mu lahko neposredno na spodnji naslov. Avtomatiziran kontaktni obrazec ni vzpostavljen.</p><a href="mailto:{EMAIL}" class="contact-mail">{EMAIL} <span aria-hidden="true">↗</span></a><p><strong>Kontaktna oseba:</strong> Dan Fredi Grmuša · ustanovitelj</p><p class="note">Povezava odpre vaš e-poštni program. Sporočilo se ne pošlje brez vaše potrditve v e-poštnem odjemalcu.</p></div><div class="contact-address">{eyebrow('Kje delujemo')}<address><strong>ZZT – Zavod za zeleno tehnologijo</strong><br>Kostel · Slovenija</address><hr><h3>O čem se lahko pogovorimo?</h3><p>Okoljski podatki, razvoj izobraževalnih gradiv, dokumentiranje lokalne dediščine ter predlogi za strokovno in mednarodno sodelovanje.</p><p>Za prvi stik zadostuje kratek opis teme in vprašanje, na katero bi želeli odgovoriti.</p><a href="mailto:{EMAIL}" class="text-link">Kontakt: Dan Fredi Grmuša ↗</a></div></div></section>'''

def privacy():
 return hero('Zasebnost','Zasebnost','Kaj ta izdaja spletne strani počne in česa ne.')+f'''<section class="section"><div class="wrap two-col">{band('Informacije')}<div><h2>Minimalna obdelava.</h2><p>Spletna stran nima uporabniških računov, lastnih analitičnih skript, sledilnih piškotkov ali spletnega kontaktnega obrazca. Za pošiljanje sporočila uporablja povezavo <code>mailto:</code>, ki odpre vaš e-poštni program.</p><p>Fotografije so izvirno objavljene v zbirki Wikimedia Commons in so ob objavi spletne strani shranjene tudi na gostovanju. Povezavo z Wikimedia vaš brskalnik vzpostavi, če odprete stran z izvirno fotografijo. Gostovanje zagotavlja GitHub Pages, ki lahko obdeluje tehnične podatke o dostopih skladno s svojimi pogoji.</p><p>Upravljavec vsebine je ZZT – Zavod za zeleno tehnologijo. Za zahteve v zvezi z osebnimi podatki pišite ustanovitelju na dan.grmusa@gmail.com. Obvestilo bomo posodobili ob uvedbi novih spletnih funkcij.</p></div></div></section>'''

def credits():
 rows=''.join(f'<tr><td>{escape(p["name"])}</td><td>{escape(p["author"])}</td><td>{escape(p["licence"])}</td><td>{ext(p["url"],"Izvirnik")}</td></tr>' for k,p in PHOTOS.items() if k in ('kolpa_kuzelj','kolpa_bosljiva','kolpa','kostel','izola','ankaran'))
 return hero('Viri fotografij','Avtorji in licence fotografij','Dokumentiramo avtorstvo in licence ter ne predstavljamo fotografij kot dokazov lastnih raziskav.')+f'<section class="section"><div class="wrap"><div class="table-scroller"><table class="experience-table"><thead><tr><th>Fotografija</th><th>Avtor</th><th>Licenca</th><th>Izvor</th></tr></thead><tbody>{rows}</tbody></table></div><p class="note">Slike so vizualne upodobitve lokacij; niso fotografije terenskega dela ZZT. Pri fotografijah so navedeni avtorji, oznake licenc in povezave do izvirnikov. Avtorske pravice ostanejo pri avtorjih.</p></div></section>'

PAGES={'':('Domov – ZZT','ZZT s sedežem v Kostelu povezuje okoljske raziskave, zelene tehnologije, izobraževanje mladih in razvoj projektov.',home),
 'o-zavodu':('O zavodu','Uradno poslanstvo, ustanovitveni akt in registracijski podatki ZZT.',about),
 'raziskave-in-razvoj':('Raziskave in razvoj','Raziskovalna področja, metode in okoljski pilotni projekti ZZT.',research),
 'izobrazevanje-in-mladi':('Izobraževanje in mladi','Programi učenja, mladinskega dela in digitalnih kompetenc v ZZT.',education),
 'projekti':('Raziskovalne smeri','Delovne hipoteze, strokovne smeri in predvidene raziskovalne metode ZZT.',projects),
 'ekipa-in-izkusnje':('Ekipa in izkušnje','Ustanovitelj ZZT in dokumentirane osebne reference v evropskih in mladinskih projektih.',team),
 'sodelovanje':('Sodelovanje','Strokovno sodelovanje z raziskovalci, izobraževalnimi ustanovami in skupnostmi.',cooperation),
 'publikacije-in-objave':('Publikacije in viri','Raziskovalna literatura, dokumenti in načrtovane publikacije ZZT.',publications),
 'kontakt':('Kontakt','Projektni kontakt in sedež Zavoda za zeleno tehnologijo.',contact),
 'zasebnost':('Zasebnost','Obvestilo o zasebnosti za statično spletno izdajo ZZT.',privacy),
 'viri-fotografij':('Viri fotografij','Avtorji, fotografije in licence vizualnega gradiva spletne strani ZZT.',credits),
}

def layout(slug,title,description,content):
 hero_preload = f'<link rel="preload" as="image" imagesrcset="{HERO_SRCSET}" imagesizes="{HERO_SIZES}" fetchpriority="high">' if not slug else ''
 items=''.join(f'<a href="{url(s)}" aria-current="page">{escape(label)}</a>' if slug==s else f'<a href="{url(s)}">{escape(label)}</a>' for s,label in NAV)
 footeritems=''.join(f'<a href="{url(s)}">{escape(l)}</a>' for s,l in NAV if s!='')
 return f'''<!doctype html>
<html lang="sl"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><meta name="theme-color" content="#faf6ec"><title>{escape(title)} | ZZT – Zavod za zeleno tehnologijo</title><meta name="description" content="{escape(description,quote=True)}"><meta name="robots" content="index,follow"><link rel="canonical" href="https://zavod-zzt.eu{url(slug)}"><meta property="og:url" content="https://zavod-zzt.eu{url(slug)}"><meta property="og:type" content="website"><meta property="og:locale" content="sl_SI"><meta property="og:site_name" content="ZZT – Zavod za zeleno tehnologijo"><meta property="og:image" content="https://zavod-zzt.eu/assets/photos/b527e1baf61975f3.jpg"><meta name="twitter:card" content="summary_large_image"><meta property="og:title" content="{escape(title,quote=True)} | ZZT"><meta property="og:description" content="{escape(description,quote=True)}"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml">{hero_preload}<link rel="stylesheet" href="/assets/site.css?v={STYLE_REVISION}"><script defer src="/assets/site.js?v={SCRIPT_REVISION}"></script><script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"ZZT – Zavod za zeleno tehnologijo","legalName":"ZZT – Zavod za zeleno tehnologijo, Slavski Laz, zavod za spodbujanje mladih pri novih zelenih tehnologijah","foundingDate":"2026-09-29","url":"https://zavod-zzt.eu/","email":"{EMAIL}","founder":{{"@type":"Person","name":"Dan Fredi Grmuša"}},"address":{{"@type":"PostalAddress","addressLocality":"Kostel","addressCountry":"SI"}}}}</script></head>
<body><a class="skip-link" href="#main">Preskoči na vsebino</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="/" aria-label="ZZT – Domov"><span class="brand-name"><strong>ZZT</strong><small>Zavod za zeleno tehnologijo</small></span></a><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="main-nav" aria-label="Odpri navigacijo"><span></span><span></span></button><nav class="main-nav" id="main-nav" aria-label="Glavna navigacija">{items}</nav></div></header>
<main id="main" tabindex="-1">{content}</main><footer class="site-footer"><div class="wrap footer-top"><div><p class="footer-brand">ZZT</p><p>Zavod za zeleno tehnologijo<br>Kostel · Slovenija</p></div><nav aria-label="Navigacija v nogi">{footeritems}</nav><div><p class="footer-kicker">Ustanovitelj in kontakt</p><strong class="footer-person">Dan Fredi Grmuša</strong><a href="mailto:{EMAIL}">{EMAIL} ↗</a><p>Raziskovanje · izobraževanje · sodelovanje</p></div></div><div class="wrap footer-bottom"><span>© 2026 ZZT – Zavod za zeleno tehnologijo</span><span><a href="/zasebnost/">Zasebnost</a> · <a href="/viri-fotografij/">Viri fotografij</a></span><span>Kostel · Slovenija</span></div></footer></body></html>'''

for slug,(title,desc,fn) in PAGES.items():
 dest=OUT/slug/'index.html' if slug else OUT/'index.html'
 dest.parent.mkdir(parents=True,exist_ok=True)
 dest.write_text(layout(slug,title,desc,fn()),encoding='utf-8')
# Keep machine-readable content model for verification/future CMS migration.
(OUT/'assets'/'research-areas.json').write_text(json.dumps([{k:v for k,v in a.items() if k!='photo'} for a in AREAS],ensure_ascii=False,indent=2),encoding='utf-8')
legacy_data=OUT/'assets'/'projects.json'
if legacy_data.exists(): legacy_data.unlink()
from shutil import rmtree
for old_slug in ('obala-v-podatkih','mladi-za-pregledne-odlocitve','graditeljska-dediscina-kostela'):
 old_dir=OUT/'projekti'/old_slug
 if old_dir.is_dir(): rmtree(old_dir)
(OUT/'robots.txt').write_text('User-agent: *\nAllow: /\nSitemap: https://zavod-zzt.eu/sitemap.xml\n',encoding='utf-8')
(OUT/'CNAME').write_text('zavod-zzt.eu\n',encoding='utf-8')
(OUT/'.nojekyll').touch()
(OUT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join('<url><loc>https://zavod-zzt.eu'+url(slug)+'</loc></url>\n' for slug in PAGES) + '</urlset>\n',encoding='utf-8')
(OUT/'404.html').write_text(layout('404','Strani ni mogoče najti','Stran ni na voljo.',f'<section class="section"><div class="wrap"><h1>Strani ni mogoče najti.</h1><p>Naslov ni pravilen ali pa je bila vsebina premaknjena.</p>{link("","Nazaj na naslovnico","btn primary")}</div></section>'),encoding='utf-8')
print('Created',len(PAGES),'pages at',OUT)
