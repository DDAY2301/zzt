# Preverjanje spletne strani ZZT

Poročila preverjanj so na voljo kot dnevnik vsakega zagona GitHub Actions. Ta dokument opisuje **meje** izvedenega pregleda, ne ocene izvora vsebine.

- `src/qa_static.py`: 14 strani, notranje povezave, opisi, naslovi, kanonični URL, trije fotografski viri Kolpe, XML sitemap in robots.txt.
- `src/qa_e2e.py`: Chromium, namizni/tablični/mobilni prelom, vidne in naložene fotografije, navigacija, 14 lokalnih poti, klik `mailto:`, osnovni JavaScript napaki in HTTP 200 za produkcijsko naslovnico.
- `.github/workflows/pages.yml`: ponovno generiranje izvorne kode, preverjanja, objava in sinhronizacija dejanskih HTML/fotografij v GitHub.

Testi ne dokazujejo prejema elektronskih sporočil (stran uporablja `mailto:`), izvedenih okoljskih meritev, odobritve razpisov ali popolne skladnosti z WCAG 2.2 AA. Fotografije so resnični prikazi lokacij, ne dokumenti terenskega izvajanja ZZT.
