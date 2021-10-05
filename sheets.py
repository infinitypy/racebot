import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1iG4mtopJVlF7g3gv6sNrYspyonSQGSHuDOb-QMNVnPc')
race_info = sheet.worksheet('raceinfo')
round_info = sheet.worksheet('rounds')


def race(num, display_race_id=None):
    if num == 129 and display_race_id is None:
        return ':corn::tada:'
    else:
        col = 3 if display_race_id is not None else 2
        return race_info.cell(num + 1, col).value


def length(num, abr):
    col = 2 if abr is not None else 1
    return round_info.cell(num + 1, col).value


def rtime(start, end, stime, abr):
    col = 2 if abr is not None else 1
    bonus_delay = 0
    if start == 0:
        start = 1
        bonus_delay = 0.2
    rounds = round_info.range(start + 1, col, end + 1, col)
    rounds_adj = [float(r.value) + (i * 0.2) for i, r in enumerate(rounds)]
    longest = max(rounds_adj)
    longest_round = rounds_adj.index(longest)
    return round(longest + stime + bonus_delay + 0.0167 - 0.2, 2), longest_round + start


def info(num):
    stats = [c.value for c in race_info.range(num + 1, 4, num + 1, 20)]
    output = ['Name: ' + race(num, None), 'Map: ' + stats[0], 'Mode: ' + stats[1] + ", " + stats[2],
              'Rounds: ' + stats[3], 'Starting cash: ' + stats[4], 'Starting lives: ' + stats[5]]
    modifiers = ''
    for i in range(6, 11):
        if stats[i]:
            modifiers += race_info.cell(1, i + 4).value + ', '
    if modifiers:
        output.append(modifiers[0:-2])
    for i in range(11, 15):
        if stats[i]:
            output.append(race_info.cell(1, i + 4).value + ': ' + stats[i])
    return output
