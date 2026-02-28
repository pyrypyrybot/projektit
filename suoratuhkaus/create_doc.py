#!/usr/bin/env python3
"""
Luo Suoratuhkaus.fi toimintaohje Google Docsiin ja jaa epahonkanen@gmail.com
"""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json, time

SCOPES = [
    'https://www.googleapis.com/auth/gmail.modify',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/documents'
]

with open('/home/node/.openclaw/workspace/google_token.json') as f:
    creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)

docs  = build('docs',  'v1', credentials=creds)
drive = build('drive', 'v3', credentials=creds)

# --- Luo dokumentti ---
doc = docs.documents().create(body={'title': 'Suoratuhkaus.fi — Toimintaohje v1.0'}).execute()
doc_id = doc['documentId']
print(f"Dokumentti luotu: https://docs.google.com/document/d/{doc_id}")

# --- Jaa käyttäjille ---
for email in ['mpasanen@gmail.com', 'epahonkanen@gmail.com']:
    drive.permissions().create(
        fileId=doc_id,
        body={'type': 'user', 'role': 'writer', 'emailAddress': email},
        sendNotificationEmail=True
    ).execute()
    print(f"Jaettu: {email}")

# --- Helper: lisää teksti ---
def txt(t, style='NORMAL_TEXT', bold=False, italic=False, color=None, size=None, indent=0):
    req = [
        {'insertText': {'location': {'index': 1}, 'text': t + '\n'}},
        {'updateParagraphStyle': {
            'range': {'startIndex': 1, 'endIndex': len(t) + 2},
            'paragraphStyle': {
                'namedStyleType': style,
                'indentFirstLine': {'magnitude': indent, 'unit': 'PT'},
                'indentStart': {'magnitude': indent, 'unit': 'PT'},
            },
            'fields': 'namedStyleType,indentFirstLine,indentStart'
        }}
    ]
    ts = {'bold': bold, 'italic': italic}
    if color:
        ts['foregroundColor'] = {'color': {'rgbColor': color}}
    if size:
        ts['fontSize'] = {'magnitude': size, 'unit': 'PT'}
    if bold or italic or color or size:
        req.append({'updateTextStyle': {
            'range': {'startIndex': 1, 'endIndex': len(t) + 1},
            'textStyle': ts,
            'fields': ','.join(ts.keys())
        }})
    return req

def human_note(text):
    """Punainen ihminen-vaatii-huomio-kenttä"""
    full = f'[IHMINEN VAATII] {text}'
    return txt(full, bold=True, color={'red': 0.8, 'green': 0.1, 'blue': 0.1}, size=11)

# Rakennetaan dokumentti takaperin (insertText at index 1 = aina alkuun)
# Joten lisätään viimeiset kappaleet ensin

sections = []

# FOOTER / Päiväys
sections.append(txt('Laadittu: 24.2.2025  |  Versio 1.0  |  Luottamuksellinen — vain sisäiseen käyttöön', italic=True, color={'red': 0.5, 'green': 0.5, 'blue': 0.5}, size=9))
sections.append(txt(''))

# 8. LAADUNVARMISTUS
sections.append(txt('8. Laadunvarmistus ja seuranta', style='HEADING_2'))
sections.append(txt('8.1 KPI-seuranta (kuukausittain)'))
sections.append(txt('• Vasteaika ensimmäiseen yhteydenottoon (tavoite < 5 min ark., < 30 min viikonloput)'))
sections.append(txt('• Luottotarkistuksen hyväksymisaste'))
sections.append(txt('• Ennakkomaksujen keräysaste'))
sections.append(txt('• Asiakastyytyväisyys (NPS-kysely toimituksen jälkeen, automaattinen)'))
sections.append(txt('• Perunkirjoitus: läpimenoaika tilauksesta valmistuneeseen perukirjaan (tavoite 7 arkipäivää)'))
sections.append(txt(''))
sections.append(txt('8.2 Reklamaatioiden käsittely'))
sections.append(human_note('Kaikki reklamaatiot käsitellään henkilökohtaisesti. Vastaus 24 h. Eskaloi tarvittaessa vastuuhenkilölle.'))
sections.append(txt(''))
sections.append(txt('8.3 Dokumenttien säilytys'))
sections.append(txt('• Perunkirjoitusasiakirjat: 10 vuotta (verottajan vaatimus)'))
sections.append(txt('• Suoratuhkausasiakirjat: 5 vuotta'))
sections.append(txt('• Luottotietoraportti: 6 kuukautta tai sopimuksen päättymiseen'))
sections.append(txt(''))

