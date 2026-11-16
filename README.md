# ZZT – Zavod za zeleno tehnologijo | Spletna izdaja 1.0

**Datum izdelave:** 16. november 2026  
**Namen:** uredniško zasnovana, večstranska statična spletna stran za javno predstavitev registriranega zasebnega zavoda.  
**Status:** lokalna izvedba z izvedenimi statičnimi in izoliranimi brskalniškimi preverjanji; **ni bila nameščena na produkcijsko domeno**.

## 1. Zagon (Windows)

1. Razširite vsebino ZIP v poljubno mapo.
2. Dvokliknite `START PREVIEW.bat` (zahtevan Python in ukaz `py`).
3. Odprite `http://127.0.0.1:8765/`, če se brskalnik ne odpre samodejno.
4. Zaustavite strežnik z `Ctrl+C` v konzoli.

Alternativa:

```powershell
cd "pot-do-mape\ZZT Spletna stran"
py -m http.server 8765 --directory site
```

Za namestitev na statično gostovanje objavite **celotno mapo `site/` v korenu domene**, saj poti uporabljajo začetni `/` (npr. `/projekti/`). Na voljo je tudi osnovni `netlify.toml` za Netlify. Strežnik in vsebina ne zahtevata npm, podatkovne baze ali API ključa.

## 2. Zgradba

- `site/` – vse HTML strani, CSS, JS, favicon, JSON projektov, robots.txt.
- `src/build_site.py` – vir za ustvarjanje 14 HTML strani (brez odvisnosti).
- `src/qa_browser.py` – Playwright izolirani DOM/test navigacijskega menija.
- `NETLIFY`: `netlify.toml` – primer konfiguracije za statično objavo in varnostne glave.
- `Viri in dokazila.md` – povezava med javnimi trditvami, dokumenti in stanjem dokazil.
- `Fotografije in licence.md` – evidenca fotografij in njihovih pogojev.
- `QA poročilo.md` – pošteno poročilo, kaj je dejansko izmerjeno.

Za ponovno generiranje po spremembi vsebine v Pythonu:

```powershell
py "src\build_site.py"
```

**Opomba:** `site/assets/site.css`, `site/assets/site.js` in `site/assets/favicon.svg` so ročno vzdrževani; generator jih ne prepiše.

## 3. Strani

Naslovnica, O zavodu, Raziskave in razvoj, Izobraževanje in mladi, Projekti, trije projektni profili, Ekipa in izkušnje, Sodelovanje, Publikacije in objave, Kontakt, Zasebnost in Viri fotografij (skupaj 14 HTML strani).

## 4. Preverjanje pred objavo

- Povezave do fotografij Wikimedia Commons so **zunanje**; v izoliranem testnem brskalniku niso bile dosegljive. Preverite, da se res prikažejo na ciljnem gostovanju, in ohranite podatke o avtorjih/licencah. Ničesar ne predstavljajte kot fotografijo izvedenih projektov ZZT.
- Kontakt uporablja dejanski `mailto:` naslov projektne kontaktne osebe iz predloženih podatkov, ne pa spletnega kontaktnega obrazca. **Ni potrjenega neposrednega pošiljanja.** Za direct-send bi morali povezati avtoriziran backend ter preveriti dejansko dostavo.
- Potrebujemo končno produkcijsko domeno za kanonične URL, sitemap.xml, og:url, morebitne preusmeritve in nadzorovalna orodja.
- Po izbiri gostovanja prilagodite obvestilo o zasebnosti dejanskim obdelavam podatkov in ponudniku.
- Za projektne statuse vzdržujte evidenco sprememb. Projekti v pripravi niso odobreni ali dokončani.
- Preverite vsak javni osebni podatek, reference in soglasja zunanjih strokovnjakov pred prodno objavo.

## 5. Kaj ni bilo narejeno

Ni bilo: dostopa do obstoječega ZZT repozitorija; povezave z živo domeno; produkcijske postavitve; potrditve dostave e-pošte; celovitega zunanjega pregleda WCAG 2.2 AA; meritev Lighthouse / Core Web Vitals; resničnega klikovnega end-to-end testa na spletni domeni. Te točke se ne smejo šteti kot zaključene.


## GitHub Pages (2026)

Ob spremembah v `src/` ali `site/` GitHub Actions ponovno generira vse strani z `python3 src/build_site.py`, preveri osnovne datoteke, nato objavi `site/`. Izbrane fotografije Kolpe so resnične fotografije Wikimedia Commons (CC0 / public domain), z navedbo virov. Za predogled je možen lokalni Python strežnik.
