# Hautaustoimisto Mielonen — Redesign-ehdotukset

## Graafinen ohjeisto 2023 — Keskeiset havainnot

| Elementti | Virallinen arvo | Nykyinen sivusto |
|-----------|----------------|-----------------|
| Purppura | `#3d0042` | `#3d0043` (1 off) |
| Naava | `#d1e0d7` | `#d1e0d7` ✅ |
| Pellava | `#f2f2eb` | `#f2f2eb` ✅ |
| Musta | `#241f21` | `#000000` ❌ |
| Otsikkofontti | PP Right Didone | PP Right Didone ✅ |
| Leipäfontti | Source Sans Pro | Source Sans Pro ✅ |
| Kuvakehys | Ovaali + ohut reunaviiva | Ovaali + border ✅ |
| Kuvitukset | Piia Huttusen viivapiirroskuvitukset | Lintu käytössä ✅ |

**Tärkeimmät puutteet sivustolla:**
- Puhelinnumero ei näy navigaatiossa / headerissa
- Navigaatio häviää kun scrollaa (ei sticky)
- Sivustolla on harvinainen split-navigaatio (logo keskellä) — epätavallinen UX



Kaksi erillistä redesign-versiota hautaustoimistomielonen.fi-sivustolle.

## Kehitysserveri
```bash
cd /home/node/.openclaw/workspace/mielonen-redesign
python3 -m http.server 8099
```
- **Versio 1:** http://localhost:8099/versio1/
- **Versio 2:** http://localhost:8099/versio2/

---

## Versio 1: "Lämmin & Moderni" ✅ Brändin mukainen

**Konsepti:** 100% graafisen ohjeiston mukainen toteutus. Pitää Mielosen brändin mutta parantaa käytettävyyttä ja rakennetta merkittävästi.

**Brändinmukaisuus:**
- ✅ Värit: #3d0042 purppura, #d1e0d7 naava, #f2f2eb pellava, #241f21 musta (lämmin)
- ✅ Fontit: PP Right Didone (otsikot) + Source Sans Pro (leipäteksti)
- ✅ Kuvakehys: ovaali + ohut purppurareunalinja
- ✅ Piia Huttusen linnun kuvitus hero-osiossa
- ✅ Vasemmalle tasattu asettelu
- ✅ Äänensävy: selkeä, rauhallinen, empaattinen

**Parannukset nykyiseen:**
- **Top bar** — puhelinnumero ja sähköposti heti näkyvissä sivun yläreunassa
- **Sticky header** — navigaatio seuraa mukana scrollatessa (nykyinen häviää)
- **Selkeä navigaatio** — kaikki linkit yhdessä rivissä, ei split-logiikkaa
- **Hero full-width** — lintuillustration oikealla, teksti vasemmalla; taustaelementtinä havut
- **Palvelut-palkki** — 4 palvelukategoriaa kirkkaalla violetilla heti hero-osion alla
- **Parempi CTA** — "Soita nyt" fixattuna alakulmaan
- **Arvostelukortteja** — siistit kortit beige-taustalla sidebar-tyylisen liukurin sijaan
- **Footer** — 4-kolumnirakenne, selkeämmät tiedot

**Väripaletti:** #3d0042 + #d1e0d7 + #f2f2eb + #241f21
**Fontit:** PP Right Didone + Source Sans Pro (virallinen kombinaatio)

---

## Versio 2: "Klassinen & Arvokas" ⚠️ Konseptivaihtoehto (poikkeaa brändistä)

**Konsepti:** Täysin uusi värimaailma — tumma laivastonsininen (#1a2744) + kulta (#c9a96e) + kerma. Inspiraationa espoonhautaustoimisto.fi ja kuopionhautaustoimisto.fi. **Ei vastaa nykyistä graafista ohjeistusta** — tämä on vaihtoehtoinen suunta jos brändiä halutaan uudistaa.

**Rakenne:**
- **Top bar** — musta palkki: sijainnit + puhelin + sähköposti
- **Header** — laivastonsininen, logo + nimi + tagline, kulta-CTA-nappi
- **Hero full-width** — tumma sininen tausta, suuri serif-otsikko kursivoinnilla, luottamusmittarit alhaalla (80v / 24/7 / 4 toimipistettä)
- **Kultalinja** — koristeellinen kultaraiviitus hero:n alapuolella
- **Quote banner** — sitaatti-osio yrityksen motosta
- **Service cards** — 4 korttia hover-animaatiolla, kultaraja aktivoituessa
- **About-osio** — tumma sininen tausta, valokuva kultavarjolla + vuosilukubadge, statistiikka-ruudukko
- **Planning steps** — puhdas listanäkymä numeroineen, ei ympyröitä
- **Reviews** — 4-kolumni tähtiarvostelut valkoisilla korteilla
- **Contact** — split: vasemmalla tietolaatikot, oikealla tiimikortit + CTA-napit
- **Footer** — tumma, 4-kolumni

**Väripaletti:** #1a2744 navy + #c9a96e kulta + #faf8f3 kerma + #1c1c1c charcoal
**Fontit:** Playfair Display (otsikot) + Inter (leipäteksti)

---

## Suositukset jatkokehitykseen

1. **WordPress-teeman kehitys** näiden mockup-versioiden pohjalta
2. **Google Fonts** voidaan korvata Mielosella jo olevilla kirjasinpareilla (PP Right Didone → Playfair Display on läheisin)
3. **Kuvamateriaalin päivitys** — hero-kuvana voisi olla tunnelmallinen maisemakuva linnun sijaan
4. **Puhelinnumero header-otsikossa** on kriittinen muutos — tällä hetkellä se löytyy vain sivun alareunasta
5. **Versio 2:n** kulta-teema erottuu hautausalan kilpailijoista positiivisesti

## Tiedostot
```
mielonen-redesign/
├── versio1/index.html    — Lämmin & Moderni
├── versio2/index.html    — Klassinen & Arvokas  
└── assets/               — Ladattu kuva-aineisto mielonen.fi:stä
    ├── bird.png
    ├── portrait.jpg (+ p1,p2,p3.jpg)
    ├── havut.png
    ├── joutsenet.png
    └── logo-purple/white.svg
```
