#!/usr/bin/env python3
"""Korjaa Sheet-muotoilu ja lisää hyperlinkit."""
import os, math, json, time, re
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive',
]
with open('/home/node/.openclaw/workspace/google_token.json') as f:
    creds = Credentials.from_authorized_user_info(json.load(f), SCOPES)
sheets = build('sheets', 'v4', credentials=creds)
drive  = build('drive',  'v3', credentials=creds)

with open('/home/node/.openclaw/workspace/google_ids.json') as f:
    ids = json.load(f)

ss_id     = ids['suoratuhkaus_kaupungit_sheet_id']
folder_id = ids['suoratuhkaus_drive_folder_id']

print(f"Sheet ID: {ss_id}")

# Hae todellinen sheet (grid) ID
ss_info = sheets.spreadsheets().get(spreadsheetId=ss_id).execute()
real_sheet_id = ss_info['sheets'][0]['properties']['sheetId']
print(f"Todellinen Sheet grid ID: {real_sheet_id}")

# ── Muotoilu ──────────────────────────────────────────────────────────────
fmt_requests = [
    {"repeatCell": {
        "range": {"sheetId": real_sheet_id, "startRowIndex": 0, "endRowIndex": 1},
        "cell": {"userEnteredFormat": {
            "textFormat": {"bold": True, "foregroundColor": {"red":1,"green":1,"blue":1}},
            "backgroundColor": {"red":0.165,"green":0.239,"blue":0.18}
        }},
        "fields": "userEnteredFormat(textFormat,backgroundColor)"
    }},
    {"updateSheetProperties": {
        "properties": {"sheetId": real_sheet_id, "gridProperties": {"frozenRowCount": 1}},
        "fields": "gridProperties.frozenRowCount"
    }},
    {"updateDimensionProperties": {
        "range": {"sheetId": real_sheet_id, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 1},
        "properties": {"pixelSize": 160}, "fields": "pixelSize"
    }},
    {"updateDimensionProperties": {
        "range": {"sheetId": real_sheet_id, "dimension": "COLUMNS", "startIndex": 2, "endIndex": 4},
        "properties": {"pixelSize": 360}, "fields": "pixelSize"
    }},
    {"updateDimensionProperties": {
        "range": {"sheetId": real_sheet_id, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5},
        "properties": {"pixelSize": 160}, "fields": "pixelSize"
    }},
    {"updateDimensionProperties": {
        "range": {"sheetId": real_sheet_id, "dimension": "COLUMNS", "startIndex": 7, "endIndex": 8},
        "properties": {"pixelSize": 160}, "fields": "pixelSize"
    }},
]
sheets.spreadsheets().batchUpdate(
    spreadsheetId=ss_id, body={'requests': fmt_requests}
).execute()
print("Muotoilu OK.")

# ── Hyperlinkit D-sarakkeeseen (esikatselu) ───────────────────────────────
# Lue data ensin
result = sheets.spreadsheets().values().get(
    spreadsheetId=ss_id, range='Linkit!A2:I500'
).execute()
rows = result.get('values', [])

link_updates = []
for row_i, row in enumerate(rows, start=2):
    if len(row) < 9: continue
    prev_url = row[3]  # D-sarake
    link_updates.append({
        "updateCells": {
            "rows": [{"values": [{"userEnteredValue": {"formulaValue": f'=HYPERLINK("{prev_url}","Esikatselu")'}}]}],
            "fields": "userEnteredValue",
            "range": {"sheetId": real_sheet_id,
                      "startRowIndex": row_i - 1, "endRowIndex": row_i,
                      "startColumnIndex": 3, "endColumnIndex": 4}
        }
    })
    if len(link_updates) >= 100:
        sheets.spreadsheets().batchUpdate(spreadsheetId=ss_id, body={'requests': link_updates}).execute()
        link_updates = []
        time.sleep(0.4)
        print(f"  Hyperlinkit: {row_i-1}/{len(rows)}")

if link_updates:
    sheets.spreadsheets().batchUpdate(spreadsheetId=ss_id, body={'requests': link_updates}).execute()

print("Hyperlinkit OK.")

# ── Siirrä Sheet kansioon ─────────────────────────────────────────────────
drive.files().update(
    fileId=ss_id,
    addParents=folder_id,
    fields='id,parents'
).execute()
print("Sheet siirretty kansioon.")

# ── Jaa ──────────────────────────────────────────────────────────────────
for email in ['mpasanen@gmail.com', 'epahonkanen@gmail.com']:
    try:
        drive.permissions().create(
            fileId=ss_id,
            body={'type':'user','role':'writer','emailAddress':email},
            sendNotificationEmail=True
        ).execute()
        print(f"Sheet jaettu: {email}")
    except Exception as e:
        print(f"Jako jo olemassa tai virhe: {email} — {e}")

print(f"""
=== VALMIS ===
Drive-kansio: https://drive.google.com/drive/folders/{folder_id}
Sheet:        https://docs.google.com/spreadsheets/d/{ss_id}
Toimintaohje: https://docs.google.com/document/d/{ids.get('suoratuhkaus_toimintaohje_doc_id')}
""")