# 7. MUISTOTILAISUUS
sections.append(txt('7. Muistotilaisuuden järjestely (lisäpalvelu)', style='HEADING_2'))
sections.append(txt('Muistotilaisuus on aina erillinen, asiakkaan haluamaan ajankohtaan järjestetty tilaisuus. Se EI sisälly perus- tai täydellinen-paketteihin.'))
sections.append(txt(''))
sections.append(txt('Vaihe 1: Kyselyyn vastaaminen (AI)'))
sections.append(txt('AI lähettää automaattisesti tietopaketin muistotilaisuusvaihtoehdoista ja pyytää toiveet: ajankohta, paikka, henkilömäärä, erikoistoiveet.'))
sections.append(txt(''))
sections.append(txt('Vaihe 2: Tarjous'))
sections.append(human_note('Muistotilaisuuden tarjous tehdään aina manuaalisesti, koska hinta riippuu tilauksesta. Lähetä tarjous 24 h yhteydenotosta.'))
sections.append(txt(''))
sections.append(txt('Vaihe 3: Järjestely'))
sections.append(human_note('Tila, kukkia, musiikki, pappi/muistopuhuja — kaikki sovitaan henkilökohtaisesti. Koordinoi erikoistoimittajien kanssa.'))
sections.append(txt(''))

