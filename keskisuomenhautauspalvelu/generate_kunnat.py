#!/usr/bin/env python3
"""Generoi kuntasivut Keski-Suomen Hautauspalvelulle."""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "kaupungit")
os.makedirs(OUTPUT_DIR, exist_ok=True)

KUNNAT = [
    {"nimi": "Jyväskylä", "slug": "jyvaskyla", "matka_km": 0,
     "kuvaus": "Keski-Suomen maakuntakeskus ja palvelumme kotipaikka.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Toimipisteemme sijaitsee Jyväskylässä.",
     "lahikunnat": ["Muurame", "Laukaa", "Jämsä", "Hankasalmi", "Uurainen", "Toivakka"]},
    {"nimi": "Jämsä", "slug": "jamsa", "matka_km": 70,
     "kuvaus": "Jämsä on teollisuuskaupunki Keski-Suomen eteläosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Jämsästä palvelu hoituu Jyväskylän krematorion kautta.",
     "lahikunnat": ["Jyväskylä", "Keuruu", "Multia", "Toivakka", "Joutsa"]},
    {"nimi": "Keuruu", "slug": "keuruu", "matka_km": 75,
     "kuvaus": "Keuruu on järvirikas kaupunki Keski-Suomen länsiosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Keuruulta nouto järjestyy — kuljetus Jyväskylän krematoriolle.",
     "lahikunnat": ["Jyväskylä", "Jämsä", "Multia", "Muurame", "Petäjävesi"]},
    {"nimi": "Äänekoski", "slug": "aanekoski", "matka_km": 45,
     "kuvaus": "Äänekoski on metsäteollisuuskaupunki Keski-Suomen pohjoisosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Äänekoskelta nouto Jyväskylän krematoriolle — ei kuljetuslisää.",
     "lahikunnat": ["Jyväskylä", "Saarijärvi", "Uurainen", "Konnevesi", "Laukaa"]},
    {"nimi": "Saarijärvi", "slug": "saarijärvi", "matka_km": 78,
     "kuvaus": "Saarijärvi on vireä kaupunki Keski-Suomen luoteisosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Saarijärveltä palvelu hoituu verkon ja puhelimen välityksellä.",
     "lahikunnat": ["Äänekoski", "Karstula", "Uurainen", "Kannonkoski", "Kyyjärvi"]},
    {"nimi": "Viitasaari", "slug": "viitasaari", "matka_km": 105,
     "kuvaus": "Viitasaari on musiikistaan tunnettu kaupunki pohjois-Keski-Suomessa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Viitasaarelta kuljetuslisä kerrotaan etukäteen.",
     "lahikunnat": ["Pihtipudas", "Äänekoski", "Konnevesi", "Kinnula", "Saarijärvi"]},
    {"nimi": "Laukaa", "slug": "laukaa", "matka_km": 22,
     "kuvaus": "Laukaa on Jyväskylän naapurikunta aivan maakuntakeskuksen tuntumassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Laukaalta matka krematoriolle on lyhyt — palvelu nopeaa.",
     "lahikunnat": ["Jyväskylä", "Äänekoski", "Hankasalmi", "Konnevesi", "Uurainen"]},
    {"nimi": "Muurame", "slug": "muurame", "matka_km": 18,
     "kuvaus": "Muurame on kasvava naapurikunta Jyväskylän eteläpuolella.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Muuramesta Jyväskylään on vain muutama kilometri.",
     "lahikunnat": ["Jyväskylä", "Jämsä", "Keuruu", "Laukaa", "Toivakka"]},
    {"nimi": "Hankasalmi", "slug": "hankasalmi", "matka_km": 55,
     "kuvaus": "Hankasalmi on rautatien varrella sijaitseva maaseutukunta.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Hankasalmelta nouto — ei kuljetuslisää.",
     "lahikunnat": ["Jyväskylä", "Laukaa", "Konnevesi", "Uurainen", "Äänekoski"]},
    {"nimi": "Joutsa", "slug": "joutsa", "matka_km": 80,
     "kuvaus": "Joutsa on rauhallinen maaseutukunta Keski-Suomen eteläreunalla.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Joutsasta palvelu hoituu etänä — saavumme noutamaan.",
     "lahikunnat": ["Jyväskylä", "Jämsä", "Toivakka", "Luhanka", "Muurame"]},
    {"nimi": "Karstula", "slug": "karstula", "matka_km": 105,
     "kuvaus": "Karstula on luonnonläheinen kunta Keski-Suomen luoteisosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Karstulan pitkähköstä matkasta kuljetuslisä kerrotaan etukäteen.",
     "lahikunnat": ["Saarijärvi", "Kyyjärvi", "Äänekoski", "Kannonkoski", "Kivijärvi"]},
    {"nimi": "Kinnula", "slug": "kinnula", "matka_km": 145,
     "kuvaus": "Kinnula on pieni kunta Keski-Suomen pohjoisimmassa kolkassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Kinnulan pitkästä matkasta kuljetuslisä kerrotaan tarkasti etukäteen.",
     "lahikunnat": ["Viitasaari", "Pihtipudas", "Kivijärvi", "Kannonkoski"]},
    {"nimi": "Konnevesi", "slug": "konnevesi", "matka_km": 65,
     "kuvaus": "Konnevesi on järvimaisemistaan tunnettu kunta Keski-Suomessa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Konnevedeltä nouto — ei kuljetuslisää.",
     "lahikunnat": ["Jyväskylä", "Äänekoski", "Laukaa", "Hankasalmi", "Viitasaari"]},
    {"nimi": "Multia", "slug": "multia", "matka_km": 88,
     "kuvaus": "Multia on metsäinen maaseutukunta Keski-Suomen länsiosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Multialta palvelu hoituu etänä — saavumme noutamaan.",
     "lahikunnat": ["Keuruu", "Jämsä", "Petäjävesi", "Muurame"]},
    {"nimi": "Petäjävesi", "slug": "petajavesi", "matka_km": 42,
     "kuvaus": "Petäjävesi on Unescon maailmanperintökohteestaan tunnettu kunta.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Petäjävedeltä nouto — ei kuljetuslisää.",
     "lahikunnat": ["Jyväskylä", "Keuruu", "Multia", "Muurame", "Uurainen"]},
    {"nimi": "Pihtipudas", "slug": "pihtipudas", "matka_km": 128,
     "kuvaus": "Pihtipudas on Keski-Suomen pohjoisin kunta.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Pihtipudaksen pitkästä matkasta kuljetuslisä kerrotaan etukäteen.",
     "lahikunnat": ["Viitasaari", "Kinnula", "Äänekoski", "Karstula"]},
    {"nimi": "Toivakka", "slug": "toivakka", "matka_km": 38,
     "kuvaus": "Toivakka on rauhallinen maaseutukunta Jyväskylän eteläpuolella.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Toivakasta nouto — ei kuljetuslisää.",
     "lahikunnat": ["Jyväskylä", "Jämsä", "Muurame", "Joutsa", "Luhanka"]},
    {"nimi": "Uurainen", "slug": "uurainen", "matka_km": 35,
     "kuvaus": "Uurainen on kasvava naapurikunta Jyväskylän pohjoispuolella.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Uuraisista nouto — ei kuljetuslisää.",
     "lahikunnat": ["Jyväskylä", "Äänekoski", "Saarijärvi", "Laukaa", "Hankasalmi"]},
    {"nimi": "Kannonkoski", "slug": "kannonkoski", "matka_km": 115,
     "kuvaus": "Kannonkoski on pieni, luonnonläheinen kunta pohjois-Keski-Suomessa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Kannonkoskelta kuljetuslisä kerrotaan etukäteen.",
     "lahikunnat": ["Saarijärvi", "Viitasaari", "Karstula", "Kinnula", "Kivijärvi"]},
    {"nimi": "Kivijärvi", "slug": "kivijärvi", "matka_km": 128,
     "kuvaus": "Kivijärvi on pieni kunta Keski-Suomen luoteisosassa.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Kivijärveltä kuljetuslisä kerrotaan etukäteen.",
     "lahikunnat": ["Karstula", "Kinnula", "Kannonkoski", "Kyyjärvi"]},
    {"nimi": "Kyyjärvi", "slug": "kyyjärvi", "matka_km": 120,
     "kuvaus": "Kyyjärvi on pieni kunta aivan Keski-Suomen länsireunalla.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Kyyjärveltä kuljetuslisä kerrotaan etukäteen.",
     "lahikunnat": ["Karstula", "Saarijärvi", "Äänekoski", "Kivijärvi"]},
    {"nimi": "Luhanka", "slug": "luhanka", "matka_km": 92,
     "kuvaus": "Luhanka on Keski-Suomen pienin kunta Päijänteen rannalla.",
     "krematorio": "Jyväskylän krematorio", "lisatieto": "Luhangasta palvelu hoituu etänä — saavumme noutamaan.",
     "lahikunnat": ["Joutsa", "Toivakka", "Jämsä", "Muurame"]},
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="fi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Hautauspalvelu {nimi} — Keski-Suomen Hautauspalvelu</title>
<meta name="description" content="Arvokas hautauspalvelu {nimissa}. Keski-Suomen Hautauspalvelu palvelee {nimen} asukkaita verkon ja puhelimen välityksellä. Kivijalka Jyväskylässä.">
<link rel="canonical" href="https://keskisuomenhautauspalvelu.fi/hautauspalvelu-{slug}/">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--cream:#f7f8fa;--white:#fff;--navy:#1e3a5c;--navy-l:#2a5080;--navy-xl:#e8eef5;--dark:#151e2b;--text:#242d3a;--text-m:#5a6b80;--border:#d8dde6;--border-l:#e8edf4}}
html{{scroll-behavior:smooth;background:var(--cream)}}
body{{font-family:'Inter',sans-serif;color:var(--text);background:var(--cream);line-height:1.6;overflow-x:hidden}}
.nav{{background:rgba(247,248,250,.96);border-bottom:1px solid var(--border);padding:0 40px;height:64px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;backdrop-filter:blur(8px)}}
.nav-logo{{font-family:'Cormorant Garamond',serif;font-size:17px;font-weight:500;color:var(--dark);text-decoration:none}}
.nav-logo span{{font-size:10px;font-weight:500;letter-spacing:.16em;text-transform:uppercase;color:#8a9bb0;display:block;margin-top:1px}}
.nav-phone{{font-size:13px;font-weight:600;color:var(--navy);text-decoration:none;border:1px solid var(--navy);border-radius:4px;padding:7px 16px}}
.hero{{background:var(--dark);padding:80px 40px;position:relative;overflow:hidden}}
.hero-tint{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(30,58,92,.25) 0%,transparent 60%);pointer-events:none}}
.hero-inner{{max-width:900px;margin:0 auto;position:relative}}
.hero-eyebrow{{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:rgba(160,190,220,.7);margin-bottom:16px}}
.hero-h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,64px);font-weight:300;color:#f0f4f8;line-height:1.08;margin-bottom:20px}}
.hero-h1 em{{font-style:italic;color:#a0bedc}}
.hero-p{{font-size:16px;font-weight:300;color:rgba(240,244,248,.5);line-height:1.9;max-width:540px;margin-bottom:36px}}
.hero-btns{{display:flex;gap:12px;flex-wrap:wrap}}
.btn-n{{display:inline-flex;align-items:center;gap:8px;background:var(--navy);color:#fff;font-size:13px;font-weight:500;padding:13px 24px;border-radius:3px;text-decoration:none}}
.btn-o{{display:inline-flex;align-items:center;gap:8px;background:transparent;border:1px solid rgba(240,244,248,.2);color:rgba(240,244,248,.6);font-size:13px;font-weight:500;padding:13px 24px;border-radius:3px;text-decoration:none}}
.price-bar{{background:var(--navy);padding:16px 40px;display:flex;justify-content:center;gap:56px;flex-wrap:wrap}}
.pb-item{{display:flex;align-items:center;gap:10px}}
.pb-item svg{{width:14px;height:14px;stroke:#a0bedc}}
.pb-text{{font-size:12px;font-weight:500;color:rgba(255,255,255,.7)}}
.content{{max-width:900px;margin:0 auto;padding:72px 40px}}
.section{{margin-bottom:60px}}
.section h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,40px);font-weight:300;color:var(--dark);margin-bottom:14px;line-height:1.1}}
.section h2 em{{font-style:italic;color:var(--navy)}}
.section-rule{{width:36px;height:1px;background:var(--navy);margin-bottom:22px}}
.section p{{font-size:14px;font-weight:300;color:var(--text-m);line-height:1.9;margin-bottom:14px}}
.price-cards{{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:32px}}
.pc{{background:var(--white);border:1px solid var(--border-l);border-radius:8px;padding:28px 22px}}
.pc.featured{{background:var(--dark);border-color:var(--dark)}}
.pc-label{{font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:#8a9bb0;margin-bottom:12px}}
.pc.featured .pc-label{{color:rgba(240,244,248,.38)}}
.pc-price{{font-family:'Cormorant Garamond',serif;font-size:42px;font-weight:300;color:var(--dark);line-height:1;margin-bottom:6px}}
.pc.featured .pc-price{{color:#f0f4f8}}
.pc-note{{font-size:11px;color:#8a9bb0;margin-bottom:18px;line-height:1.5}}
.pc.featured .pc-note{{color:rgba(240,244,248,.28)}}
.pc-list{{list-style:none}}
.pc-list li{{font-size:12px;font-weight:300;color:var(--text-m);padding:6px 0;border-top:1px solid var(--border-l);display:flex;gap:7px;align-items:flex-start;line-height:1.6}}
.pc.featured .pc-list li{{color:rgba(240,244,248,.58);border-top-color:rgba(255,255,255,.07)}}
.pc-list li::before{{content:'';width:5px;height:5px;border-radius:50%;background:var(--navy);flex-shrink:0;margin-top:5px}}
.pc.featured .pc-list li::before{{background:#a0bedc}}
.prosessi-steps{{display:flex;flex-direction:column;gap:0;margin-top:28px}}
.ps{{display:flex;gap:20px;padding-bottom:28px;position:relative}}
.ps::before{{content:'';position:absolute;left:15px;top:40px;bottom:0;width:1px;background:var(--border-l)}}
.ps:last-child::before{{display:none}}
.ps-num{{width:32px;height:32px;border-radius:50%;background:var(--navy-xl);border:1px solid var(--navy);display:flex;align-items:center;justify-content:center;flex-shrink:0;font-size:11px;font-weight:600;color:var(--navy)}}
.ps-body h4{{font-size:14px;font-weight:600;color:var(--dark);margin-bottom:4px}}
.ps-body p{{font-size:13px;font-weight:300;color:var(--text-m);line-height:1.75;margin:0}}
.lahikunnat{{display:flex;flex-wrap:wrap;gap:10px;margin-top:24px}}
.lk-tag{{background:var(--white);border:1px solid var(--border-l);border-radius:5px;padding:8px 14px;font-size:12px;font-weight:500;color:var(--text-m);text-decoration:none;transition:border-color .15s}}
.lk-tag:hover{{border-color:var(--navy);color:var(--navy)}}
.contact-box{{background:var(--white);border:1px solid var(--border-l);border-radius:10px;padding:40px}}
.contact-box h3{{font-family:'Cormorant Garamond',serif;font-size:28px;font-weight:300;color:var(--dark);margin-bottom:18px}}
.cf-field{{width:100%;background:var(--cream);border:1px solid var(--border);border-radius:4px;padding:11px 13px;font-size:13px;font-family:inherit;color:var(--text);outline:none;margin-bottom:10px}}
.cf-field:focus{{border-color:var(--navy)}}
.fld2{{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-bottom:0}}
.btn-submit{{width:100%;background:var(--navy);color:#fff;border:none;border-radius:4px;padding:13px;font-size:13px;font-weight:500;cursor:pointer;font-family:inherit;margin-top:6px}}
.breadcrumb{{font-size:12px;color:#8a9bb0;margin-bottom:20px}}
.breadcrumb a{{color:#8a9bb0;text-decoration:none}}
.breadcrumb a:hover{{color:var(--navy)}}
footer{{background:var(--dark);padding:36px 40px;text-align:center}}
.ftr-name{{font-family:'Cormorant Garamond',serif;font-size:16px;font-weight:300;color:#f0f4f8;margin-bottom:6px}}
.ftr-sub{{font-size:11px;color:rgba(240,244,248,.28)}}
@media(max-width:768px){{.nav{{padding:0 20px}}.hero{{padding:56px 20px}}.content{{padding:48px 20px}}.price-cards{{grid-template-columns:1fr}}.fld2{{grid-template-columns:1fr}}.price-bar{{gap:20px;padding:14px 20px}}footer{{padding:28px 20px}}}}
</style>
</head>
<body>

<nav class="nav">
  <a href="../" class="nav-logo">Keski-Suomen Hautauspalvelu<span>Palvelun tuottaa Jyväskylän Hautaustoimisto</span></a>
  <a href="tel:+358141234567" class="nav-phone">014 123 4567</a>
</nav>

<section class="hero">
  <div class="hero-tint"></div>
  <div class="hero-inner">
    <p class="hero-eyebrow">Hautauspalvelu {nimissa} — Keski-Suomi</p>
    <h1 class="hero-h1">Arvokas hautauspalvelu<em> {nimissa}</em></h1>
    <p class="hero-p">{kuvaus} Hoidamme vainajan noutamisen, kaikki viranomaisasiat ja krematorion tai hautauksen järjestelyt. Läpinäkyvä hinnasto, ei yllätyksiä.</p>
    <div class="hero-btns">
      <a href="#yhteys" class="btn-n">Ota yhteyttä</a>
      <a href="#hinnasto" class="btn-o">Katso hinnasto</a>
    </div>
  </div>
</section>

<div class="price-bar">
  <div class="pb-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="pb-text">Suoratuhkaus alkaen 990 €</span>
  </div>
  <div class="pb-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="pb-text">Peruspalvelu 1 490 €</span>
  </div>
  <div class="pb-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="pb-text">Tavoitettavissa 24/7</span>
  </div>
  <div class="pb-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07"/></svg>
    <span class="pb-text">Palvelu FI / EN / RU</span>
  </div>
</div>

<div class="content">
  <div class="breadcrumb">
    <a href="../">Keski-Suomen Hautauspalvelu</a> &rsaquo; Hautauspalvelu {nimissa}
  </div>

  <div class="section" id="palvelu">
    <h2>Hautauspalvelu <em>{nimissa}</em></h2>
    <div class="section-rule"></div>
    <p>{kuvaus} Palvelemme kaikkia {nimen} asukkaita verkon ja puhelimen välityksellä — kivijalkatoimistomme on Jyväskylässä, mutta vainajan nouto järjestyy koko {nimen} alueelle.</p>
    <p>{lisatieto} Lähimpänä teitä toimiva krematorio on {krematorio}{matka_teksti}.</p>
    <p>Jyväskylän Hautaustoimisto on maakunnan luotettu hautauspalvelu. Palvelemme suomeksi, englanniksi ja venäjäksi — Keski-Suomen monikulttuurinen väestö on meille tärkeä.</p>
  </div>

  <div class="section" id="hinnasto">
    <h2>Hinnasto — <em>kiinteä hinta</em></h2>
    <div class="section-rule"></div>
    <p>Kaikki hinnat sisältävät ALV:n. Krematorion maksu (300–600 €) on erillinen, julkinen maksu joka tulee näiden hintojen päälle. Se kerrotaan teille aina etukäteen.</p>
    <div class="price-cards">
      <div class="pc">
        <p class="pc-label">Suoratuhkaus</p>
        <div class="pc-price">990 €</div>
        <p class="pc-note">+ krematorion maksu 300–600 €</p>
        <ul class="pc-list">
          <li>Vainajan nouto {nimiosta}</li>
          <li>Valmistelu ja arkkuun laitto</li>
          <li>Kuljetus krematoriolle</li>
          <li>Tuhkaus</li>
          <li>Tuhkan toimitus tai hautaus</li>
          <li>Viranomaisilmoitukset</li>
        </ul>
      </div>
      <div class="pc featured">
        <p class="pc-label">Peruspalvelu</p>
        <div class="pc-price">1 490 €</div>
        <p class="pc-note">kaikki järjestelyt mukaan lukien</p>
        <ul class="pc-list">
          <li>Kaikki suoratuhkauksen sisältö</li>
          <li>Arkkuvaihtoehtojen valinta</li>
          <li>Suru-ilmoitus lehdessä</li>
          <li>Muistotilaisuuden koordinointi</li>
          <li>Viranomaisasiointi kokonaan</li>
          <li>Jatkotuki 30 vrk</li>
        </ul>
      </div>
      <div class="pc">
        <p class="pc-label">Täydellinen palvelu</p>
        <div class="pc-price">2 490 €</div>
        <p class="pc-note">kattavin kokonaisuus</p>
        <ul class="pc-list">
          <li>Kaikki peruspalvelun sisältö</li>
          <li>Kukkaset ja somistus</li>
          <li>Muistotilaisuuden järjestely</li>
          <li>Etäperunkirjoitus 595 € sis.</li>
          <li>Muistokirja omaisille</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>Näin palvelu <em>etenee</em></h2>
    <div class="section-rule"></div>
    <div class="prosessi-steps">
      <div class="ps">
        <div class="ps-num">1</div>
        <div class="ps-body">
          <h4>Yhteydenotto</h4>
          <p>Soittakaa numeroon 014 123 4567 tai täyttäkää yhteydenottolomake. Olemme tavoitettavissa ympäri vuorokauden.</p>
        </div>
      </div>
      <div class="ps">
        <div class="ps-num">2</div>
        <div class="ps-body">
          <h4>Suunnittelu yhdessä</h4>
          <p>Käymme toiveet ja käytännön järjestelyt läpi rauhassa — puhelimitse tai verkon välityksellä. Teidän ei tarvitse tulla Jyväskylään.</p>
        </div>
      </div>
      <div class="ps">
        <div class="ps-num">3</div>
        <div class="ps-body">
          <h4>Toteutus kokonaisuudessaan</h4>
          <p>Hoidamme vainajan noudosta viranomaisasioihin ja krematoriolle kuljetukseen kaiken. Teidän ei tarvitse huolehtia yksityiskohdista.</p>
        </div>
      </div>
      <div class="ps">
        <div class="ps-num">4</div>
        <div class="ps-body">
          <h4>Jälkihoito</h4>
          <p>Autamme myös jälkeen päin: muistokivet, uurnat ja etäperunkirjoitus 595 €:lla kotoa käsin hoidettuna.</p>
        </div>
      </div>
    </div>
  </div>

  <div class="section" id="yhteys">
    <h2>Ota <em>yhteyttä</em></h2>
    <div class="section-rule"></div>
    <p>Vastaamme kiireellisiin asioihin aina, ympäri vuorokauden. Tavallisiin tiedusteluihin vastaamme arkisin 2 tunnin sisällä.</p>
    <div class="contact-box">
      <h3>Yhteydenottolomake</h3>
      <div class="fld2">
        <input class="cf-field" type="text" placeholder="Etunimi">
        <input class="cf-field" type="text" placeholder="Sukunimi">
      </div>
      <input class="cf-field" type="tel" placeholder="Puhelinnumero" style="margin-top:10px">
      <input class="cf-field" type="email" placeholder="Sähköposti">
      <select class="cf-field">
        <option value="">Palvelu</option>
        <option>Suoratuhkaus (990 €)</option>
        <option>Peruspalvelu (1 490 €)</option>
        <option>Täydellinen palvelu (2 490 €)</option>
        <option>Etäperunkirjoitus (595 €)</option>
        <option>Halusin tietoa</option>
      </select>
      <textarea class="cf-field" style="height:100px;resize:vertical" placeholder="Viesti (vapaaehtoinen)"></textarea>
      <button class="btn-submit">Lähetä yhteydenotto</button>
    </div>
  </div>

  <div class="section">
    <h2>Muut Keski-Suomen <em>kunnat</em></h2>
    <div class="section-rule"></div>
    <p>Palvelemme kaikkia Keski-Suomen kuntia. Alla lähikunnat, joissa tarjoamme saman hautauspalvelun.</p>
    <div class="lahikunnat">
      {lahikunnat_html}
    </div>
  </div>
</div>

<footer>
  <div class="ftr-name">Keski-Suomen Hautauspalvelu</div>
  <div class="ftr-sub">Palvelun tuottaa Jyväskylän Hautaustoimisto &mdash; Kauppakatu 25, 40100 Jyväskylä &mdash; 014 123 4567</div>
</footer>

</body>
</html>
'''

INESSIVE = {
    'Jyväskylä': 'Jyväskylässä', 'Jämsä': 'Jämsässä', 'Keuruu': 'Keuruulla',
    'Äänekoski': 'Äänekoskella', 'Saarijärvi': 'Saarijärvellä', 'Viitasaari': 'Viitasaarella',
    'Laukaa': 'Laukaalla', 'Muurame': 'Muuramessa', 'Hankasalmi': 'Hankasalmella',
    'Joutsa': 'Joutsassa', 'Karstula': 'Karstulaassa', 'Kinnula': 'Kinnulassa',
    'Konnevesi': 'Konnevedellä', 'Multia': 'Multialla', 'Petäjävesi': 'Petäjävedellä',
    'Pihtipudas': 'Pihtiputaalla', 'Toivakka': 'Toivakassa', 'Uurainen': 'Uuraisissa',
    'Kannonkoski': 'Kannonkoskella', 'Kivijärvi': 'Kivijärvellä',
    'Kyyjärvi': 'Kyyjärvellä', 'Luhanka': 'Luhangassa',
}
ELATIVE = {
    'Jyväskylä': 'Jyväskylästä', 'Jämsä': 'Jämsästä', 'Keuruu': 'Keuruulta',
    'Äänekoski': 'Äänekoskelta', 'Saarijärvi': 'Saarijärveltä', 'Viitasaari': 'Viitasaarelta',
    'Laukaa': 'Laukaalta', 'Muurame': 'Muuramesta', 'Hankasalmi': 'Hankasalmelta',
    'Joutsa': 'Joutsasta', 'Karstula': 'Karstulaasta', 'Kinnula': 'Kinnulasta',
    'Konnevesi': 'Konnevedeltä', 'Multia': 'Multialta', 'Petäjävesi': 'Petäjävedeltä',
    'Pihtipudas': 'Pihtiputaalta', 'Toivakka': 'Toivakasta', 'Uurainen': 'Uuraisista',
    'Kannonkoski': 'Kannonkoskelta', 'Kivijärvi': 'Kivijärveltä',
    'Kyyjärvi': 'Kyyjärveltä', 'Luhanka': 'Luhangasta',
}
GENITIVE = {
    'Jyväskylä': 'Jyväskylän', 'Jämsä': 'Jämsän', 'Keuruu': 'Keuruun',
    'Äänekoski': 'Äänekosken', 'Saarijärvi': 'Saarijärven', 'Viitasaari': 'Viitasaaren',
    'Laukaa': 'Laukaan', 'Muurame': 'Muuramen', 'Hankasalmi': 'Hankasalmen',
    'Joutsa': 'Joutsan', 'Karstula': 'Karstulaan', 'Kinnula': 'Kinnulan',
    'Konnevesi': 'Konneveden', 'Multia': 'Multian', 'Petäjävesi': 'Petäjäveden',
    'Pihtipudas': 'Pihtipudaksen', 'Toivakka': 'Toivakan', 'Uurainen': 'Uurais',
    'Kannonkoski': 'Kannonkosken', 'Kivijärvi': 'Kivijärven',
    'Kyyjärvi': 'Kyyjärven', 'Luhanka': 'Luhangan',
}
SLUG_MAP = {
    'ä': 'a', 'ö': 'o', 'å': 'a', ' ': '-',
}

def slugify(name):
    result = name.lower()
    for k, v in SLUG_MAP.items():
        result = result.replace(k, v)
    return result

for kunta in KUNNAT:
    nimi = kunta['nimi']
    slug = kunta['slug']
    nimissa = INESSIVE.get(nimi, nimi + 'ssa')
    nimiosta = ELATIVE.get(nimi, nimi + 'sta')
    nimen = GENITIVE.get(nimi, nimi + 'n')
    matka_km = kunta['matka_km']
    if matka_km == 0:
        matka_teksti = " — toimipisteemme on täällä"
    elif matka_km <= 60:
        matka_teksti = f" (noin {matka_km} km)"
    else:
        ylitys = matka_km - 60
        lisahinta = round(ylitys * 1.80)
        matka_teksti = f" (noin {matka_km} km, kuljetuslisä n. {lisahinta} €)"

    lahikunnat_html = "\n      ".join(
        f'<a href="hautauspalvelu-{slugify(k)}.html" class="lk-tag">{k}</a>'
        for k in kunta['lahikunnat']
    )

    html = TEMPLATE.format(
        nimi=nimi, slug=slug, nimissa=nimissa, nimiosta=nimiosta, nimen=nimen,
        kuvaus=kunta['kuvaus'], krematorio=kunta['krematorio'],
        matka_teksti=matka_teksti, lisatieto=kunta['lisatieto'],
        lahikunnat_html=lahikunnat_html,
    )

    fname = f"hautauspalvelu-{slug}.html"
    with open(os.path.join(OUTPUT_DIR, fname), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  OK: {fname}")

print(f"\nValmis — {len(KUNNAT)} sivua generoitu hakemistoon {OUTPUT_DIR}")
