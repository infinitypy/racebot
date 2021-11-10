import gspread
from oauth2client.service_account import ServiceAccountCredentials

import leaderboard

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('16WGnLuUGxalfNEFND-YUfplhXIZMxJ1zzkESc3ISgn4')
fulldata = sheet.worksheet('main')
user_data = sheet.worksheet('users')

assoc_ids = user_data.col_values(2)
assoc_players = user_data.col_values(3)


def load_race(race_num):
    global fulldata
    #fulldata = sheet.worksheet('main')
    if race_num < fulldata.col_count:
        return False
    sheet.worksheet('main')
    fulldata.add_cols(1)
    batch_size = 100
    fulldata.update_cell(1, race_num + 1, str(race_num))
    lb = leaderboard.get_api_lb(race_num)
    for i in range(0, len(lb), batch_size):
        partial = fulldata.range(i + 2, race_num + 1, i + batch_size + 1, race_num + 1)
        for index, cell in enumerate(partial):
            cell.value = lb[i:i + batch_size][index]
        fulldata.update_cells(partial)
    return True


def load_all_users():
    unique_ids = set()
    for race_lb in leaderboard.full_data:
        for entry in race_lb:
            if entry:
                unique_ids.add(entry[0:entry.index(',')])
    unique_ids = list(unique_ids)
    batch_size = 200
    for i in range(0, len(unique_ids), batch_size):
        partial = user_data.range(i + 2, 2, i + batch_size + 1, 2)
        for index, cell in enumerate(partial):
            if i + index >= len(unique_ids):
                break
            cell.value = unique_ids[i + index]
        user_data.update_cells(partial)


def load_nicks(start):
    import time
    batch_size = 10
    while True:
        try:
            partial = user_data.range(start, 2, start + batch_size - 1, 3)
        except Exception:
            time.sleep(5)
            continue
        for i in range(0, batch_size * 2, 2):
            nicks = leaderboard.get_nicks(partial[i].value)
            if not nicks:
                continue
            else:
                most_used = nicks[0][0]
                max_use = nicks[0][1]
                for entry in nicks[1:]:
                    if entry[1] == max_use:
                        most_used += ',' + entry[0]
                    else:
                        break
            partial[i + 1].value = most_used
        user_data.update_cells(partial)
        start += batch_size