# 6. ETÄ PERUNKIRJOITUS
sections.append(txt('6. Etä perunkirjoitus — Palvelupolku', style='HEADING_2'))
sections.append(txt('Hinta: 595 € (sis. ALV 25,5 %). Ennakkomaksu 100 % ennen työn aloitusta.'))
sections.append(txt(''))
sections.append(txt('Mitä palvelu sisältää:'))
sections.append(txt('• Perukirjan laadinta toimitetuista asiakirjoista'))
sections.append(txt('• Perunkirjoitustilaisuuden järjestäminen etäyhteyden kautta (Teams/Zoom)'))
sections.append(txt('• Valmiin perukirjan toimitus sähköisesti (allekirjoitettu) ja postitse'))
sections.append(txt('• Neuvonta verottajan ilmoittamisessa'))
sections.append(txt(''))
sections.append(txt('Askel 1 — Yhteydenotto (AI hoitaa):'))
sections.append(txt('AI kerää lomakkeelta tai sähköpostista: vainajan nimi, kuolinpäivä, kotipaikka, perilliset (nimet, syntymäajat, osoitteet), arvioitu omaisuus. AI lähettää automaattisen vahvistuksen ja asiakirjalistan.'))
sections.append(txt(''))
sections.append(txt('Askel 2 — Ennakkomaksulasku (automaatti):'))
sections.append(txt('Järjestelmä lähettää 595 € laskun automaattisesti (Stripe / Netvisor). Työ alkaa vasta maksun jälkeen. Maksulinkki on voimassa 7 päivää.'))
sections.append(txt(''))
sections.append(txt('Askel 3 — Asiakirjojen toimitus (asiakas):'))
sections.append(txt('Asiakas toimittaa asiakirjat JOKO:'))
sections.append(txt('  A) Turvasähköpostilla: secure@suoratuhkaus.fi (Zecure/Trustm8-palvelu)', indent=20))
sections.append(txt('  B) Turvalliseen tietopankkiin: asiakaskohtainen linkki järjestelmästä', indent=20))
sections.append(txt(''))
sections.append(txt('Vaaditut asiakirjat (lähetetään automaattinen tarkistuslista):'))
sections.append(txt('  • Vainajan sukuselvitys (virkatodistukset kaikista seurakunnista / DVV)', indent=20))
sections.append(txt('  • Virkatodistukset kaikista perillisistä', indent=20))
sections.append(txt('  • Testamentti (jos on)', indent=20))
sections.append(txt('  • Avioehtosopimus (jos on)', indent=20))
sections.append(txt('  • Pankkitiliotteet kuolinpäivältä (kaikki tilit)', indent=20))
sections.append(txt('  • Kiinteistöjen lainhuutotodistukset / kauppakirjat', indent=20))
sections.append(txt('  • Ajoneuvojen rekisteriotteet', indent=20))
sections.append(txt('  • Eläke- ja henkivakuutustodistukset', indent=20))
sections.append(txt('  • Velkojen todisteet (lainasopimukset, saldot)', indent=20))
sections.append(txt(''))
sections.append(human_note('Asiakirjojen tarkistus: Palveluneuvojan tulee käydä läpi toimitetut dokumentit 1 arkipäivän sisällä. Jos asiakirjoja puuttuu, lähetä automaattinen muistutus (AI), mutta tee henkilökohtainen yhteydenotto mikäli asia on kiireellinen tai puuttuu oleellista.'))
sections.append(txt(''))
sections.append(txt('Askel 4 — Perukirjan laadinta:'))
sections.append(human_note('Perukirja laaditaan aina koulutetun henkilön toimesta. Varmista, että laadinnan tekee oikeudellisesti pätevä henkilö. Käytä perukirjapohjaa (Liite A) ja tarkista jokainen kohta.'))
sections.append(txt(''))
sections.append(txt('Askel 5 — Perunkirjoitustilaisuus (etäyhteys):'))
sections.append(human_note('Perunkirjoitustilaisuus pidetään Teams/Zoom-kokouksena. Lähetä kutsu automaattisesti kalenterista. Tilaisuudessa tulee olla läsnä vähintään kaksi uskottua miestä. Tallenna tilaisuus (suostumus pyydettävä). Tavoiteaika: 7 arkipäivää asiakirjojen vastaanottamisesta.'))
sections.append(txt(''))
sections.append(txt('Askel 6 — Valmis perukirja:'))
sections.append(txt('Perukirja allekirjoitetaan sähköisesti (Dokobit/Visma Sign). AI lähettää automaattisesti:'))
sections.append(txt('  • Digitaalisen kopion sähköpostilla', indent=20))
sections.append(txt('  • Tilauksen fyysisestä kopiosta postitse (lisätilaus)', indent=20))
sections.append(txt('  • Ohjeet verottajalle ilmoittamiseen (DVV, OmaVero)', indent=20))
sections.append(txt(''))
sections.append(txt('Askel 7 — Arkistointi:'))
sections.append(txt('Asiakirjat arkistoidaan salattuun tietopankkiin 10 vuodeksi. Asiakas saa pysyvän pääsyn omiin asiakirjoihinsa.'))
sections.append(txt(''))

