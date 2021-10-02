import gspread
from oauth2client.service_account import ServiceAccountCredentials
from decimal import Decimal

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1iG4mtopJVlF7g3gv6sNrYspyonSQGSHuDOb-QMNVnPc")
race_info = sheet.worksheet("raceinfo")
round_info = sheet.worksheet("rounds")


def get_race_name(num, id):
    col = 3 if id is not None else 2
    if num == 129:
        return ':corn::tada:'
    else:
        return race_info.cell(num + 1, col).value


def length(num, abr):
    col = 2 if abr is not None else 1
    return round_info.cell(num + 1, col).value


def last_bloon_time(start, end, stime, abr):
    col = 2 if abr is not None else 1
    bonusdelay = 0
    if start == 0:
        start = 1
        bonusdelay = 0.2
    
    rounds = round_info.range(start + 1, col, end + 1, col)
    rounds_adj = []
    for i, r in enumerate(rounds):
        rounds_adj.append(float(r.value) + (i * 0.2))
    longest = max(rounds_adj)
    longest_round = rounds_adj.index(longest)
    return round(longest + stime + bonusdelay + 0.0167 - 0.2 , 2), longest_round + start
