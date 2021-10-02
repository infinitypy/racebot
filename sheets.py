import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open_by_key("1iG4mtopJVlF7g3gv6sNrYspyonSQGSHuDOb-QMNVnPc")

worksheet = sheet.worksheet("raceinfo")



row = int(input())
col = 2
cell = worksheet.cell(row+1,col).value
print(cell)