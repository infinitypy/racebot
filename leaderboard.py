import json
from json import JSONDecodeError
import datetime

import requests

import sheets
import writelbtosheet


def string_to_tuple(entry):
    return tuple(map(str, entry.split(',')))


def column(num, res=''):
    return column(num // 26, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[num % 26] + res) if num > 1 else res


loaded_races = writelbtosheet.fulldata.row_values(1)
full_data = writelbtosheet.fulldata.get_values('B2:' + column(writelbtosheet.fulldata.col_count) + '101', major_dimension='COLUMNS')


def get_api_lb(race_num):
    race_id = sheets.all_ids[race_num - 1]
    race_url = f'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_{race_id}.json'
    try:
        data = requests.get(race_url).json()
    except JSONDecodeError:
        return None
    entries = json.loads(data["data"])['scores']['equal']
    stuff = [(entry['score'], entry['userID']) for entry in entries]

    times = []
    complete = []

    for i in range(len(stuff)):
        if str(stuff[i][0])[-1] == '9':
            times.append(str(stuff[i][0])[0:-1] + '8')
        else:
            times.append(str(stuff[i][0]))

    times = [str(datetime.timedelta(milliseconds=999999999 - int(time)))[3:-3] for time in times]
    for i in range(len(stuff)):
        complete.append(f'{stuff[i][1]}, {times[i]}')

    return complete


def get_leaderboard(race_num):
    if race_num is len(sheets.all_ids):
        output = get_api_lb(race_num)
        if not output:
            return None
    else:
        global full_data
        if int(race_num) == len(sheets.all_ids) - 1 and writelbtosheet.load_race(race_num):
            full_data = writelbtosheet.fulldata.get_values(f'B2:{column(race_num)}101', major_dimension='COLUMNS')
            full_data[race_num - 1] = [cell.value for cell in
                                       writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
        output = full_data[race_num - 1]
    split_entries = [entry.split(',') for entry in output]
    return split_entries


def get_id(race_num, rank):
    if not get_leaderboard(race_num):
        return None
    if rank.isdigit():
        split_entry = string_to_tuple(full_data[race_num - 1][int(rank) - 1])
        if len(split_entry) == 3:
            return split_entry[:2]
        else:
            name = sheets.known(split_entry[0])
            return split_entry[0], name[1]
    else:
        user_id = sheets.known(rank)
        if user_id[0] != user_id[1]:
            return user_id
        for entry in full_data[race_num - 1]:
            if string_to_tuple(entry)[1].lower() == user_id.lower():
                return string_to_tuple(entry)[:2]


def get_nicks(user_id):
    race_nicks = {}
    for race_num in range(1, len(sheets.all_ids)):
        lb = get_leaderboard(race_num)
        if not lb:
            continue
        for entry in lb:
            if not entry[0] or len(entry) == 2:
                continue
            nick = entry[1]
            if entry[0] == user_id and nick:
                if nick not in race_nicks:
                    race_nicks[nick] = 0
                race_nicks[nick] += 1
                break
    return sorted(race_nicks.items(), key=lambda x: x[1], reverse=True)


def get_rank(race_num, user_id):
    full_lb = get_leaderboard(race_num)
    if not full_lb:
        return None
    for index, entry in enumerate(full_lb):
        if entry[0] == user_id:
            return index + 1


def get_all_rank(user_id):
    ranks = []
    for race_num in range(1, len(sheets.all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = get_rank(race_num, user_id)
            if rank:
                ranks.append((race_num, rank))
    return ranks


def get_worst_rank(user_id):
    worst = (0, -1)
    for race_num in range(1, len(sheets.all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = get_rank(race_num, user_id)
            if rank and rank >= worst[1]:
                worst = (race_num, rank)
    return worst


def get_best_rank(user_id):
    best = (0, 101)
    for race_num in range(1, len(sheets.all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = get_rank(race_num, user_id)
            if rank and rank <= best[1]:
                best = (race_num, rank)
    return best
