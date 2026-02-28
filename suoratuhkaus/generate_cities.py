#!/usr/bin/env python3
"""
Generoi landing page jokaiselle Suomen kunnalle suoratuhkaus.fi -sivustolle.
Luo Google Sheet linkeillä + Drive-kansio + siirtää dokumentit.
"""
import os, math, json, time, re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

with open('/home/node/.openclaw/workspace/google_token.json') as f:
    creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)

sheets = build('sheets', 'v4', credentials=creds)
drive  = build('drive',  'v3', credentials=creds)

# ── DATA ────────────────────────────────────────────────────────────────────

KUNNAT = {
  "Akaa":[61.1715,23.8599],"Alajärvi":[62.9958,23.8117],"Alavieska":[63.9971,24.3196],"Alavus":[62.589,23.6232],
  "Asikkala":[61.1772,25.5524],"Askola":[60.5271,25.5952],"Äänekoski":[62.5985,25.7253],
  "Enonkoski":[61.9917,28.7498],"Enontekiö":[68.3777,23.6231],"Espoo":[60.2052,24.6522],
  "Eura":[61.1335,22.1363],"Eurajoki":[61.2013,21.7263],"Evijärvi":[63.3629,23.4847],
  "Forssa":[60.8153,23.6207],"Haapajärvi":[63.7571,25.337],"Haapavesi":[64.1383,25.3556],
  "Hailuoto":[65.0333,25.1333],"Halsua":[63.4588,24.1879],"Hamina":[60.5692,27.1963],
  "Hankasalmi":[62.3937,26.4254],"Hanko":[59.8297,23.0004],"Harjavalta":[61.3172,22.1541],
  "Hartola":[61.5857,26.0158],"Hattula":[61.0565,24.3452],"Hausjärvi":[60.7787,25.0145],
  "Heinola":[61.2012,26.0332],"Heinävesi":[62.4357,28.6392],"Helsinki":[60.1699,24.9384],
  "Hirvensalmi":[61.6335,26.8059],"Hollola":[60.9906,25.5157],"Huittinen":[61.1762,22.698],
  "Humppila":[60.9191,23.3843],"Hyrynsalmi":[64.6763,28.5375],"Hyvinkää":[60.6317,24.8606],
  "Hämeenkyrö":[61.6375,23.1939],"Hämeenlinna":[60.9961,24.4645],"Ii":[65.3116,25.3788],
  "Iisalmi":[63.5567,27.1915],"Ikaalinen":[61.7694,23.0663],"Ilmajoki":[62.7344,22.5743],
  "Ilomantsi":[62.668,30.9166],"Imatra":[61.1723,28.772],"Inari":[68.9038,27.0256],
  "Inkoo":[60.0547,24.0028],"Isojoki":[62.1198,21.9649],"Isokyrö":[62.9961,22.3164],
  "Janakkala":[60.8961,24.6007],"Joensuu":[62.601,29.7636],"Jokioinen":[60.8041,23.4806],
  "Joroinen":[62.1768,27.8216],"Joutseno":[61.1137,28.5009],"Joutsa":[61.7481,26.1094],
  "Juuka":[63.2408,29.2497],"Jurva":[62.6736,21.9887],"Juva":[61.8993,27.8619],
  "Jyväskylä":[62.2415,25.7209],"Jämsä":[61.8638,25.1901],"Järvenpää":[60.4749,25.0898],
  "Kaarina":[60.4035,22.3752],"Kajaani":[64.2273,27.729],"Kalajoki":[64.2594,23.9573],
  "Kangasala":[61.4647,24.0727],"Kangasniemi":[61.9875,26.6479],"Kankaanpää":[61.8018,22.3966],
  "Kannonkoski":[63.156,25.3442],"Kannus":[63.9019,23.923],"Karijoki":[62.2238,21.8396],
  "Karstula":[62.8726,24.7973],"Kaskinen":[62.3802,21.2225],"Kauhajoki":[62.4321,22.1771],
  "Kauhava":[63.1042,23.0618],"Kaustinen":[63.5518,23.6947],"Keitele":[63.1907,26.3337],
  "Kemi":[65.7368,24.5642],"Kemijärvi":[66.7141,27.4289],"Keminmaa":[65.7803,24.5644],
  "Kemiönsaari":[60.178,22.7246],"Kempele":[64.9134,25.5217],"Kerava":[60.4032,25.1043],
  "Keuruu":[62.2594,24.7051],"Kihniö":[62.2049,23.1671],"Kiiminki":[65.1356,25.7488],
  "Kinnula":[63.3856,25.0055],"Kirkkonummi":[60.1282,24.4422],"Kitee":[62.0978,30.1447],
  "Kittilä":[67.6596,24.904],"Kiuruvesi":[63.6525,26.6186],"Kokemäki":[61.2586,22.3517],
  "Kokkola":[63.8373,23.1333],"Kolari":[67.3368,23.7938],"Kontiolahti":[62.7494,29.8454],
  "Korsnäs":[62.8793,21.2124],"Kotka":[60.4669,26.9458],"Kouvola":[60.8679,26.7042],
  "Kristiinankaupunki":[62.2752,21.3716],"Kruunupyy":[63.7228,23.0126],"Kuhmo":[64.1282,29.5212],
  "Kuhmoinen":[61.5639,25.1814],"Kuopio":[62.8924,27.677],"Kuortane":[62.8048,23.5074],
  "Kurikka":[62.6088,22.4185],"Kuusamo":[65.9651,29.186],"Kyyjärvi":[62.9956,24.5735],
  "Kärkölä":[60.8828,25.3111],"Kärsämäki":[63.9842,25.7591],"Lahti":[60.9827,25.6617],
  "Laihia":[62.978,22.0043],"Laitila":[60.8774,21.6942],"Lapinjärvi":[60.6123,26.1519],
  "Lapinlahti":[63.3644,27.3978],"Lappeenranta":[61.0587,28.1887],"Lapua":[62.9714,23.006],
  "Laukaa":[62.4162,25.9449],"Lemi":[61.0533,28.3169],"Lempäälä":[61.3161,23.751],
  "Leppävirta":[62.4917,27.7725],"Lestijärvi":[63.5367,24.6507],"Lieto":[60.4993,22.4568],
  "Liperi":[62.533,29.383],"Lohja":[60.25,24.0664],"Loimaa":[60.8534,23.0564],
  "Loppi":[60.7248,24.4428],"Loviisa":[60.4573,26.2247],"Lumijoki":[64.8854,25.154],
  "Luoto":[63.7978,22.9027],"Luumäki":[60.9156,27.5824],"Maalahti":[62.945,21.5573],
  "Maaninka":[63.1667,27.3003],"Marttila":[60.6259,22.9072],"Masku":[60.5705,22.1053],
  "Merijärvi":[64.1178,24.1665],"Merikarvia":[61.8524,21.5012],"Miehikkälä":[60.6734,27.4613],
  "Mikkeli":[61.688,27.2727],"Muhos":[64.8082,25.9906],"Multia":[62.4285,24.7786],
  "Muonio":[67.957,23.6774],"Mustasaari":[63.1155,21.7826],"Mynämäki":[60.6835,21.9896],
  "Myrskylä":[60.674,25.8559],"Mäntsälä":[60.6355,25.3191],"Mäntyharju":[61.4134,26.8817],
  "Mänttä-Vilppula":[62.0271,24.6258],"Naantali":[60.4676,22.0247],"Nakkila":[61.3633,21.9],
  "Nilsiä":[63.1897,28.0702],"Nivala":[63.9285,24.9745],"Nokia":[61.4783,23.5091],
  "Nousiainen":[60.6367,22.1383],"Nurmes":[63.5441,29.1279],"Nurmijärvi":[60.4676,24.8046],
  "Orimattila":[60.8049,25.7314],"Orivesi":[61.6759,24.366],"Oulainen":[64.2669,24.8196],
  "Oulu":[65.0121,25.4651],"Padasjoki":[61.3478,25.1128],"Paimio":[60.4574,22.6831],
  "Paltamo":[64.3928,27.8301],"Parainen":[60.3006,22.3006],"Parkano":[62.0135,23.0188],
  "Pedersören kunta":[63.6455,22.9063],"Pelkosenniemi":[67.1091,27.5098],"Pello":[66.7765,23.9649],
  "Perho":[63.3125,24.5213],"Pertunmaa":[61.505,26.4803],"Petäjävesi":[62.2579,25.1934],
  "Pieksämäki":[62.3018,27.1399],"Pielavesi":[63.2373,26.765],"Pietarsaari":[63.6731,22.6915],
  "Pihtipudas":[63.3744,25.5696],"Pirkkala":[61.4635,23.6445],"Polvijärvi":[62.8544,29.3879],
  "Pomarkku":[61.6928,22.0238],"Pornainen":[60.4821,25.368],"Porvoo":[60.3929,25.6647],
  "Posio":[66.1109,28.1593],"Pudasjärvi":[65.3622,26.9153],"Pukkila":[60.6393,25.5673],
  "Punkalaidun":[61.1138,23.1009],"Puolanka":[64.8663,27.6722],"Puumala":[61.5267,28.1829],
  "Pyhäjärvi":[63.6682,25.9049],"Pyhäjoki":[64.4634,24.239],"Pyhäranta":[60.9544,21.4607],
  "Pälkäne":[61.3421,24.28],"Pöytyä":[60.727,22.6921],"Raahe":[64.684,24.4805],
  "Raisio":[60.4864,22.1714],"Ranua":[65.9271,26.5296],"Rauma":[61.1285,21.5107],
  "Rautalampi":[62.6289,26.8359],"Rautavaara":[63.8617,28.3088],"Rautjärvi":[61.4035,29.3455],
  "Reisjärvi":[63.8224,25.2889],"Riihimäki":[60.7392,24.7759],"Ristijärvi":[64.5076,28.2211],
  "Rovaniemi":[66.5039,25.7294],"Ruokolahti":[61.2883,28.8262],"Ruovesi":[61.9836,24.071],
  "Saarijärvi":[62.7059,25.2553],"Saari":[61.6782,29.8127],"Salla":[67.0993,28.6736],
  "Salo":[60.3839,23.1247],"Sastamala":[61.3441,22.9028],"Savitaipale":[61.1971,27.7069],
  "Savonlinna":[61.8693,28.8812],"Savukoski":[67.2953,29.0987],"Seinäjoki":[62.7906,22.8403],
  "Sievi":[63.9085,24.5146],"Siikajoki":[64.8348,25.084],"Siikalatva":[64.2823,26.173],
  "Siilinjärvi":[63.0767,27.6587],"Simo":[65.658,25.0638],"Sipoo":[60.3756,25.2711],
  "Siuntio":[60.1475,24.2148],"Sodankylä":[67.4181,26.5892],"Soini":[62.8641,24.222],
  "Somero":[60.6334,23.5168],"Sonkajärvi":[63.6784,27.5238],"Sotkamo":[64.1329,28.4022],
  "Sulkava":[61.7828,28.3727],"Suomussalmi":[64.8792,28.9026],"Suonenjoki":[62.6238,27.1178],
  "Sysmä":[61.5028,25.6888],"Taipalsaari":[61.1768,28.0863],"Taivalkoski":[65.5693,28.2393],
  "Taivassalo":[60.5621,21.5688],"Tammela":[60.8122,23.8079],"Tampere":[61.4978,23.761],
  "Tervo":[62.9488,26.7561],"Tervola":[66.0837,24.8054],"Teuva":[62.4841,21.7447],
  "Tohmajärvi":[62.2259,30.3476],"Toholampi":[63.7795,24.2436],"Toivakka":[62.0878,26.0912],
  "Tornio":[65.8501,24.1441],"Turku":[60.4518,22.2666],"Tuusula":[60.4034,25.0219],
  "Tuusniemi":[62.808,28.482],"Tyrnävä":[64.8073,25.6532],"Ulvila":[61.4271,21.8777],
  "Urjala":[61.082,23.5345],"Utajärvi":[64.7537,26.4189],"Utsjoki":[69.9078,27.0219],
  "Uurainen":[62.5231,25.4094],"Uusikaupunki":[60.7978,21.4082],"Uusikaarlepyy":[63.5229,22.5315],
  "Vaala":[64.5476,26.7753],"Vaasa":[63.096,21.6158],"Valkeakoski":[61.263,24.033],
  "Vantaa":[60.2934,25.0378],"Varkaus":[62.3155,27.8718],"Vesilahti":[61.3452,23.619],
  "Veteli":[63.4741,23.6908],"Vieremä":[63.7599,26.9944],"Vihti":[60.4218,24.3953],
  "Vimpeli":[63.1508,23.8277],"Virolahti":[60.5362,27.6861],"Virrat":[62.2388,23.7731],
  "Ylivieska":[64.0745,24.5565],"Ylitornio":[66.3176,23.6679],"Ylöjärvi":[61.5563,23.5941],
  "Ypäjä":[60.7854,23.3199],"Ähtäri":[62.5564,24.0723]
}

