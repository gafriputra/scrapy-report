import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('bidgear-60e0866538fc.json', scope)
client = gspread.authorize(creds)

sheet = client.open('Coba API GOOGLE').sheet1

cobaku = sheet.get_all_records()
print(cobaku)