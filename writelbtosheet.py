from json import JSONDecodeError

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
import datetime
import sheets

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('16WGnLuUGxalfNEFND-YUfplhXIZMxJ1zzkESc3ISgn4')
fulldata = sheet.worksheet('main')

all_races = {}
all_ids = sheets.race_info.col_values(3)[1:]


def lb(race_num):
    times = []
    new_times = []
    complete = []

    race_id = all_ids[race_num - 1]
    race_url = 'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_{}.json'\
        .format(race_id)
    try:
        data = requests.get(race_url).json()
    except JSONDecodeError:
        return None
    entries = json.loads(data["data"])['scores']['equal']
    stuff = [(entry['metadata'].split(',')[0], entry['score'], entry['userID']) for entry in entries]

    for i in range(len(stuff)):
        if str(stuff[i][1])[-1] == '9':
            times.append(str(stuff[i][1])[0:-1] + '8')
        else:
            times.append(str(stuff[i][1]))

    for i in range(len(times)):
        new_times.append(str(datetime.timedelta(milliseconds=999999999 - int(times[i])))[3:-3])

    for i in range(len(stuff)):
        complete.append(stuff[i][2] + ',' + stuff[i][0] + ',' + new_times[i])

    return complete


def load_race(race_num):
    leaderboard = lb(race_num)
    if not leaderboard:
        return False
    else:
        if race_num >= fulldata.col_count:
            fulldata.add_cols(race_num - fulldata.col_count + 1)
        batch_size = 100
        fulldata.update_cell(1, race_num + 1, str(race_num))
        for j in range(0, len(leaderboard), batch_size):
            partial = fulldata.range(j + 2, race_num + 1, j + batch_size + 1, race_num + 1)
            for index, cell in enumerate(partial):
                cell.value = leaderboard[j:j + batch_size][index]
            fulldata.update_cells(partial)
        return True