KREMATORIOT = [
  {"n":"Helsinki","lat":60.1726,"lng":24.9113},
  {"n":"Vantaa","lat":60.3218,"lng":25.0611},
  {"n":"Tampere","lat":61.5016,"lng":23.758},
  {"n":"Turku","lat":60.4518,"lng":22.2666},
  {"n":"Oulu","lat":65.0121,"lng":25.4651},
  {"n":"Jyväskylä","lat":62.2328,"lng":25.7292},
  {"n":"Kuopio","lat":62.8924,"lng":27.677},
  {"n":"Lahti","lat":60.9827,"lng":25.6617},
  {"n":"Joensuu","lat":62.601,"lng":29.7636},
  {"n":"Rovaniemi","lat":66.5039,"lng":25.7294},
  {"n":"Hämeenlinna","lat":60.9961,"lng":24.4645},
  {"n":"Kouvola","lat":60.8679,"lng":26.7042},
  {"n":"Seinäjoki","lat":62.7906,"lng":22.8403},
  {"n":"Vaasa","lat":63.096,"lng":21.6158},
  {"n":"Mikkeli","lat":61.688,"lng":27.2727},
  {"n":"Pori","lat":61.4851,"lng":21.7975},
  {"n":"Lappeenranta","lat":61.0587,"lng":28.1887},
  {"n":"Kajaani","lat":64.2273,"lng":27.729},
  {"n":"Savonlinna","lat":61.8693,"lng":28.8812},
  {"n":"Kemi","lat":65.7368,"lng":24.5642},
  {"n":"Kotka","lat":60.4669,"lng":26.9458},
  {"n":"Hyvinkää","lat":60.6317,"lng":24.8606},
  {"n":"Rauma","lat":61.1285,"lng":21.5107},
  {"n":"Kokkola","lat":63.8373,"lng":23.1333},
  {"n":"Iisalmi","lat":63.5567,"lng":27.1915},
  {"n":"Pietarsaari","lat":63.6731,"lng":22.6915},
  {"n":"Riihimäki","lat":60.7392,"lng":24.7759}
]