# 5. SUORATUHKAUS
sections.append(txt('5. Suoratuhkaus — Palvelupolku', style='HEADING_2'))
sections.append(txt(''))
sections.append(txt('Askel 1 — Yhteydenotto (AI hoitaa kanavasta riippuen):'))
sections.append(txt('• Puhelin: ihminen vastaa 24/7 (ei automatisoida)'))
sections.append(txt('• Web-lomake: AI lähettää välittömän vahvistuksen + FAQ-paketin + hintaestimaatin'))
sections.append(txt('• WhatsApp / sähköposti: AI käsittelee yhteydenoton, kerää perustiedot (paikkakunta, paketti, kiireellisyys)'))
sections.append(txt(''))
sections.append(human_note('PUHELIN: Puhelinpäivystys ei automatisoida. Ihmisen on vastattava. Iltaisin ja viikonloppuisin järjestä päivystysvuoro. Kirjaa puhelun tiedot CRM-järjestelmään välittömästi.'))
sections.append(txt(''))
sections.append(txt('Askel 2 — Tarjouslaskenta (automaatti):'))
sections.append(txt('Järjestelmä laskee automaattisesti: palvelumaksu (690/1090 €) + krematorion maksu (300–600 € paikkakunnasta) + mahdollinen kuljetuslisä. Tarjous lähetetään sähköpostilla ja WhatsAppilla.'))
sections.append(txt(''))
sections.append(txt('Askel 3 — Luottotarkistus tai ennakkomaksu:'))
sections.append(txt('Katso kohta 4 (Luottotarkistus).'))
sections.append(txt(''))
sections.append(txt('Askel 4 — Tilauksen vahvistus:'))
sections.append(human_note('Ennen kuin mitään käytännön toimenpiteitä aloitetaan, vastuuhenkilön TÄYTYY vahvistaa tilaus. Tarkista: luottotarkistus OK tai ennakkomaksu vastaanotettu, sopimus allekirjoitettu (Dokobit), tiedot CRM:ssä.'))
sections.append(txt(''))
sections.append(txt('Askel 5 — Vainajan nouto:'))
sections.append(human_note('Noudon aikatauluttaa henkilökunta. Ilmoita omaisille aikataulusta tekstiviestillä/WhatsAppilla (automaattinen viesti lähtee järjestelmästä). Tarkista noutopaikka ja erityistarpeet.'))
sections.append(txt(''))
sections.append(txt('Askel 6 — Kuljetus ja tuhkaus:'))
sections.append(txt('Automaattiset tilapäivitykset omaisille:'))
sections.append(txt('  • "Vainaja noudettu" — lähetetään automaattisesti kun nouto kirjataan', indent=20))
sections.append(txt('  • "Vainaja toimitettu krematoriolle" — kirjaus CRM:ään', indent=20))
sections.append(txt('  • "Tuhkaus suoritettu" — automaattinen ilmoitus omaisille', indent=20))
sections.append(txt(''))
sections.append(txt('Askel 7 — Tuhkien toimitus:'))
sections.append(txt('AI lähettää automaattisen ilmoituksen toimituksesta + seurantakoodin. Perhe valitsee toimitustavan lomakkeella (posti/nouto).'))
sections.append(txt(''))
sections.append(txt('Askel 8 — Jälkihoito (AI hoitaa):'))
sections.append(txt('3 päivää toimituksen jälkeen: automaattinen kiitosviesti + NPS-kysely + muistotilaisuuden esittely.'))
sections.append(txt(''))

# 4. LUOTTOTARKISTUS JA ENNAKKOMAKSU
sections.append(txt('4. Luottotarkistus ja ennakkomaksu', style='HEADING_2'))
sections.append(txt('Jokainen asiakas joko läpäisee luottotarkistuksen TAI maksaa ennakkomaksun ennen palvelun aloittamista. Poikkeuksia ei tehdä.'))
sections.append(txt(''))
sections.append(txt('Vaihtoehto A: Luottotarkistus'))
sections.append(txt('1. Asiakas antaa suostumuksen luottotietojen tarkistamiseen (digitaalinen allekirjoitus lomakkeella)'))
sections.append(txt('2. Järjestelmä tekee automaattisen tarkistuksen: Suomen Asiakastieto Oy (Alusta-rajapinta) tai Creditsafe Finland'))
sections.append(txt('3. Tulos:'))
sections.append(txt('   • Hyväksytty → automaattinen vahvistusviesti, palvelu etenee', indent=20))
sections.append(txt('   • Hylätty tai rajoituksia → katso alla', indent=20))
sections.append(human_note('Jos luottotarkistus hylätään tai asiakkaalla on maksuhäiriöitä: ÄLÄ jatka palvelua automaattisesti. Palveluneuvojan tulee ottaa yhteyttä asiakkaaseen henkilökohtaisesti ja arvioida tilanne. Vaihtoehto: 100 % ennakkomaksu ennen palvelua.'))
sections.append(txt(''))
sections.append(txt('Vaihtoehto B: Ennakkomaksu'))
sections.append(txt('Jos asiakas ei anna lupaa luottotarkistukseen tai luottotiedot ovat huonot:'))
sections.append(txt('• Suoratuhkaus: 50 % ennakkomaksu tilauksen yhteydessä, loppumaksu tuhkien toimituksen yhteydessä'))
sections.append(txt('• Etä perunkirjoitus: 100 % ennakkomaksu ennen työn aloittamista'))
sections.append(txt('• Maksuvälineet: Korttilinkin (Stripe) tai verkkolaskun kautta'))
sections.append(txt(''))
sections.append(human_note('Maksuihin liittyvät poikkeustilanteet (kuolemantapaus, kriisitilanne): Palveluneuvojan harkintavalta. Kirjaa aina perustelut CRM:ään ja informoi vastuuhenkilöä.'))
sections.append(txt(''))

