import gspread
from oauth2client.service_account import ServiceAccountCredentials

import newracedecode
import writelbtosheet

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('1iG4mtopJVlF7g3gv6sNrYspyonSQGSHuDOb-QMNVnPc')
race_info = sheet.worksheet('Race Info')
round_info = sheet.worksheet('rounds')
players = sheet.worksheet('Player Info')

all_names = race_info.col_values(2)[1:]
all_cnames = race_info.col_values(3)[1:]
all_ids = race_info.col_values(4)[1:]

known_players = players.col_values(1)
known_ids = players.col_values(2)

assoc_ids = writelbtosheet.user_data.col_values(2)
assoc_players = writelbtosheet.user_data.col_values(3)


def known(identifier):
    identifier = str(identifier)
    ids_to_names = {}
    for i in range(min(len(assoc_ids), len(assoc_players))):
        ids_to_names[assoc_ids[i]] = assoc_players[i]
    if identifier in ids_to_names:
        return identifier, ids_to_names[identifier].split(',')[0]
    else:
        for id, aliases in ids_to_names.items():
            split_aliases = aliases.lower().split(',')
            if identifier.lower() in split_aliases:
                return id, aliases.split(',')[0]
    return identifier, identifier


def race(num, display_col=0):
    if not num:
        num = writelbtosheet.fulldata.col_count - 1
    try:
        num = int(num)
    except TypeError:
        return ''
    if num <= 0:
        return ''
    if num == 129 and display_col == 0:
        return ':corn::tada:'
    return race_info.cell(num + 1, display_col + 2).value


def race_range(start, end, display_col=0):
    try:
        start = int(start)
        end = int(end)
    except TypeError:
        return ''
    if start <= 0 or end <= 0 or start > end:
        return ''
    names = race_info.col_values(display_col + 2)
    output = '```'
    for i in range(start, end + 1):
        output += f'{i:>2}. {names[i]}\n'
    return output[0: -1] + '```'


def length(num, abr):
    col = 2 if abr is not None else 1
    return round_info.cell(num + 1, col).value


def rtime(start, end, stime, abr):
    col = 2 if abr is not None else 1
    bonus_delay = 0
    if start == 0:
        start = 1
        bonus_delay = 0.2
    rounds = round_info.range(start + 2, col, end + 1, col)
    rounds_adj = [float(r.value) + ((i + 1) * 0.2) for i, r in enumerate(rounds)]
    longest = max(rounds_adj)
    longest_round = rounds_adj.index(longest) + 1
    time = longest + stime + bonus_delay + 0.0333 - 0.2
    time = round(time * 60) / 60
    return time, longest_round + start


def write_race(race_stats):
    row_num = [name.lower() for name in all_names].index(race_stats['name'].lower()) + 2
    cell_info = []
    cell_info.append([race_stats['map']])
    cell_info.append([race_stats['difficulty']])
    cell_info.append([race_stats['mode']])
    cell_info.append([])
    race_info.update(f'E{row_num}:G{row_num}', cell_info, major_dimension='COLUMNS')


def add_race():
    race_info.add_rows(1)
    race_info.update_cell(race_info.row_count + 1, 1, race_info.row_count)
    race_info.update_cell(race_info.row_count + 1, 2, newracedecode.racename())
    race_info.update_cell(race_info.row_count + 1, 4, newracedecode.events()[1])
