import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('16WGnLuUGxalfNEFND-YUfplhXIZMxJ1zzkESc3ISgn4')
fulldata = sheet.worksheet('main')
user_data = sheet.worksheet('users')


def load_race(race_num):
    import leaderboards
    global fulldata
    fulldata = sheet.worksheet('main')
    if race_num == fulldata.col_count:
        fulldata.add_cols(1)
    sheet.worksheet('main')
    batch_size = 100
    fulldata.update_cell(1, race_num + 1, str(race_num))
    lb = leaderboards.get_api_lb(race_num)
    for i in range(0, len(lb), batch_size):
        partial = fulldata.range(i + 2, race_num + 1, i + batch_size + 1, race_num + 1)
        for index, cell in enumerate(partial):
            cell.value = lb[i:i + batch_size][index]
        fulldata.update_cells(partial)
    return True
