import datetime
import json
import time
from json import JSONDecodeError

import aiohttp
import urllib3

import newracedecode
import sheets
import writelbtosheet

full_data = writelbtosheet.fulldata.get_all_values(major_dimension='COLUMNS')[1:]
full_data = [col[1:] for col in full_data]
timestamp = 0


async def get_api_lb(race_num):
    try:
        race_id = sheets.all_ids[race_num - 1]
    except Exception:
        race_id = newracedecode.events()[1]
    race_url = f'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_{race_id}.json'
    http = urllib3.PoolManager()
    try:
        r = http.request('GET', race_url)
        data = json.loads(r.data)
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

    times = [str(datetime.timedelta(milliseconds=1000000000 - int(time)))[3:-3] for time in times]
    for i in range(len(stuff)):
        complete.append(f'{stuff[i][1]}, {times[i]}')

    return complete


async def get_leaderboard(race_num, update=False):
    global full_data, timestamp
    if update and time.time() - timestamp > 300 and newracedecode.racename() and newracedecode.racename() not in sheets.all_names:
        sheets.add_race()
        await writelbtosheet.load_race(writelbtosheet.fulldata.col_count)
        full_data = writelbtosheet.fulldata.get_all_values(major_dimension='COLUMNS')[1:]
        full_data = [col[1:] for col in full_data]
        timestamp = time.time()
    if not race_num:
        race_num = writelbtosheet.fulldata.col_count - 1
        if update and time.time() - timestamp > 300:
            await writelbtosheet.load_race(race_num)
            full_data = writelbtosheet.fulldata.get_all_values(major_dimension='COLUMNS')[1:]
            full_data = [col[1:] for col in full_data]
            timestamp = time.time()
    else:
        try:
            race_num = int(race_num)
        except TypeError:
            return list()
    try:
        output = full_data[race_num - 1]
    except IndexError:
        return list()
    if not output[0]:
        return list()
    split_entries = [[x.strip() for x in entry.split(',')] for entry in output]
    return split_entries


async def get_id(race_num: int, rank) -> (str, str):
    try:
        race_num = int(race_num)
    except TypeError:
        return None
    if not await get_leaderboard(race_num):
        return None
    if rank.isdigit():
        rank = int(rank)
        split_entry = (await get_leaderboard(race_num))[rank - 1]
        if len(split_entry) == 3:
            return split_entry[:2]
        else:
            name = sheets.known(split_entry[0])
            return split_entry[0], name[1]
    else:
        user_id = sheets.known(rank)
        if user_id[0] != user_id[1]:
            return user_id
        for split_entry in await get_leaderboard(race_num):
            if split_entry[1].lower() == user_id[1].lower():
                return split_entry[:2]
        return None


async def get_nicks(user_id):
    race_nicks = {}
    for race_num in range(1, len(sheets.all_ids)):
        lb = await get_leaderboard(race_num)
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


async def get_rank(race_num, user_id):
    full_lb = await get_leaderboard(race_num)
    if not full_lb:
        return None
    for index, entry in enumerate(full_lb):
        if entry[0] == user_id:
            if len(entry) == 3:
                return index + 1, entry[2]
            else:
                return index + 1, entry[1]


async def get_all_rank(user_id):
    ranks = []
    for race_num in range(1, len(sheets.all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = await get_rank(race_num, user_id)
            if rank:
                ranks.append((race_num, rank[0]))
    return ranks


async def get_worst_rank(user_id):
    worst = (0, -1)
    for race_num in range(1, len(sheets.all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = await get_rank(race_num, user_id)
            if rank and rank >= worst[1]:
                worst = (race_num, rank[0])
    return worst


async def get_best_rank(user_id):
    best = (0, 101)
    for race_num in range(1, len(sheets.all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = await get_rank(race_num, user_id)
            if rank and rank <= best[1]:
                best = (race_num, rank[0])
    return best
