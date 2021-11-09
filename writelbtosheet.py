import gspread
from oauth2client.service_account import ServiceAccountCredentials

import sheets
import leaderboard

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('16WGnLuUGxalfNEFND-YUfplhXIZMxJ1zzkESc3ISgn4')
fulldata = sheet.worksheet('main')

all_races = {}
all_ids = sheets.race_info.col_values(3)[1:]


def load_race(race_num):
    global fulldata
    fulldata = sheet.worksheet('main')
    if race_num < fulldata.col_count:
        return False
    sheet.worksheet('main')
    fulldata.add_cols(1)
    batch_size = 100
    fulldata.update_cell(1, race_num + 1, str(race_num))
    lb = leaderboard.get_api_lb(race_num)
    for j in range(0, len(lb), batch_size):
        partial = fulldata.range(j + 2, race_num + 1, j + batch_size + 1, race_num + 1)
        for index, cell in enumerate(partial):
            cell.value = lb[j:j + batch_size][index]
        fulldata.update_cells(partial)
    return True
