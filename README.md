# ZZT – Zavod za zeleno tehnologijo

**Spletna stran:** https://zavod-zzt.eu/  
**Izvorna koda:** https://github.com/DDAY2301/zzt  
**Kontakt:** Dan Fredi Grmuša, ustanovitelj – [dan.grmusa@gmail.com](mailto:dan.grmusa@gmail.com)

Spletna stran zasebnega nepridobitnega zavoda s sedežem v Kostelu. Poudarek je na okoljskih raziskavah, zelenih tehnologijah, izobraževanju mladih ter dokumentiranih projektnih zasnovah. Osebne reference ustanovitelja so ločene od institucionalnega delovanja.

## Struktura

| Mapa | Vloga |
|---|---|
| `site/` | **Dejanska javna stran:** vse HTML datoteke, CSS, JavaScript, favicon, fotografije, sitemap in CNAME |
| `site/assets/site.css` | Oblika za namizne, tablične in mobilne zaslone |
| `site/assets/site.js` | Dostopna mobilna navigacija in obravnava napak fotografij |
| `src/build_site.py` | Enoten vir besedil in strukture za 14 strani |
| `src/cache_photos.py` | Prenos dovoljenih resničnih fotografij Wikimedia Commons, z ohranjenim avtorstvom |
| `src/qa_static.py`, `src/qa_e2e.py` | Preverjanje povezav, vsebine, mobilnega prikaza, fotografij in navigacije |
| `.github/workflows/` | Samodejna priprava, preverjanje in objava GitHub Pages |
| `docs/` | Viri dejanskih trditev, licence fotografij in pregled kakovosti |

## Kako spremeniti spletno stran

Za besedila, strani, projektne statuse in navedbe urejajte `src/build_site.py`. Za videz urejajte `site/assets/site.css`; za interakcije `site/assets/site.js`.

Spremembe na veji `main` sprožijo GitHub Actions. Pred objavo se znova ustvarijo HTML strani, pripravijo lokalne kopije licenciranih fotografij ter preverijo povezave in sintaksa. **Ustvarjene datoteke se samodejno shranijo tudi nazaj v repozitorij**, tako da sta javna stran in vsebina `site/` usklajeni.

## Lokalni zagon

Potrebujete Python 3.11+; ni potrebnih Node odvisnosti za delovanje strani.

```bash
python src/build_site.py
python -m http.server 8765 --directory site
```

Odprite http://127.0.0.1:8765/. Za lokalne fotografije zaženite tudi `python src/cache_photos.py`, ko imate omrežni dostop.

## Kakovost, zasebnost in viri

- 14 dejanskih strani (vključno s tremi projektnimi profili), navigacija, odzivnost in SEO.
- Javne registracije in projektne navedbe temeljijo na predloženih dokumentih. Projekti v pripravi **niso** prikazani kot odobreni.
- Fotografije Kolpe in drugih lokacij so iz Wikimedia Commons; avtorstva ter licence so vidne na strani in evidentirane v [fotografskem registru](docs/Fotografije%20in%20licence.md).
- [Register virov](docs/Viri%20in%20dokazila.md) pojasnjuje podlago za javne trditve.
- Kontakt je povezava `mailto:`; neposredni strežniški kontaktni obrazec ni nameščen. Ne trdimo, da je pošiljanje e-pošte avtomatsko.
- [Pregled preverjanja](docs/Preverjanje%20spletne%20strani.md) in rezultati testov v zavihku **Actions**.

## Pravna opozorila

Vse pravice do fotografij ostanejo pri njihovih avtorjih. Datoteke s pogoji CC BY-SA se uporabljajo z navedbo vira in licence. Stran ni predstavitev zaključenih, financiranih projektov, če so navedeni šele kot projektne zasnove.
