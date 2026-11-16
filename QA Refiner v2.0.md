# ZZT – revizija Authenticity & Engineering Quality v2.0

**Datum:** 16. november 2026  
**Izhodišče:** arhiv »ZZT Spletna stran celoten projekt.zip«, lokalno izdana statična spletna stran, brez dostopa do produkcijskega repozitorija ZZT.  
**Obseg:** naslovnica, generator vseh 14 vsebinskih strani, nav, zunanje fotografije, integracija veščine. Originalna izdaja ostane nespremenjena.

## Ugotovitve in popravki

| ID | Stopnja | Ugotovitev | Dejanska sprememba | Preverjanje |
|---|---|---|---|---|
| Q-01 | P1 | Ob nedosegljivi oddaljeni fotografiji je ostal prazen/broken element | Dostopno rezervno besedilo in CSS stanje `is-unavailable`; ostane avtorstvo in izvirnik | Izolirani Chromium: sprožena `error` na sliki, fallback viden, kredit ohranjen |
| Q-02 | P2 | Deli naslovnice so imeli generičen opis in niso dovolj razločevali ciljev ZZT od dosedanjih rezultatov | Natančnejši opis zasebnega zavoda, projektnih priprav in osebnih referenc ustanovitelja | Ponovno generirana naslovnica, ročni pregled besedila |
| Q-03 | P2 | Povezave v namizni navigaciji so bile zelo drobne (`0.7rem`) | Povečane na `0.78rem` | Chromium širin 1200–1440 brez prekrivanja in prelivanja |
| Q-04 | P3 | Pomožna projektna veščina ni bila prisotna v zadnji izdaji | Originalna veščina dodana v `.agents/skills/` brez sprememb ali odstranitve licenc | Validator paketa: PASS |

## Dejanski testni rezultati

- Strukturni pregled veščine: PASS.
- Python generator: PASS; obnovljenih 14 vsebinskih HTML strani, plus `404.html` (skupaj 15 HTML datotek).
- Python syntax in JS `node --check`: PASS.
- Read-only `review_signals.py`: 28 pregledanih datotek, 0 očitnih placeholder/dummy-link signalov; to **ni** detektor AI-avtorstva.
- Notranji statični URL, `h1`, `img alt`: 15 HTML datotek, 0 najdenih napak.
- Izolirani Chromium DOM: naslovnica 390, 820, 1440 px brez horizontalnega prelivanja; mobilni meni se odpre, zapre s `Escape`; na vseh 14 straneh je en `h1`.
- Dodatno preverjanje 390, 820, 1180, 1200, 1280, 1366, 1440 px: brez horizontalnega prelivanja; pri širših pogledih ni prekrivanja nav in logotipa.
- Simulirana napaka slikanega vira: PASS, besedilo fallback in avtorstvo ostaneta vidna.
- Lokalni HTTP pregled v tem testnem okolju: **NEPREVERJENO**; zahteva je bila zavrnjena z `ConnectionRefusedError` pri 127.0.0.1:8767. Ne trdimo, da so klikovne omrežne poti preverjene.

## Odprte naloge

1. E3: preizkus dejanskih klikov po objavi na izbrano domeno; produkcijskega gostovanja ni.
2. E3: preverjanje izvirnih zunanjih fotografij na produkciji in vseh pogojev uporabe; rezervni prikaz ni nadomestek za pravo fotografijo.
3. E3/E4: neodvisen WCAG 2.2 AA in Lighthouse preizkus.
4. E4: kontakt uporablja `mailto:`, dostava ni potrjena in ni neposrednega zalednega pošiljanja.
5. E4: veljavni produkcijski DNS, canonical URL, pravilnik o zasebnosti po dejanskem gostovanju, zakonita kontaktna identiteta in dovoljenja za objavo osebnih referenc.

**Dosežena stopnja:** E2 (lokalna izvedba in izolirano DOM preverjanje), ne E3/E4 in ne produkcijsko dokončanje.  
**Predpisani provenienčni podatki in fotografski krediti ostanejo nespremenjeni.**
