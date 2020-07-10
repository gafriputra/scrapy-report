from pprint import pprint
from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient import discovery

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('bidgear-60e0866538fc.json', scope)
service = discovery.build('sheets', 'v4', credentials=credentials)

list = [["12",2,4,534,"pending"]]
resource = {
  "majorDimension": "ROWS",
  "values": list
}
spreadsheetId = "18XV73kOQoCPvfJQLLSf7lxiItyVIEL3NTLOcLjsatus"
range = "Sheet1!A:A";
service.spreadsheets().values().append(
  spreadsheetId=spreadsheetId,
  range=range,
  body=resource,
  valueInputOption="USER_ENTERED"
).execute()