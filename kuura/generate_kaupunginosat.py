#!/usr/bin/env python3
"""Generoi kaupunginosasivut Kuura-siivouspalvelulle."""
import os

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "kaupunginosat")
os.makedirs(OUTPUT_DIR, exist_ok=True)

NAAPURUSTOT = [
    {"nimi": "Keskusta", "slug": "keskusta", "kuvaus": "Jyväskylän eläväinen ydinkeskusta — toimistot, kerrostalot ja liiketilat."},
    {"nimi": "Kuokkala", "slug": "kuokkala", "kuvaus": "Vireä asuinalue Jyväskylän eteläosassa, täynnä rivitaloja ja omakotitaloja."},
    {"nimi": "Taulumäki", "slug": "taulumaki", "kuvaus": "Rauhallinen omakotitaloalue lähellä Jyväskylän keskustaa."},
    {"nimi": "Seppälä", "slug": "seppala", "kuvaus": "Kaupallinen ja asuinalue Jyväskylän pohjoisosassa."},
    {"nimi": "Palokka", "slug": "palokka", "kuvaus": "Suosittu perhealue Jyväskylän pohjoisella laidalla."},
    {"nimi": "Keljo", "slug": "keljo", "kuvaus": "Vehreä asuinalue Jyväskylän länsiosassa."},
    {"nimi": "Halssila", "slug": "halssila", "kuvaus": "Monipuolinen asuinalue Jyväskylän itäosassa."},
    {"nimi": "Kortepohja", "slug": "kortepohja", "kuvaus": "Opiskelijakylästään tunnettu alue lähellä yliopistoa."},
    {"nimi": "Myllyjärvi", "slug": "myllyjärvi", "kuvaus": "Rauhallinen omakotitaloalue hyvien yhteyksien varrella."},
    {"nimi": "Pupuhuhta", "slug": "pupuhuhta", "kuvaus": "Perheystävällinen alue Jyväskylän eteläosassa."},
    {"nimi": "Keltinmäki", "slug": "keltinmaki", "kuvaus": "Kerrostalo- ja rivitaloaluetta lähellä keskustaa."},
    {"nimi": "Vaajakoski", "slug": "vaajakoski", "kuvaus": "Kasvava taajama Jyväskylän itäreunalla, hyvät kulkuyhteydet."},
    {"nimi": "Jyskä", "slug": "jyska", "kuvaus": "Moderni asuinalue Vaajakosken tuntumassa."},
    {"nimi": "Lohikoski", "slug": "lohikoski", "kuvaus": "Vehreä asuinalue luonnon äärellä Jyväskylässä."},
    {"nimi": "Huhtasuo", "slug": "huhtasuo", "kuvaus": "Yhteisöllinen kerrostaloalue Jyväskylässä."},
    {"nimi": "Ristonmaa", "slug": "ristonmaa", "kuvaus": "Rauhallinen pientaloalue hyvien palvelujen lähellä."},
    {"nimi": "Mannila", "slug": "mannila", "kuvaus": "Pienimuotoinen asuinalue Jyväskylän pohjoisosassa."},
    {"nimi": "Tikka", "slug": "tikka", "kuvaus": "Omakotitaloalue Jyväskylän länsiosassa."},
    {"nimi": "Ainola", "slug": "ainola", "kuvaus": "Arvokas omakotitaloalue aivan Jyväskylän ydinkeskustan tuntumassa."},
    {"nimi": "Säynätsalo", "slug": "saynatsalo", "kuvaus": "Alvar Aallon suunnittelema historiallinen saariyhteisö Jyväskylässä."},
    {"nimi": "Haukkala", "slug": "haukkala", "kuvaus": "Väljä omakotitaloalue luonnon läheisyydessä."},
    {"nimi": "Kangasvuori", "slug": "kangasvuori", "kuvaus": "Hiljainen omakotitaloalue Jyväskylän reunamilla."},
]

HINNAT = [
    ("Perus", "139", "noin 2 h", ["Imurointi", "Pyyhintä", "Keittiö", "WC"]),
    ("Kodikas", "199", "noin 3 h", ["Kaikki Peruksen sisältö", "Ikkunoiden pyyhintä", "Kaappien ulkopinnat", "Kylpyhuone perusteellisesti"]),
    ("Täydellinen", "299", "noin 4–5 h", ["Kaikki Kodikkaan sisältö", "Kaapit sisältä", "Kodinkoneet", "Saunan pesu"]),
]