# ── HELPERS ─────────────────────────────────────────────────────────────────

def haversine(lat1, lng1, lat2, lng2):
    R = 6371
    dLat = math.radians(lat2 - lat1)
    dLng = math.radians(lng2 - lng1)
    a = math.sin(dLat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dLng/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

def slugify(name):
    s = name.lower()
    replacements = {'ä':'a','ö':'o','å':'a','é':'e','ü':'u',' ':'-','.':'',',':'','(':'',')':'','/':'-'}
    for k, v in replacements.items():
        s = s.replace(k, v)
    s = re.sub(r'[^a-z0-9-]', '', s)
    s = re.sub(r'-+', '-', s)
    return s.strip('-')

def nearest_krematorio(lat, lng):
    best_d = float('inf')
    best_k = None
    for k in KREMATORIOT:
        d = haversine(lat, lng, k['lat'], k['lng'])
        if d < best_d:
            best_d = d
            best_k = k
    road_km = round(best_d * 1.28)
    surcharge = 0
    if road_km > 200:   surcharge = 500
    elif road_km > 120: surcharge = 300
    elif road_km > 60:  surcharge = 150
    return best_k['n'], road_km, surcharge

def nearby_cities(city, lat, lng, n=8):
    dists = []
    for name, coords in KUNNAT.items():
        if name == city: continue
        d = haversine(lat, lng, coords[0], coords[1])
        dists.append((d, name))
    dists.sort()
    return [name for _, name in dists[:n]]

def price_range(surcharge):
    # Perus-paketti: 690 + krematorio 300-600 + surcharge
    lo = 690 + 300 + surcharge
    hi = 690 + 600 + surcharge
    return lo, hi

# ── HTML TEMPLATE ────────────────────────────────────────────────────────────

SHARED_CSS = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{
  --dark:#1c1a17;--dark-m:#2e2b26;
  --forest:#2a3d2e;--forest-m:#364f3a;--forest-l:#4a7858;
  --sage:#6b9478;--sage-l:#9dbfa9;--sage-x:#cddfd5;
  --stone:#f0ebe3;--sand:#e2dbd0;--warm:#faf9f6;
  --terra:#b87355;--terra-l:#d4a080;--terra-x:#f0ddd0;
  --text:#1c1a17;--text-m:#4a4640;--text-l:#8a847a;
}
html{scroll-behavior:smooth}
body{font-family:'Inter',sans-serif;color:var(--text);background:var(--warm);line-height:1.7;overflow-x:hidden}
a{text-decoration:none}
.nav{position:fixed;top:0;left:0;right:0;z-index:300;background:var(--forest)}
.nav-in{max-width:1100px;margin:0 auto;padding:0 24px;height:62px;display:flex;align-items:center;justify-content:space-between;gap:12px}
.logo{display:flex;align-items:center;gap:9px;color:#fff}
.logo-main{font-family:'Cormorant Garamond',serif;font-size:19px;font-weight:600;letter-spacing:.06em;text-transform:uppercase}
.logo-sub{font-size:9px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--sage-l);margin-top:2px;display:block}
.nav-back{font-size:13px;color:rgba(255,255,255,.65);border:1px solid rgba(255,255,255,.2);padding:7px 14px;border-radius:3px;transition:all .15s}
.nav-back:hover{color:#fff;background:rgba(255,255,255,.08)}
.nav-cta{background:var(--terra);color:#fff;padding:8px 18px;border-radius:4px;font-size:13px;font-weight:700;transition:background .15s}
.nav-cta:hover{background:var(--terra-l)}

.hero{padding:110px 24px 72px;background:var(--forest);position:relative;overflow:hidden}
.hero::after{content:'';position:absolute;top:0;right:0;bottom:0;width:45%;opacity:.04;background-image:radial-gradient(var(--sage-l) 1px,transparent 1px);background-size:24px 24px;pointer-events:none}
.hero-in{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 360px;gap:56px;align-items:center}
.hero-ey{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--terra-l);margin-bottom:14px}
.hero-h1{font-family:'Cormorant Garamond',serif;font-size:clamp(38px,5vw,72px);font-weight:300;color:#fff;line-height:1.08;margin-bottom:18px}
.hero-h1 em{font-style:italic;color:var(--sage-l);display:block}
.hero-p{font-size:16px;color:rgba(255,255,255,.65);line-height:1.82;margin-bottom:32px;max-width:480px}
.hero-btns{display:flex;gap:12px;flex-wrap:wrap}
.btn-t{display:inline-flex;align-items:center;gap:8px;background:var(--terra);color:#fff;padding:13px 24px;border-radius:4px;font-size:14px;font-weight:700;transition:background .15s}
.btn-t:hover{background:var(--terra-l)}
.btn-w{display:inline-flex;align-items:center;gap:8px;background:transparent;color:rgba(255,255,255,.85);padding:12px 22px;border-radius:4px;font-size:14px;font-weight:600;border:1.5px solid rgba(255,255,255,.22);transition:all .15s}
.btn-w:hover{background:rgba(255,255,255,.07);border-color:rgba(255,255,255,.5);color:#fff}
.hero-card{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:10px;padding:28px;backdrop-filter:blur(6px)}
.hc-head{font-size:11px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:var(--sage-l);margin-bottom:16px}
.hc-row{display:flex;justify-content:space-between;align-items:center;padding:12px 14px;background:rgba(255,255,255,.05);border-radius:6px;border:1px solid rgba(255,255,255,.08);margin-bottom:8px}
.hc-row:last-of-type{margin-bottom:0}
.hc-label{font-size:13px;color:rgba(255,255,255,.7);font-weight:500}
.hc-val{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:500;color:#fff}
.hc-sub{font-size:11px;color:rgba(255,255,255,.35);margin-top:2px;text-align:right}
.hc-note{font-size:12px;color:rgba(255,255,255,.38);text-align:center;margin-top:14px;line-height:1.7}
.hc-note strong{color:rgba(255,255,255,.55)}

.trust{background:var(--dark);padding:14px 24px}
.trust-in{max-width:1100px;margin:0 auto;display:flex;justify-content:center;flex-wrap:wrap;gap:8px 32px}
.ti{display:flex;align-items:center;gap:7px;font-size:12.5px;color:rgba(255,255,255,.5)}
.ti-dot{width:4px;height:4px;border-radius:50%;background:var(--sage-l);flex-shrink:0}

section{padding:72px 24px}
.wrap{max-width:1100px;margin:0 auto}
.eyebrow{font-size:11px;font-weight:700;letter-spacing:.2em;text-transform:uppercase;color:var(--text-l);margin-bottom:10px}
.eyebrow-t{color:var(--terra)}
.eyebrow-s{color:var(--sage)}
.sec-h2{font-family:'Cormorant Garamond',serif;font-size:clamp(28px,3.5vw,48px);font-weight:400;color:var(--forest);line-height:1.12;margin-bottom:14px}
.sec-p{font-size:15.5px;color:var(--text-m);line-height:1.85}

.info-sect{background:var(--warm)}
.info-grid{display:grid;grid-template-columns:1fr 1fr;gap:64px;align-items:start}
.info-text p{font-size:15.5px;color:var(--text-m);line-height:1.85;margin-bottom:14px}
.info-box{background:var(--stone);border-radius:10px;padding:32px}
.ib-row{display:flex;justify-content:space-between;align-items:flex-start;padding:14px 0;border-bottom:1px solid var(--sand)}
.ib-row:last-child{border-bottom:none}
.ib-label{font-size:13px;color:var(--text-l);font-weight:500}
.ib-val{font-size:15px;font-weight:700;color:var(--forest);text-align:right}
.ib-val small{display:block;font-size:12px;font-weight:400;color:var(--text-l)}

.how-sect{background:var(--stone)}
.how-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:2px;background:var(--sand);border-radius:8px;overflow:hidden;margin-top:40px}
.how-step{background:var(--warm);padding:32px 24px;position:relative}
.how-n{font-family:'Cormorant Garamond',serif;font-size:64px;font-weight:300;color:var(--forest);opacity:.08;line-height:1;position:absolute;top:14px;right:14px}
.how-icon{width:42px;height:42px;background:var(--sage-x);border-radius:50%;display:flex;align-items:center;justify-content:center;margin-bottom:14px}
.how-step h3{font-family:'Cormorant Garamond',serif;font-size:20px;font-weight:500;color:var(--forest);margin-bottom:8px}
.how-step p{font-size:13.5px;color:var(--text-m);line-height:1.72}

.price-sect{background:var(--warm)}
.price-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;max-width:820px;margin:40px auto 0}
.pkg{background:var(--stone);border-radius:10px;padding:34px;border:2px solid transparent;transition:border-color .2s}
.pkg.pop{border-color:var(--forest);position:relative}
.pkg-badge{position:absolute;top:-11px;left:50%;transform:translateX(-50%);background:var(--forest);color:#fff;font-size:10px;font-weight:700;padding:4px 14px;border-radius:20px}
.pkg-name{font-family:'Cormorant Garamond',serif;font-size:26px;font-weight:500;color:var(--forest);margin-bottom:6px}
.pkg-price{display:flex;align-items:baseline;gap:2px;margin:12px 0 4px}
.pkg-eur{font-family:'Cormorant Garamond',serif;font-size:48px;font-weight:400;color:var(--dark);line-height:1}
.pkg-cur{font-family:'Cormorant Garamond',serif;font-size:18px;color:var(--text-m)}
.pkg-note{font-size:12.5px;color:var(--text-l);margin-bottom:18px}
.pkg-rule{height:1px;background:var(--sand);margin-bottom:16px}
.pkg-list{list-style:none;margin-bottom:22px}
.pkg-list li{font-size:13.5px;color:var(--text-m);padding:5px 0;border-bottom:1px solid var(--sand);display:flex;gap:8px;line-height:1.5}
.pkg-list li:last-child{border-bottom:none}
.pkg-list li::before{content:'✓';color:var(--sage);font-weight:700;flex-shrink:0}
.btn-pkg{display:block;width:100%;background:var(--forest);color:#fff;border:none;padding:13px;border-radius:4px;font-family:'Inter',sans-serif;font-size:14px;font-weight:700;cursor:pointer;text-align:center;text-decoration:none;transition:background .15s}
.btn-pkg:hover{background:var(--forest-m)}
.pop .btn-pkg{background:var(--terra)}
.pop .btn-pkg:hover{background:var(--terra-l)}
.krematorio-note{grid-column:1/-1;background:var(--stone);border-radius:8px;padding:24px 28px;border:2px dashed var(--sand);display:flex;justify-content:space-between;align-items:center;gap:20px;flex-wrap:wrap}
.kn-text p{font-size:14px;color:var(--text-m);line-height:1.7;max-width:560px}
.kn-price{font-family:'Cormorant Garamond',serif;font-size:32px;color:var(--forest);flex-shrink:0}

.cta-sect{background:var(--dark);padding:72px 24px;text-align:center}
.cta-sect h2{font-family:'Cormorant Garamond',serif;font-size:clamp(28px,4vw,56px);font-weight:300;color:#fff;line-height:1.1;margin-bottom:10px}
.cta-sect h2 em{font-style:italic;color:var(--sage-l)}
.cta-sect p{font-size:16px;color:rgba(255,255,255,.55);max-width:440px;margin:0 auto 36px;line-height:1.8}
.cta-btns{display:flex;justify-content:center;gap:12px;flex-wrap:wrap;margin-bottom:28px}
.cta-phone{font-size:26px;font-family:'Cormorant Garamond',serif;color:#fff;font-weight:300}
.cta-phone:hover{color:var(--sage-l)}
.cta-note{font-size:12px;color:rgba(255,255,255,.3);margin-top:6px}

.nearby{background:var(--stone);padding:48px 24px}
.nearby h3{font-family:'Cormorant Garamond',serif;font-size:24px;color:var(--forest);margin-bottom:18px}
.nearby-links{display:flex;flex-wrap:wrap;gap:8px}
.nb-link{font-size:13px;color:var(--forest);background:var(--warm);border:1px solid var(--sand);padding:7px 14px;border-radius:4px;transition:all .15s}
.nb-link:hover{background:var(--forest);color:#fff;border-color:var(--forest)}

.ftr{background:var(--dark);padding:40px 24px 24px}
.ftr-in{max-width:1100px;margin:0 auto}
.ftr-top{display:grid;grid-template-columns:2fr 1fr 1fr;gap:40px;padding-bottom:32px;border-bottom:1px solid rgba(255,255,255,.06)}
.ftr-brand{font-family:'Cormorant Garamond',serif;font-size:18px;font-weight:600;color:#fff;letter-spacing:.06em;text-transform:uppercase;margin-bottom:3px}
.ftr-sub{font-size:10px;font-weight:600;letter-spacing:.16em;text-transform:uppercase;color:var(--sage-l);margin-bottom:12px}
.ftr-p{font-size:12.5px;color:rgba(255,255,255,.32);line-height:1.8;max-width:260px}
.ftr-col h4{color:rgba(255,255,255,.65);font-size:10px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin-bottom:12px}
.ftr-col a{display:block;color:rgba(255,255,255,.32);font-size:13px;padding:2px 0;transition:color .14s}
.ftr-col a:hover{color:rgba(255,255,255,.8)}
.ftr-bot{max-width:1100px;margin:18px auto 0;display:flex;justify-content:space-between;font-size:11px;color:rgba(255,255,255,.18)}

.sph{position:fixed;bottom:20px;right:20px;z-index:400;background:var(--terra);color:#fff;padding:11px 20px;border-radius:40px;font-size:13.5px;font-weight:700;box-shadow:0 4px 20px rgba(184,115,85,.45);transition:opacity .3s;display:flex;align-items:center;gap:7px}
.sph:hover{background:var(--terra-l)}

@media(max-width:900px){
  .hero-in{grid-template-columns:1fr}
  .hero-card{max-width:400px}
  .info-grid,.how-grid,.price-grid{grid-template-columns:1fr}
  .krematorio-note{grid-column:1}
  .ftr-top{grid-template-columns:1fr 1fr}
  section{padding:52px 20px}
}
@media(max-width:600px){
  .hero-btns{flex-direction:column}
  .ftr-top{grid-template-columns:1fr}
  .how-grid{gap:1px}
  .price-grid{grid-template-columns:1fr}
}
"""

def html_page(city, slug, lat, lng, krema_name, road_km, surcharge, nearby):
    lo, hi = price_range(surcharge)
    surcharge_line = f"+ kuljetuslisä {surcharge} € (matka {road_km} km)" if surcharge > 0 else ""
    total_range_text = f"{lo:,}–{hi:,} €".replace(",", "\u202f")

    # genitive form attempts (rough)
    gen_map = {
        "Espoo": "Espoossa", "Helsinki": "Helsingissä", "Tampere": "Tampereella",
        "Turku": "Turussa", "Oulu": "Oulussa", "Jyväskylä": "Jyväskylässä",
        "Kuopio": "Kuopiossa", "Lahti": "Lahdessa", "Joensuu": "Joensuussa",
        "Rovaniemi": "Rovaniemellä", "Vaasa": "Vaasassa", "Seinäjoki": "Seinäjoella",
        "Mikkeli": "Mikkelissä", "Lappeenranta": "Lappeenrannassa", "Kouvola": "Kouvolassa",
        "Kotka": "Kotkassa", "Pori": "Porissa", "Kajaani": "Kajaanissa",
        "Savonlinna": "Savonlinnassa", "Kemi": "Kemissä",
    }
    city_ssa = gen_map.get(city, f"{city}ssa" if city[-1] in 'aouåAOU' else f"{city}ssä")

    nearby_links = "\n".join(
        f'<a href="/suoratuhkaus-{slugify(n)}/" class="nb-link">{n}</a>'
        for n in nearby
    )

    # surcharge note in hero card
    surcharge_row = ""
    if surcharge > 0:
        surcharge_row = f"""
        <div class="hc-row">
          <div>
            <div class="hc-label">Kuljetuslisä</div>
          </div>
          <div>
            <div class="hc-val">+{surcharge} €</div>
            <div class="hc-sub">Matka {road_km} km krematoriolle</div>
          </div>
        </div>"""

    production_url = f"https://suoratuhkaus.fi/suoratuhkaus-{slug}/"

    return f"""<!DOCTYPE html>
<html lang="fi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Suoratuhkaus {city} | Läpinäkyvä hinnoittelu – Suoratuhkaus.fi</title>
<meta name="description" content="Suoratuhkaus {city_ssa}. Kiinteä palvelumaksu {690} €, krematorion maksu erikseen. Lähin krematorio: {krema_name} ({road_km} km). Arviohinta yhteensä {total_range_text}. Pyydä tarjous.">
<link rel="canonical" href="{production_url}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;0,600;1,300;1,400&family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>{SHARED_CSS}</style>
</head>
<body>

<header class="nav">
  <div class="nav-in">
    <a href="/suoratuhkaus/" class="logo">
      <div>
        <span class="logo-main">Suoratuhkaus</span>
        <span class="logo-sub">Koko Suomessa</span>
      </div>
    </a>
    <div style="display:flex;gap:8px;align-items:center">
      <a href="/suoratuhkaus/" class="nav-back">&larr; Etusivulle</a>
      <a href="/suoratuhkaus/#yhteystiedot" class="nav-cta">Ota yhteyttä</a>
    </div>
  </div>
</header>

<section class="hero">
  <div class="hero-in">
    <div>
      <p class="hero-ey">Suoratuhkaus &nbsp;&middot;&nbsp; {city} &nbsp;&middot;&nbsp; Avoin hinnoittelu</p>
      <h1 class="hero-h1">Suoratuhkaus<em>{city_ssa}</em></h1>
      <p class="hero-p">Hoidamme suoratuhkauksen {city_ssa} ja lähikunnissa. Palvelumaksumme on kiinteä. Krematorion maksu ja mahdolliset kuljetuskulut kerrotaan avoimesti ennen kuin mitään sovitaan.</p>
      <div class="hero-btns">
        <a href="/suoratuhkaus/#yhteystiedot" class="btn-t">Pyydä tarjous &rarr;</a>
        <a href="tel:+358800000000" class="btn-w">Soita 0800 000 000</a>
      </div>
    </div>
    <div class="hero-card">
      <div class="hc-head">Hinta-arvio &mdash; {city}</div>
      <div class="hc-row">
        <div>
          <div class="hc-label">Palvelumaksu (kiinteä)</div>
        </div>
        <div>
          <div class="hc-val">690 &euro;</div>
          <div class="hc-sub">Perus-paketti</div>
        </div>
      </div>
      <div class="hc-row">
        <div>
          <div class="hc-label">Krematorio</div>
          <div style="font-size:12px;color:rgba(255,255,255,.4);margin-top:2px">{krema_name} &middot; {road_km} km</div>
        </div>
        <div>
          <div class="hc-val">300&ndash;600 &euro;</div>
          <div class="hc-sub">Paikkakunnasta riippuen</div>
        </div>
      </div>{surcharge_row}
      <div class="hc-note">
        <strong>Yhteensä arviolta {total_range_text}</strong><br>
        Tarkka tarjous pyydettäessä &mdash; ilmaiseksi<br>
        <a href="/suoratuhkaus/#laske" style="color:var(--terra-l)">Laske tarkemmin &darr;</a>
      </div>
    </div>
  </div>
</section>

<div class="trust">
  <div class="trust-in">
    <div class="ti"><div class="ti-dot"></div>Palvelemme {city_ssa}</div>
    <div class="ti"><div class="ti-dot"></div>24/7 päivystys</div>
    <div class="ti"><div class="ti-dot"></div>Kaikki kulut kerrotaan etukäteen</div>
    <div class="ti"><div class="ti-dot"></div>Lähin krematorio: {krema_name} ({road_km} km)</div>
  </div>
</div>

<section class="info-sect">
  <div class="wrap">
    <div class="info-grid">
      <div>
        <p class="eyebrow eyebrow-s">Mikä on suoratuhkaus?</p>
        <h2 class="sec-h2">Yksinkertainen hyvästijättö {city_ssa}</h2>
        <div>
          <p class="sec-p">Suoratuhkaus tarkoittaa, että vainaja tuhkataan ilman etukäteistä siunaustilaisuutta. Se on kasvava, arvokas vaihtoehto perinteiselle hautaukselle.</p>
          <p class="sec-p" style="margin-top:12px">Hoidamme kaiken: haemme vainajan, hoidamme lupa-asiat, kuljetamme krematoriolle ({krema_name}) ja toimitamme tuhkat perheelle. Teidän ei tarvitse huolehtia mistään käytännön asiasta.</p>
          <p class="sec-p" style="margin-top:12px">Palvelemme {city_ssa} ja kaikissa lähikunnissa. Muistotilaisuuden voi järjestää erikseen, milloin perheelle sopii.</p>
        </div>
      </div>
      <div class="info-box">
        <div class="ib-row">
          <span class="ib-label">Kaupunki</span>
          <span class="ib-val">{city}</span>
        </div>
        <div class="ib-row">
          <span class="ib-label">Lähin krematorio</span>
          <span class="ib-val">{krema_name}<small>{road_km} km (arvio tieajosta)</small></span>
        </div>
        <div class="ib-row">
          <span class="ib-label">Palvelumaksu (Perus)</span>
          <span class="ib-val">690 &euro;<small>Kiinteä, ei piilokuluja</small></span>
        </div>
        <div class="ib-row">
          <span class="ib-label">Krematorion maksu</span>
          <span class="ib-val">300&ndash;600 &euro;<small>Paikkakunnasta riippuen</small></span>
        </div>
        {"<div class='ib-row'><span class='ib-label'>Kuljetuslisä</span><span class='ib-val'>+" + str(surcharge) + " &euro;<small>Matka " + str(road_km) + " km</small></span></div>" if surcharge > 0 else ""}
        <div class="ib-row">
          <span class="ib-label">Arvioitu kokonaishinta</span>
          <span class="ib-val" style="color:var(--forest)">{total_range_text}</span>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="how-sect">
  <div class="wrap">
    <p class="eyebrow eyebrow-s">Prosessi</p>
    <h2 class="sec-h2">Miten suoratuhkaus toimii {city_ssa}?</h2>
    <div class="how-grid">
      <div class="how-step">
        <div class="how-n">1</div>
        <div class="how-icon">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="2" width="16" height="16" rx="3" stroke="#2a3d2e" stroke-width="1.5"/><path d="M6 10h8M6 7h8M6 13h5" stroke="#2a3d2e" stroke-width="1.5" stroke-linecap="round"/></svg>
        </div>
        <h3>Ota yhteyttä</h3>
        <p>Soita 0800 000 000 tai lähetä yhteydenottopyyntö. Vastaamme ympäri vuorokauden.</p>
      </div>
      <div class="how-step">
        <div class="how-n">2</div>
        <div class="how-icon">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><rect x="2" y="4" width="16" height="13" rx="2" stroke="#2a3d2e" stroke-width="1.5"/><path d="M14 2v4M6 2v4M2 8h16" stroke="#2a3d2e" stroke-width="1.5" stroke-linecap="round"/></svg>
        </div>
        <h3>Saat kirjallisen tarjouksen</h3>
        <p>Tarjous sisältää palvelumaksun, krematorion maksun ja mahdolliset kuljetuskulut. Ei yllätyksiä.</p>
      </div>
      <div class="how-step">
        <div class="how-n">3</div>
        <div class="how-icon">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M4 10h12M10 4l6 6-6 6" stroke="#2a3d2e" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </div>
        <h3>Me hoidamme käytännön</h3>
        <p>Noudamme vainajan {city_ssa}, hoidamme kaikki luvat ja kuljetamme krematoriolle ({krema_name}).</p>
      </div>
      <div class="how-step">
        <div class="how-n">4</div>
        <div class="how-icon">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none"><path d="M10 3C10 3 4 7 4 12a6 6 0 0012 0C16 7 10 3 10 3Z" stroke="#2a3d2e" stroke-width="1.5" stroke-linejoin="round"/></svg>
        </div>
        <h3>Tuhkat perheelle</h3>
        <p>Toimitetaan tuhkat postitse tai noudettavissa. Muistohetki on, kun teille sopii.</p>
      </div>
    </div>
  </div>
</section>

<section class="price-sect">
  <div class="wrap">
    <div style="text-align:center;margin-bottom:8px">
      <p class="eyebrow eyebrow-t">Hinnoittelu</p>
      <h2 class="sec-h2">Suoratuhkauksen hinta {city_ssa}</h2>
      <p class="sec-p" style="max-width:540px;margin:0 auto">Kaksi selkeää pakettia. Palvelumaksu on kiinteä. Krematorion maksu ja kuljetuskulut kerrotaan tarjouksessa.</p>
    </div>
    <div class="price-grid">
      <div class="pkg">
        <div class="pkg-name">Perus</div>
        <p style="font-size:13.5px;color:var(--text-m);min-height:36px">Kaikki käytännön asiat hoidettu.</p>
        <div class="pkg-price"><span class="pkg-cur">&euro;</span><span class="pkg-eur">690</span></div>
        <p class="pkg-note">palvelumaksu + krematorio erikseen</p>
        <div class="pkg-rule"></div>
        <ul class="pkg-list">
          <li>Vainajan nouto {city_ssa}</li>
          <li>Kuljetus krematoriolle ({krema_name})</li>
          <li>Krematoriovarauksen hoito</li>
          <li>Kaikki viranomaisasiakirjat</li>
          <li>Tuhkien toimitus perheelle</li>
          <li>24/7 puhelinpalvelu</li>
        </ul>
        <a href="/suoratuhkaus/#yhteystiedot" class="btn-pkg">Valitse Perus &rarr;</a>
      </div>
      <div class="pkg pop">
        <div class="pkg-badge">Suosituin</div>
        <div class="pkg-name">Täydellinen</div>
        <p style="font-size:13.5px;color:var(--text-m);min-height:36px">Uurna ja henkilökohtainen palvelija.</p>
        <div class="pkg-price"><span class="pkg-cur">&euro;</span><span class="pkg-eur">1 090</span></div>
        <p class="pkg-note">palvelumaksu + krematorio erikseen</p>
        <div class="pkg-rule"></div>
        <ul class="pkg-list">
          <li>Kaikki Perus-paketin palvelut</li>
          <li>Laadukas uurna valintasi mukaan</li>
          <li>Aikataulun valinta</li>
          <li>Henkilökohtainen palvelija</li>
          <li>Muistokortti vainajasta</li>
        </ul>
        <a href="/suoratuhkaus/#yhteystiedot" class="btn-pkg">Valitse Täydellinen &rarr;</a>
      </div>
      <div class="krematorio-note">
        <div class="kn-text">
          <strong style="color:var(--forest);font-size:15px;display:block;margin-bottom:4px">Krematorion maksu &mdash; {krema_name}</strong>
          <p>Lähin krematorio on {krema_name} ({road_km} km). Krematorion maksu peritään suoraan krematoriolta ja on tyypillisesti 300&ndash;600 euroa.{f' Kuljetuslisä tästä sijainnista: {surcharge} euroa.' if surcharge > 0 else ''} Kerromme tarkan summan tarjouksessa.</p>
        </div>
        <div class="kn-price">300&ndash;600 &euro;</div>
      </div>
    </div>
    <p style="text-align:center;font-size:13px;color:var(--text-l);margin-top:20px;line-height:1.8">
      Kaikki hinnat sis. ALV 25,5&nbsp;%. Perus-paketin arvioitu kokonaishinta {city_ssa}: <strong style="color:var(--forest)">{total_range_text}</strong>
      {f"(sis. {surcharge} € kuljetuslisä)" if surcharge > 0 else ""}
    </p>
  </div>
</section>

<div class="cta-sect">
  <h2>Palvelemme {city_ssa}<em>ympäri vuorokauden</em></h2>
  <p>Yhteydenottoon ei tarvita erityistä syytä. Voit ottaa yhteyttä etukäteen tai juuri nyt.</p>
  <div class="cta-btns">
    <a href="/suoratuhkaus/#yhteystiedot" class="btn-t">Pyydä tarjous &rarr;</a>
    <a href="/suoratuhkaus/#perunkirjoitus" class="btn-w">Etä perunkirjoitus 595 &euro;</a>
  </div>
  <a href="tel:+358800000000" class="cta-phone">0800 000 000</a>
  <p class="cta-note">Päivystys ympäri vuorokauden &middot; puhelu maksuton</p>
</div>

<div class="nearby">
  <div class="wrap">
    <h3>Palvelemme myös lähikunnissa</h3>
    <div class="nearby-links">
      {nearby_links}
      <a href="/suoratuhkaus/" class="nb-link" style="background:var(--forest);color:#fff;border-color:var(--forest)">Kaikki kunnat &rarr;</a>
    </div>
  </div>
</div>

<footer class="ftr">
  <div class="ftr-in">
    <div class="ftr-top">
      <div>
        <div class="ftr-brand">Suoratuhkaus</div>
        <div class="ftr-sub">Koko Suomessa</div>
        <p class="ftr-p">Selkeä, rehellinen suoratuhkauspalvelu. Palvelemme {city_ssa} ja kaikissa muissa Suomen kunnissa.</p>
      </div>
      <div class="ftr-col">
        <h4>Palvelut</h4>
        <a href="/suoratuhkaus/#paketit">Perus-paketti</a>
        <a href="/suoratuhkaus/#paketit">Täydellinen-paketti</a>
        <a href="/suoratuhkaus/#perunkirjoitus">Etä perunkirjoitus</a>
        <a href="/suoratuhkaus/#paketit">Muistotilaisuus</a>
      </div>
      <div class="ftr-col">
        <h4>Yhteystiedot</h4>
        <a href="tel:+358800000000">0800 000 000</a>
        <a href="mailto:info@suoratuhkaus.fi">info@suoratuhkaus.fi</a>
        <a href="/suoratuhkaus/#yhteystiedot">Yhteydenottolomake</a>
        <a href="/suoratuhkaus/">Etusivu</a>
      </div>
    </div>
    <div class="ftr-bot">
      <span>&copy; 2026 Suoratuhkaus &mdash; {city}</span>
      <span>Tietosuojaseloste</span>
    </div>
  </div>
</footer>

<a href="tel:+358800000000" class="sph">
  <svg width="14" height="14" viewBox="0 0 14 14" fill="none"><path d="M12.5 9.5v1.5a1 1 0 01-1.09.998A9.985 9.985 0 011 1.59 1 1 0 012 .5h1.5a1 1 0 011 .877c.1.773.328 1.527.676 2.226a1 1 0 01-.225 1.12l-.751.751a8 8 0 004.23 4.23l.847-.75a1 1 0 011.12-.225c.7.348 1.453.576 2.226.676A1 1 0 0112.5 9.5z" stroke="white" stroke-width="1.2" fill="none"/></svg>
  Soita
</a>

</body>
</html>"""


# ── GENERATE ────────────────────────────────────────────────────────────────

out_dir = '/home/node/.openclaw/workspace/suoratuhkaus/kaupungit'
os.makedirs(out_dir, exist_ok=True)

sheet_rows = [["Kaupunki","Slug","Tuotanto-URL","Preview-URL","Lähin krematorio","Matka km","Kuljetuslisä €","Hinta-arvio (Perus)","Tiedosto"]]

cities_sorted = sorted(KUNNAT.keys())
total = len(cities_sorted)
print(f"Generoidaan {total} kaupunkisivua...")

for i, city in enumerate(cities_sorted, 1):
    lat, lng = KUNNAT[city]
    krema, road_km, surcharge = nearest_krematorio(lat, lng)
    nbr = nearby_cities(city, lat, lng, n=8)
    slug = slugify(city)
    lo, hi = price_range(surcharge)
    price_range_str = f"{lo}–{hi} €"

    html = html_page(city, slug, lat, lng, krema, road_km, surcharge, nbr)
    fname = f"suoratuhkaus-{slug}.html"
    fpath = os.path.join(out_dir, fname)
    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    prod_url  = f"https://suoratuhkaus.fi/suoratuhkaus-{slug}/"
    prev_url  = f"https://authorized-simultaneously-divine-affairs.trycloudflare.com/suoratuhkaus/kaupungit/{fname}"

    sheet_rows.append([city, slug, prod_url, prev_url, krema, road_km, surcharge, price_range_str, fname])

    if i % 50 == 0 or i == total:
        print(f"  {i}/{total} valmis")

print(f"Kaikki {total} HTML-tiedostoa kirjoitettu.")

# ── GOOGLE DRIVE KANSIO ──────────────────────────────────────────────────────

print("\nLuodaan Google Drive -kansio 'Suoratuhkaus.fi'...")
folder_meta = {
    'name': 'Suoratuhkaus.fi',
    'mimeType': 'application/vnd.google-apps.folder'
}
folder = drive.files().create(body=folder_meta, fields='id,name').execute()
folder_id = folder['id']
print(f"Kansio luotu: {folder_id}")

# Jaa kansio molemmille
for email in ['mpasanen@gmail.com', 'epahonkanen@gmail.com']:
    drive.permissions().create(
        fileId=folder_id,
        body={'type':'user','role':'writer','emailAddress':email},
        sendNotificationEmail=True
    ).execute()
    print(f"Kansio jaettu: {email}")

# ── SIIRRÄ TOIMINTAOHJE KANSIOON ─────────────────────────────────────────────

print("\nSiirretään toimintaohje kansioon...")
with open('/home/node/.openclaw/workspace/google_ids.json') as f:
    ids = json.load(f)
doc_id = ids.get('suoratuhkaus_toimintaohje_doc_id')
if doc_id:
    # Hae nykyinen vanhempi
    current = drive.files().get(fileId=doc_id, fields='parents').execute()
    prev_parents = ','.join(current.get('parents', []))
    drive.files().update(
        fileId=doc_id,
        addParents=folder_id,
        removeParents=prev_parents,
        fields='id, parents'
    ).execute()
    print(f"Toimintaohje siirretty kansioon.")
else:
    print("Toimintaohje-ID ei löydy — ohitetaan.")

# ── GOOGLE SHEET LINKEILLÄ ───────────────────────────────────────────────────

print("\nLuodaan Google Sheet 'Suoratuhkaus.fi — Kaupunkisivut'...")
ss = sheets.spreadsheets().create(body={
    'properties': {'title': 'Suoratuhkaus.fi — Kaupunkisivut'},
    'sheets': [{'properties': {'title': 'Linkit'}}]
}).execute()
ss_id = ss['spreadsheetId']
print(f"Sheet ID: {ss_id}")

# Kirjoita data
sheets.spreadsheets().values().update(
    spreadsheetId=ss_id,
    range='Linkit!A1',
    valueInputOption='RAW',
    body={'values': sheet_rows}
).execute()

# Muotoilu: otsikkorivi bold + freeze + leveys
fmt_requests = [
    # Bold otsikot
    {"repeatCell": {
        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True}, "backgroundColor": {"red":0.165,"green":0.239,"blue":0.18}}},
        "fields": "userEnteredFormat(textFormat,backgroundColor)"
    }},
    # Otsikkotekstin väri valkoiseksi
    {"repeatCell": {
        "range": {"sheetId": 0, "startRowIndex": 0, "endRowIndex": 1},
        "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "foregroundColor": {"red":1,"green":1,"blue":1}}}},
        "fields": "userEnteredFormat.textFormat"
    }},
    # Freeze ensimmäinen rivi
    {"updateSheetProperties": {
        "properties": {"sheetId": 0, "gridProperties": {"frozenRowCount": 1}},
        "fields": "gridProperties.frozenRowCount"
    }},
    # Sarakeleveydet
    {"updateDimensionProperties": {
        "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
        "properties": {"pixelSize": 160}, "fields": "pixelSize"
    }},
    {"updateDimensionProperties": {
        "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 4},
        "properties": {"pixelSize": 380}, "fields": "pixelSize"
    }},
    {"updateDimensionProperties": {
        "range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
        "properties": {"pixelSize": 160}, "fields": "pixelSize"
    }},
]
sheets.spreadsheets().batchUpdate(
    spreadsheetId=ss_id,
    body={'requests': fmt_requests}
).execute()

# Hyperlinkit C- ja D-sarakkeisiin
link_updates = []
for row_i, row in enumerate(sheet_rows[1:], start=2):
    prod_url = row[2]
    prev_url = row[3]
    # C-sarake (index 2): tuotanto URL
    link_updates.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"formulaValue": f'=HYPERLINK("{prod_url}","{prod_url}")'}}]}],
            "fields": "userEnteredValue",
            "range": {"sheetId": 0, "startRowIndex": row_i - 1, "endRowIndex": row_i, "startColumnIndex": 2, "endColumnIndex": 3}
        }
    })
    # D-sarake (index 3): preview URL
    link_updates.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"formulaValue": f'=HYPERLINK("{prev_url}","Esikatselu")'}}]}],
            "fields": "userEnteredValue",
            "range": {"sheetId": 0, "startRowIndex": row_i - 1, "endRowIndex": row_i, "startColumnIndex": 3, "endColumnIndex": 4}
        }
    })
    if len(link_updates) >= 100:
        sheets.spreadsheets().batchUpdate(spreadsheetId=ss_id, body={'requests': link_updates}).execute()
        link_updates = []
        time.sleep(0.3)

if link_updates:
    sheets.spreadsheets().batchUpdate(spreadsheetId=ss_id, body={'requests': link_updates}).execute()

print("Hyperlinkkit lisätty.")

# Siirrä Sheet kansioon
drive.files().update(
    fileId=ss_id,
    addParents=folder_id,
    fields='id, parents'
).execute()

# Jaa Sheet
for email in ['mpasanen@gmail.com', 'epahonkanen@gmail.com']:
    drive.permissions().create(
        fileId=ss_id,
        body={'type':'user','role':'writer','emailAddress':email},
        sendNotificationEmail=True
    ).execute()

# Tallenna ID:t
ids['suoratuhkaus_kaupungit_sheet_id'] = ss_id
ids['suoratuhkaus_drive_folder_id'] = folder_id
with open('/home/node/.openclaw/workspace/google_ids.json', 'w') as f:
    json.dump(ids, f, indent=2)

print(f"""
=== VALMIS ===
HTML-sivuja generoitu: {total}
Google Drive -kansio: https://drive.google.com/drive/folders/{folder_id}
Google Sheet: https://docs.google.com/spreadsheets/d/{ss_id}
Toimintaohje: https://docs.google.com/document/d/{doc_id}

Kaikki jaettu: mpasanen@gmail.com + epahonkanen@gmail.com
""")
