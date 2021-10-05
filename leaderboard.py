import requests
import json
import datetime

import sheets

all_races = {}
all_ids = [cell.value for cell in sheets.race_info.range(2, 3, 147, 3)]


def load_race(race_num):
    race_id = all_ids[race_num - 1]
    race_url = 'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_' + race_id + '.json'
    try:
        data = requests.get(race_url).json()
    except Exception:
        return False
    entries = json.loads(data["data"])['scores']['equal']
    if not entries:
        return False
    all_races[race_num] = [(entry['metadata'].split(',')[0], entry['score'], entry['userID']) for entry in entries]
    return True


def get_leaderboard(race_num, first, last):
    if race_num not in all_races:
        if not load_race(race_num):
            return "No data"
    stuff = all_races[race_num]
    times = []

    for i in range(len(stuff)):
        if str(stuff[i][1])[-1] == '9':
            times.append(str(stuff[i][1])[0:-1] + '8')
        else:
            times.append(str(stuff[i][1]))

    leaderboard = ''
    for i in range(last - first + 1):
        leaderboard += "\n" + str(i + first).ljust(2) + ' ' + str(
            datetime.timedelta(milliseconds=999999999 - int(times[i + first - 1])))[3:-4] + ' ' + \
                       str(stuff[i + first - 1][0])
    return str(leaderboard)


def get_id(race_num, rank):
    if race_num not in all_races:
        if not load_race(race_num):
            return "No data"
    if rank.isdigit():
        return all_races[race_num][int(rank) - 1]
    else:
        for entry in all_races[race_num]:
            if entry[0] == rank:
                return entry


def get_nicks(user_id):
    race_nicks = set()
    for i in range(1, 146 + 1):
        if i not in all_races:
            if not load_race(i):
                print(i)
                continue
        if all_races[i]:
            for entry in all_races[i]:
                if entry[2] == user_id:
                    race_nicks.add(entry[0])
                    break
    return race_nicks


def get_average_rank(user_id):
    ranks = []
    for i in range(1, 146 + 1):
        if i != 107 and i != 143:
            if i not in all_races:
                if not load_race(i):
                    continue
            if all_races[i]:
                for rank, entry in enumerate(all_races[i]):
                    if entry[2] == user_id:
                        ranks.append(rank + 1)
                        break
    return len(ranks), sum(ranks) / len(ranks)


def get_worst_rank(user_id):
    worst = (0, -1)
    for i in range(1, 146 + 1):
        if i != 107 and i != 143:
            if i not in all_races:
                if not load_race(i):
                    continue
            if all_races[i]:
                for rank, entry in enumerate(all_races[i]):
                    if entry[2] == user_id and rank + 1 >= worst[1]:
                        worst = (i, rank + 1)
                        break
    return worst


def get_best_rank(user_id):
    worst = (0, 101)
    for i in range(1, 146 + 1):
        if i != 107 and i != 143:
            if i not in all_races:
                if not load_race(i):
                    continue
            if all_races[i]:
                for rank, entry in enumerate(all_races[i]):
                    if entry[2] == user_id and rank + 1 <= worst[1]:
                        worst = (i, rank + 1)
                        break
    return worst
