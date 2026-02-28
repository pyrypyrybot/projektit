#!/usr/bin/env python3
"""Päivittää Google Sheetin D-sarakkeen preview-linkit uudella tunneli-URLilla."""
import json, time
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

TUNNEL = "https://defend-aimed-booth-buy.trycloudflare.com"

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
with open('/home/node/.openclaw/workspace/google_token.json') as f:
    creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)
sheets = build('sheets', 'v4', credentials=creds)

with open('/home/node/.openclaw/workspace/google_ids.json') as f:
    ids = json.load(f)

ss_id = ids['suoratuhkaus_kaupungit_sheet_id']

# Hae sheet ID
ss_info = sheets.spreadsheets().get(spreadsheetId=ss_id).execute()
grid_id = ss_info['sheets'][0]['properties']['sheetId']

# Lue data (B-sarake = slug, I-sarake = tiedostonimi)
result = sheets.spreadsheets().values().get(
    spreadsheetId=ss_id, range='Linkit!A2:I300'
).execute()
rows = result.get('values', [])
print(f"Rivejä: {len(rows)}")

# Rakenna batch-päivitys
updates = []
for row_i, row in enumerate(rows, start=2):
    if len(row) < 9:
        continue
    fname = row[8]  # I = tiedostonimi, esim. suoratuhkaus-helsinki.html
    prev_url = f"{TUNNEL}/suoratuhkaus/kaupungit/{fname}"
    city = row[0]
    updates.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {
                "formulaValue": f'=HYPERLINK("{prev_url}","Esikatselu: {city}")'
            }}]}],
            "fields": "userEnteredValue",
            "range": {
                "sheetId": grid_id,
                "startRowIndex": row_i - 1,
                "endRowIndex": row_i,
                "startColumnIndex": 3,  # D
                "endColumnIndex": 4
            }
        }
    })
    # Päivitä myös C-sarakkeen preview-raw URL
    updates.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"stringValue": prev_url}}]}],
            "fields": "userEnteredValue",
            "range": {
                "sheetId": grid_id,
                "startRowIndex": row_i - 1,
                "endRowIndex": row_i,
                "startColumnIndex": 3,
                "endColumnIndex": 4
            }
        }
    })

# Käytä vain hyperlink-version (joka toinen päällekirjoittaisi)
# → pidetään vain HYPERLINK-formaatti
link_updates = [u for i, u in enumerate(updates) if i % 2 == 0]

# Lähetä erissä
batch = 100
for i in range(0, len(link_updates), batch):
    chunk = link_updates[i:i+batch]
    sheets.spreadsheets().batchUpdate(
        spreadsheetId=ss_id, body={'requests': chunk}
    ).execute()
    print(f"  Päivitetty {min(i+batch, len(link_updates))}/{len(link_updates)}")
    time.sleep(0.3)

print(f"\nKaikki {len(link_updates)} preview-linkkiä päivitetty.")
print(f"Sheet: https://docs.google.com/spreadsheets/d/{ss_id}")
print(f"\nEsimerkkilinkki (Helsinki):")
print(f"{TUNNEL}/suoratuhkaus/kaupungit/tuhkaus-helsinki.html")
print(f"\nEsimerkkilinkki (Rovaniemi):")
print(f"{TUNNEL}/suoratuhkaus/kaupungit/tuhkaus-rovaniemi.html")
print(f"\nEsimerkkilinkki (Utsjoki):")
print(f"{TUNNEL}/suoratuhkaus/kaupungit/tuhkaus-utsjoki.html")