TEMPLATE = '''<!DOCTYPE html>
<html lang="fi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Siivouspalvelu {nimi}, Jyväskylä — Kuura</title>
<meta name="description" content="Kuura tarjoaa luotettavan ja edullisen siivouspalvelun {nimissa}. Kotitalousvähennys hyödynnettävissä — asiakas maksaa vain noin 50 % hinnasta. Varaa aika helposti.">
<link rel="canonical" href="https://kuura.fi/kaupunginosat/kuura-{slug}/">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;1,300;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{
  --teal:#1a4a5c;--teal-l:#2a6a80;--teal-xl:#e8f2f5;
  --terra:#c9663c;--cream:#f8f6f1;--white:#fff;
  --dark:#0f1e26;--text:#1e3340;--text-m:#4a6070;
  --border:#d5e0e6;--border-l:#e8f0f4;--stone:#f2ede4;
}}
html{{scroll-behavior:smooth;background:var(--cream)}}
body{{font-family:'Inter',sans-serif;color:var(--text);background:var(--cream);line-height:1.6;overflow-x:hidden}}
.nav{{background:rgba(248,246,241,.96);border-bottom:1px solid var(--border);padding:0 40px;height:64px;display:flex;align-items:center;justify-content:space-between;position:sticky;top:0;z-index:100;backdrop-filter:blur(8px)}}
.nav-logo{{font-family:'Cormorant Garamond',serif;font-size:22px;font-weight:500;color:var(--teal);text-decoration:none;letter-spacing:.01em}}
.nav-right{{display:flex;align-items:center;gap:14px}}
.nav-phone{{font-size:13px;font-weight:600;color:var(--teal);text-decoration:none;border:1px solid var(--teal);border-radius:4px;padding:7px 16px;transition:all .15s}}
.nav-phone:hover{{background:var(--teal);color:#fff}}
.hero{{background:var(--dark);padding:80px 40px;position:relative;overflow:hidden}}
.hero-tint{{position:absolute;inset:0;background:linear-gradient(135deg,rgba(26,74,92,.3) 0%,transparent 60%);pointer-events:none}}
.hero-inner{{max-width:900px;margin:0 auto;position:relative}}
.hero-eyebrow{{font-size:10px;font-weight:600;letter-spacing:.22em;text-transform:uppercase;color:rgba(168,210,220,.7);margin-bottom:16px}}
.hero-h1{{font-family:'Cormorant Garamond',serif;font-size:clamp(36px,5vw,64px);font-weight:300;color:#f5f2ec;line-height:1.08;margin-bottom:20px}}
.hero-h1 em{{font-style:italic;color:#a8d4dc}}
.hero-p{{font-size:16px;font-weight:300;color:rgba(245,242,236,.55);line-height:1.9;max-width:520px;margin-bottom:36px}}
.hero-btns{{display:flex;gap:12px;flex-wrap:wrap}}
.btn-t{{display:inline-flex;align-items:center;gap:8px;background:var(--teal);color:#fff;font-size:13px;font-weight:500;padding:13px 24px;border-radius:4px;text-decoration:none;transition:background .15s}}
.btn-t:hover{{background:var(--teal-l)}}
.btn-o{{display:inline-flex;align-items:center;gap:8px;background:transparent;border:1px solid rgba(245,242,236,.2);color:rgba(245,242,236,.65);font-size:13px;font-weight:500;padding:13px 24px;border-radius:4px;text-decoration:none}}
.kv-bar{{background:var(--teal);padding:14px 40px;display:flex;justify-content:center;gap:48px;flex-wrap:wrap}}
.kv-item{{display:flex;align-items:center;gap:8px}}
.kv-item svg{{width:14px;height:14px;stroke:rgba(168,210,220,.9)}}
.kv-text{{font-size:12px;font-weight:500;color:rgba(255,255,255,.75)}}
.content{{max-width:900px;margin:0 auto;padding:72px 40px}}
.section{{margin-bottom:56px}}
.section h2{{font-family:'Cormorant Garamond',serif;font-size:clamp(26px,3.5vw,40px);font-weight:300;color:var(--dark);margin-bottom:12px;line-height:1.1}}
.section h2 em{{font-style:italic;color:var(--teal)}}
.section-rule{{width:36px;height:1px;background:var(--teal);margin-bottom:20px}}
.section p{{font-size:14px;font-weight:300;color:var(--text-m);line-height:1.9;margin-bottom:12px}}
.pkg-grid{{display:grid;grid-template-columns:repeat(3,1fr);gap:18px;margin-top:28px}}
.pkg{{background:var(--white);border:1px solid var(--border-l);border-radius:8px;padding:28px 22px}}
.pkg.featured{{background:var(--teal);border-color:var(--teal)}}
.pkg-name{{font-size:11px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:var(--text-m);margin-bottom:10px}}
.pkg.featured .pkg-name{{color:rgba(255,255,255,.5)}}
.pkg-price{{font-family:'Cormorant Garamond',serif;font-size:44px;font-weight:300;color:var(--dark);line-height:1;margin-bottom:2px}}
.pkg.featured .pkg-price{{color:#fff}}
.pkg-dur{{font-size:11px;color:var(--text-m);margin-bottom:18px}}
.pkg.featured .pkg-dur{{color:rgba(255,255,255,.45)}}
.pkg-list{{list-style:none}}
.pkg-list li{{font-size:12px;font-weight:300;color:var(--text-m);padding:5px 0;border-top:1px solid var(--border-l);display:flex;gap:7px;line-height:1.5}}
.pkg.featured .pkg-list li{{color:rgba(255,255,255,.65);border-top-color:rgba(255,255,255,.1)}}
.pkg-list li::before{{content:'';width:5px;height:5px;border-radius:50%;background:var(--teal);flex-shrink:0;margin-top:5px}}
.pkg.featured .pkg-list li::before{{background:#a8d4dc}}
.kv-box{{background:var(--stone);border:1px solid var(--border-l);border-radius:10px;padding:36px;margin-top:0}}
.kv-box h3{{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:300;color:var(--dark);margin-bottom:14px}}
.kv-calc{{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:20px}}
.kv-num{{background:var(--white);border-radius:6px;padding:20px;text-align:center}}
.kv-val{{font-family:'Cormorant Garamond',serif;font-size:38px;font-weight:300;color:var(--teal);line-height:1}}
.kv-label{{font-size:11px;font-weight:500;color:var(--text-m);letter-spacing:.04em;margin-top:4px}}
.contact-box{{background:var(--white);border:1px solid var(--border-l);border-radius:10px;padding:36px}}
.contact-box h3{{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:300;color:var(--dark);margin-bottom:16px}}
.cf-field{{width:100%;background:var(--cream);border:1px solid var(--border);border-radius:4px;padding:11px 13px;font-size:13px;font-family:inherit;color:var(--text);outline:none;margin-bottom:10px}}
.cf-field:focus{{border-color:var(--teal)}}
.fld2{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.btn-submit{{width:100%;background:var(--teal);color:#fff;border:none;border-radius:4px;padding:13px;font-size:13px;font-weight:500;cursor:pointer;font-family:inherit;margin-top:6px}}
.breadcrumb{{font-size:12px;color:var(--text-m);margin-bottom:20px}}
.breadcrumb a{{color:var(--text-m);text-decoration:none}}
.breadcrumb a:hover{{color:var(--teal)}}
footer{{background:var(--dark);padding:36px 40px;text-align:center}}
.ftr-logo{{font-family:'Cormorant Garamond',serif;font-size:20px;color:#f5f2ec;margin-bottom:6px}}
.ftr-sub{{font-size:11px;color:rgba(245,242,236,.28)}}
@media(max-width:768px){{.nav{{padding:0 20px}}.hero{{padding:56px 20px}}.content{{padding:48px 20px}}.pkg-grid{{grid-template-columns:1fr}}.kv-calc{{grid-template-columns:1fr 1fr}}.fld2{{grid-template-columns:1fr}}.kv-bar{{gap:16px;padding:12px 20px}}footer{{padding:28px 20px}}}}
</style>
</head>
<body>

<nav class="nav">
  <a href="../" class="nav-logo">Kuura</a>
  <div class="nav-right">
    <a href="tel:+358401234567" class="nav-phone">040 123 4567</a>
  </div>
</nav>

<section class="hero">
  <div class="hero-tint"></div>
  <div class="hero-inner">
    <p class="hero-eyebrow">Siivouspalvelu {nimissa} — Jyväskylä</p>
    <h1 class="hero-h1">Puhdas koti<em> {nimissa}</em></h1>
    <p class="hero-p">{kuvaus} Kuura tuo ammattimaisen ja luotettavan siivouspalvelun suoraan kotiisi — kotitalousvähennyksellä maksat vain noin puolet.</p>
    <div class="hero-btns">
      <a href="#varaa" class="btn-t">Varaa siivous</a>
      <a href="#hinnat" class="btn-o">Katso hinnat</a>
    </div>
  </div>
</section>

<div class="kv-bar">
  <div class="kv-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="kv-text">Kotitalousvähennys hyödynnettävissä</span>
  </div>
  <div class="kv-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="kv-text">Kiinteä hinta, ei yllätyksiä</span>
  </div>
  <div class="kv-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="kv-text">Vakuutettu palvelu</span>
  </div>
  <div class="kv-item">
    <svg viewBox="0 0 24 24" fill="none" stroke-width="1.5" stroke-linecap="round"><polyline points="20 6 9 17 4 12"/></svg>
    <span class="kv-text">Helppo varaus verkossa</span>
  </div>
</div>

<div class="content">
  <div class="breadcrumb">
    <a href="../">Kuura</a> &rsaquo; Siivouspalvelu {nimissa}
  </div>

  <div class="section">
    <h2>Siivouspalvelu <em>{nimissa}</em></h2>
    <div class="section-rule"></div>
    <p>{kuvaus} Kuura palvelee kaikkia {nimen} kotitalouksia — varaa aika verkossa ja ammattilaiset tulevat sovittuna päivänä.</p>
    <p>Kotitalousvähennyksellä tehokkaasti hyödynnettynä todellinen hintasi on vain noin puolet listahinnoista. Vähennys koskee työn osuutta, joka on 60 % pakettihinnastamme.</p>
  </div>

  <div class="section" id="hinnat">
    <h2>Hinnat — <em>kiinteä hinta</em></h2>
    <div class="section-rule"></div>
    <p>Kaikki paketit ovat kiinteähintaisia. Saat laskun työn päätteeksi — ei lisäveloituksia, ei yllätyksiä.</p>
    <div class="pkg-grid">
      <div class="pkg">
        <p class="pkg-name">Perus</p>
        <div class="pkg-price">139 €</div>
        <p class="pkg-dur">noin 2 h &bull; ~70 € kotitalousvähennyksellä</p>
        <ul class="pkg-list">
          <li>Imurointi kaikissa huoneissa</li>
          <li>Pölyjen pyyhintä</li>
          <li>Keittiön pintojen puhdistus</li>
          <li>WC:n pesu</li>
        </ul>
      </div>
      <div class="pkg featured">
        <p class="pkg-name">Kodikas</p>
        <div class="pkg-price">199 €</div>
        <p class="pkg-dur">noin 3 h &bull; ~100 € kotitalousvähennyksellä</p>
        <ul class="pkg-list">
          <li>Kaikki Perus-paketin sisältö</li>
          <li>Ikkunoiden pyyhintä sisältä</li>
          <li>Kaappien ulkopinnat</li>
          <li>Kylpyhuoneen perusteellinen pesu</li>
        </ul>
      </div>
      <div class="pkg">
        <p class="pkg-name">Täydellinen</p>
        <div class="pkg-price">299 €</div>
        <p class="pkg-dur">noin 4–5 h &bull; ~150 € kotitalousvähennyksellä</p>
        <ul class="pkg-list">
          <li>Kaikki Kodikas-paketin sisältö</li>
          <li>Kaapit sisältä</li>
          <li>Kodinkoneiden puhdistus</li>
          <li>Saunan pesu</li>
        </ul>
      </div>
    </div>
  </div>

  <div class="section">
    <h2>Kotitalousvähennys <em>puolittaa hinnan</em></h2>
    <div class="section-rule"></div>
    <div class="kv-box">
      <h3>Kuinka paljon säästät?</h3>
      <p style="font-size:14px;font-weight:300;color:var(--text-m);line-height:1.85;margin-bottom:16px">Kotitalousvähennys on 40 % työn arvonlisäverottomasta osuudesta, enintään 2 250 € vuodessa. Kuuran paketeissa työn osuus on noin 60 % hinnasta.</p>
      <div class="kv-calc">
        <div class="kv-num">
          <div class="kv-val">139 €</div>
          <div class="kv-label">Perus — listahinta</div>
        </div>
        <div class="kv-num">
          <div class="kv-val" style="color:var(--terra)">~70 €</div>
          <div class="kv-label">Sinulle jää maksettavaa</div>
        </div>
        <div class="kv-num">
          <div class="kv-val">199 €</div>
          <div class="kv-label">Kodikas — listahinta</div>
        </div>
        <div class="kv-num">
          <div class="kv-val" style="color:var(--terra)">~100 €</div>
          <div class="kv-label">Sinulle jää maksettavaa</div>
        </div>
      </div>
      <p style="font-size:12px;color:var(--text-m);margin-top:16px;line-height:1.7">*Laskelma on suuntaa-antava. Todellinen vähennys riippuu vuosittaisesta verosta. Hoidamme paperityöt puolestasi.</p>
    </div>
  </div>

  <div class="section" id="varaa">
    <h2>Varaa siivous <em>{nimissa}</em></h2>
    <div class="section-rule"></div>
    <div class="contact-box">
      <h3>Yhteydenotto</h3>
      <div class="fld2">
        <input class="cf-field" type="text" placeholder="Etunimi">
        <input class="cf-field" type="text" placeholder="Sukunimi">
      </div>
      <input class="cf-field" type="tel" placeholder="Puhelin" style="margin-top:10px">
      <input class="cf-field" type="email" placeholder="Sähköposti">
      <input class="cf-field" type="text" placeholder="Osoite {nimissa}">
      <select class="cf-field">
        <option value="">Valitse paketti</option>
        <option>Perus — 139 € (~70 € kotitalousvähennyksellä)</option>
        <option>Kodikas — 199 € (~100 € kotitalousvähennyksellä)</option>
        <option>Täydellinen — 299 € (~150 € kotitalousvähennyksellä)</option>
        <option>Loppusiivous — pyydä tarjous</option>
      </select>
      <textarea class="cf-field" style="height:90px;resize:vertical" placeholder="Lisätietoja (asunnon koko, erityistoiveet...)"></textarea>
      <button class="btn-submit">Lähetä varaus</button>
    </div>
  </div>
</div>

<footer>
  <div class="ftr-logo">Kuura</div>
  <div class="ftr-sub">Puhdas koti, selkeä mieli. — 040 123 4567 — info@kuura.fi — Jyväskylä</div>
</footer>

</body>
</html>
'''