# 3. AI-ASIAKASPALVELU
sections.append(txt('3. Asiakaspalvelun automaatio — AI:n rooli', style='HEADING_2'))
sections.append(txt(''))
sections.append(txt('AI HOITAA ITSENÄISESTI (ei vaadi ihmistä):'))
sections.append(txt('• Yhteydenottopyyntöihin vastaaminen (web-lomake, sähköposti, WhatsApp) — välitön vahvistus'))
sections.append(txt('• Hintaestimaatin laskeminen ja lähettäminen'))
sections.append(txt('• FAQ-kysymyksiin vastaaminen (ks. liite: AI-vastaukset)'))
sections.append(txt('• Tilapäivitykset asiakkaille (nouto, kuljetus, tuhkaus, toimitus)'))
sections.append(txt('• Asiakirjojen pyytäminen ja tarkistuslistan lähettäminen (perunkirjoitus)'))
sections.append(txt('• Muistutukset puuttuvista asiakirjoista'))
sections.append(txt('• Ennakkomaksulaskun lähettäminen (Stripe-linkki)'))
sections.append(txt('• NPS-kysely toimituksen jälkeen'))
sections.append(txt('• Muistotilaisuuden informaatiopaketin lähettäminen'))
sections.append(txt(''))
sections.append(txt('IHMINEN HOITAA AINA:'))
sections.append(human_note('1. Puhelinpäivystys 24/7 — ihminen vastaa puhelimeen'))
sections.append(human_note('2. Tilauksen lopullinen vahvistus ennen palvelun aloittamista'))
sections.append(human_note('3. Vainajan nouto ja käytännön koordinointi'))
sections.append(human_note('4. Luottotarkistuksen poikkeustilanteet'))
sections.append(human_note('5. Muistotilaisuuden tarjous ja järjestely'))
sections.append(human_note('6. Perukirjan laadinta (oikeudellisesti pätevä henkilö)'))
sections.append(human_note('7. Perunkirjoitustilaisuuden vetäminen'))
sections.append(human_note('8. Reklamaatiot'))
sections.append(human_note('9. Erikoistilanteet, kriisit, poikkeukset'))
sections.append(txt(''))
sections.append(txt('AI-vastausajat:'))
sections.append(txt('• Web-lomake: vastaus 2 minuutin sisällä (24/7)'))
sections.append(txt('• Sähköposti: vastaus 15 minuutin sisällä (24/7)'))
sections.append(txt('• WhatsApp: vastaus 5 minuutin sisällä (24/7)'))
sections.append(txt('• Puhelin: ihminen vastaa (ei AI)'))
sections.append(txt(''))

