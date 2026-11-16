# ZZT – tehnično poročilo o preverjanju

**Datum:** 16. november 2026  
**Obseg:** statično generirana večstranska stran z 14 HTML dokumenti, delujočim lokalnim spletnim strežnikom, CSS/JS, tremi projektnimi stranmi.

## Preverjeno

- E1: pregledan izvorni ZIP z 8 veščinami, ustanovitveni akt, registracijske informacije in osebne projektne reference.
- E1: pregledan povezan GitHub, brez zaznanega repozitorija ZZT; nepovezani repozitoriji so ostali nespremenjeni.
- E2: skript za gradnjo ustvari 14 HTML strani.
- E2: lokalni strežnik je za `/projekti/` vrnil HTTP 200. Za vse generirane HTML strani je statični pregled potrdil obstoj glavnega naslova, metapodatkov in vseh notranjih povezav.
- E2: skript za izolirane Chromium DOM preizkuse uspešno upodobi 14 HTML strani.
- E2: v Chromium pri 1440, 820 in 390 px ni bil zaznan horizontalni overflow na naslovnici.
- E2: na mobilnem prikazu je gumb navigacije odprl meni; tipka Escape ga je zaprla; preverjen je `aria-expanded`.
- E2: kontaktni `mailto:` povezava obstaja in vodi v e-poštni odjemalec, ne neposredno pošiljanje.

## Ni bilo preverjeno

- E3: resnično omrežno prehajanje med stranmi v Chromium — brskalnik je vrnil `ERR_BLOCKED_BY_ADMINISTRATOR` tudi za lokalne HTTP in `file:` URL-je; zato smo uporabili izoliran DOM preizkus. Statični notranji URL-ji pa obstajajo.
- E3: prikaz oddaljenih fotografij na produkcijski domeni; dostop do zunanjih slik v testnem okolju ni deloval.
- E3: poln pregled z Lighthouse, axe-core in ročno WCAG 2.2 AA revizijo.
- E4: dejansko pošiljanje e-pošte, povezan zunanji backend, produkcijski strežnik, DNS, CDN, varnostne glave v realnem HTTP odzivu.
- E4: pristna domena in javna dostopnost; uporabnik še ni potrdil produkcijske domene in povezave z gostovanjem.

## Pred objavo

1. Preveriti pristnost in prikaz vseh 4 fotografij na ciljnem gostovanju.
2. Potrditi javno kontaktno e-pošto in morebitno ločeno institucionalno identiteto.
3. Izbrati domeno/gostovanje; po izbiri dodati `canonical`, `sitemap.xml`, `og:url` in preveriti SEO.
4. Potrditi veljavno besedilo o zasebnosti za dejanskega ponudnika in vse njegove dnevnike oziroma piškotke.
5. Opraviti resnične mobilne/desktop klikovne teste, strojne in ročne teste dostopnosti ter preveriti dejansko dostavo e-pošte, če bo dodan kontaktni obrazec.
6. Pred spreminjanjem projekta v GitHub ustvariti ustrezno repozitorijsko strukturo ali jasno potrditi izbrani repozitorij in način dostave.

**Končna stopnja pripravljenosti:** E2 za lokalno kodo/izolirane teste; E3 in E4 še nista doseženi. Stran ni v produkciji in ne trdimo, da je operativno objavljena.