INESSIVE = {{
    'Keskusta': 'Keskustassa', 'Kuokkala': 'Kuokkalassa', 'Taulumäki': 'Taulumäellä',
    'Seppälä': 'Seppälässä', 'Palokka': 'Palokassa', 'Keljo': 'Keljossa',
    'Halssila': 'Halssilassa', 'Kortepohja': 'Kortepohjassa', 'Myllyjärvi': 'Myllyjärvellä',
    'Pupuhuhta': 'Pupuhuhdassa', 'Keltinmäki': 'Keltinmäellä', 'Vaajakoski': 'Vaajakoskella',
    'Jyskä': 'Jyskässä', 'Lohikoski': 'Lohikoskella', 'Huhtasuo': 'Huhtasuolla',
    'Ristonmaa': 'Ristonmaalla', 'Mannila': 'Mannilassa', 'Tikka': 'Tikassa',
    'Ainola': 'Ainolassa', 'Säynätsalo': 'Säynätsalossa', 'Haukkala': 'Haukkalassa',
    'Kangasvuori': 'Kangasvuorella',
}}
GENITIVE = {{
    'Keskusta': 'Keskustan', 'Kuokkala': 'Kuokkalan', 'Taulumäki': 'Taulumäen',
    'Seppälä': 'Seppälän', 'Palokka': 'Palokan', 'Keljo': 'Keljon',
    'Halssila': 'Halssilaan', 'Kortepohja': 'Kortepohjan', 'Myllyjärvi': 'Myllyjärven',
    'Pupuhuhta': 'Pupuhuhdan', 'Keltinmäki': 'Keltinmäen', 'Vaajakoski': 'Vaajakosken',
    'Jyskä': 'Jyskän', 'Lohikoski': 'Lohikosken', 'Huhtasuo': 'Huhtasuon',
    'Ristonmaa': 'Ristonmaan', 'Mannila': 'Mannilan', 'Tikka': 'Tikan',
    'Ainola': 'Ainolan', 'Säynätsalo': 'Säynätsalon', 'Haukkala': 'Haukkalan',
    'Kangasvuori': 'Kangasvuoren',
}}

for n in NAAPURUSTOT:
    nimi = n['nimi']
    slug = n['slug']
    nimissa = INESSIVE.get(nimi, nimi + 'ssa')
    nimen = GENITIVE.get(nimi, nimi + 'n')

    html = TEMPLATE.format(
        nimi=nimi, slug=slug, nimissa=nimissa, nimen=nimen,
        kuvaus=n['kuvaus'],
    )

    fname = f"kuura-{slug}.html"
    with open(os.path.join(OUTPUT_DIR, fname), 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"  OK: {fname}")

print(f"\nValmis — {len(NAAPURUSTOT)} sivua generoitu hakemistoon {OUTPUT_DIR}")