# 2. PALVELUT JA HINNAT
sections.append(txt('2. Palveluvalikoimamme', style='HEADING_2'))
sections.append(txt(''))
sections.append(txt('SUORATUHKAUS', bold=True))
sections.append(txt('• Perus-paketti: 690 € (palvelumaksu) + krematorion maksu 300–600 €'))
sections.append(txt('  → Yhteensä tyypillisesti 990–1 290 €'))
sections.append(txt('• Täydellinen-paketti: 1 090 € (palvelumaksu) + krematorion maksu 300–600 €'))
sections.append(txt('  → Yhteensä tyypillisesti 1 390–1 690 €'))
sections.append(txt('• Muistotilaisuus: hinta sovitaan erikseen'))
sections.append(txt(''))
sections.append(txt('ETÄ PERUNKIRJOITUS', bold=True))
sections.append(txt('• Kiinteä hinta: 595 € (sis. ALV 25,5 %)'))
sections.append(txt('• Sisältää: asiakirjojen käsittely, perukirjan laadinta, etäperunkirjoitustilaisuus, sähköinen toimitus'))
sections.append(txt('• Maksu: 100 % ennakkomaksu ennen työn aloittamista'))
sections.append(txt(''))

# 1. JOHDANTO
sections.append(txt('1. Johdanto ja palvelun tarkoitus', style='HEADING_2'))
sections.append(txt('Tämä toimintaohje kuvaa Suoratuhkaus.fi:n operatiivisen toiminnan prosessit. Tavoitteena on mahdollisimman pitkälle automatisoitu asiakaspalvelupolku, jossa kielimalli (AI) hoitaa toistuvat, matalakynnykseiset tehtävät ja ihminen keskittyy herkkyyttä, ammattitaitoa ja päätöksentekokykyä vaativiin kohtiin.'))
sections.append(txt(''))
sections.append(txt('Periaatteet:'))
sections.append(txt('1. Läpinäkyvä hinnoittelu — asiakas tietää kaikki kulut ennen sopimusta'))
sections.append(txt('2. Nopea vastausaika — AI vastaa 24/7, ihminen tarvittaessa'))
sections.append(txt('3. Luottotarkistus tai ennakkomaksu — poikkeuksitta'))
sections.append(txt('4. Asiakirjojen turvallinen käsittely — kaikki tieto salatusti'))
sections.append(txt('5. Ihmiskontakti kriittisissä kohdissa — ei robotteja suruhetkellä'))
sections.append(txt(''))
sections.append(txt('Yhteystiedot vastuuhenkilöille:'))
sections.append(txt('• Operatiivinen vastuu: [TÄYTÄ NIMI] — [TÄYTÄ PUHELIN]'))
sections.append(txt('• Perunkirjoituspalvelu: [TÄYTÄ NIMI] — [TÄYTÄ PUHELIN]'))
sections.append(txt('• Tekninen ylläpito: info@suoratuhkaus.fi'))
sections.append(txt(''))

# OTSIKKO
sections.append(txt('Suoratuhkaus.fi — Toimintaohje palveluita hoitavalle taholle', style='HEADING_1'))
sections.append(txt('Versio 1.0 | Luottamuksellinen', italic=True, color={'red': 0.4, 'green': 0.4, 'blue': 0.4}))
sections.append(txt(''))

# Suorita kaikki päivitykset
all_requests = []
for section in sections:
    all_requests.extend(section)

# Suorita erissä (max 50 kerrallaan)
batch_size = 50
for i in range(0, len(all_requests), batch_size):
    batch = all_requests[i:i+batch_size]
    docs.documents().batchUpdate(
        documentId=doc_id,
        body={'requests': batch}
    ).execute()
    time.sleep(0.3)
    print(f"Batch {i//batch_size + 1} valmis")

print(f"\nDokumentti valmis!")
print(f"URL: https://docs.google.com/document/d/{doc_id}")
print(f"ID: {doc_id}")

# Tallenna ID
try:
    with open('/home/node/.openclaw/workspace/google_ids.json') as f:
        ids = json.load(f)
except:
    ids = {}
ids['suoratuhkaus_toimintaohje_doc_id'] = doc_id
with open('/home/node/.openclaw/workspace/google_ids.json', 'w') as f:
    json.dump(ids, f, indent=2)
print("ID tallennettu google_ids.json")
