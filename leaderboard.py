import datetime
import sheets
import writelbtosheet

all_ids = [cell.value for cell in sheets.race_info.range(2, 3, 147, 3)]
loaded_races = writelbtosheet.fulldata.row_values(1)
full_data = writelbtosheet.fulldata.get_values('B2:EQ101', major_dimension='COLUMNS')
#print(loaded_races)


def string_to_tuple(entry):
    return tuple(map(str, entry.split(',')))


def get_leaderboard(race_num, first, last):
    if str(race_num) not in loaded_races:
        if not writelbtosheet.load_race(race_num):
            return "No data"
        full_data[race_num - 1] = [cell.value for cell in
                                   writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
    stuff = [string_to_tuple(entry) for entry in full_data[race_num - 1]]

    leaderboard = ''
    for i in range(last - first + 1):
        leaderboard += "\n" + str(i + first).ljust(2)+ ' ' + stuff[i+first-1][2] + ' ' + stuff[i+first-1][1]
    
    return str(leaderboard)


def get_id(race_num, rank):
    if str(race_num) not in loaded_races:
        if not writelbtosheet.load_race(race_num):
            return "No data"
        full_data[race_num - 1] = [cell.value for cell in
                                   writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
    if rank.isdigit():
        return string_to_tuple(full_data[race_num - 1][int(rank) - 1])
    else:
        for entry in full_data[race_num - 1]:
            if string_to_tuple(entry)[1].lower() == rank.lower():
                return string_to_tuple(entry)


def get_nicks(user_id):
    race_nicks = []
    for race_num in range(1, 146 + 1):
        if str(race_num) not in loaded_races:
            if not writelbtosheet.load_race(race_num):
                continue
            full_data[race_num - 1] = [cell.value for cell in
                                       writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
        for entry in full_data[race_num - 1]:
            if string_to_tuple(entry)[0] == user_id:
                if string_to_tuple(entry)[1] not in race_nicks:
                    race_nicks.append(string_to_tuple(entry)[1])
                break
    return race_nicks


def get_average_rank(user_id):
    ranks = []
    for race_num in range(1, 146 + 1):
        if race_num != 107 and race_num != 143:
            if str(race_num) not in loaded_races:
                if not writelbtosheet.load_race(race_num):
                    continue
                full_data[race_num - 1] = [cell.value for cell in
                                           writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
            for rank, entry in enumerate(full_data[race_num - 1]):
                if string_to_tuple(entry)[0] == user_id:
                    ranks.append(rank + 1)
                    break
    return len(ranks), sum(ranks)


def get_worst_rank(user_id):
    worst = (0, -1)
    for race_num in range(1, 146 + 1):
        if race_num != 107 and race_num != 143:
            if str(race_num) not in loaded_races:
                if not writelbtosheet.load_race(race_num):
                    continue
                full_data[race_num - 1] = [cell.value for cell in
                                           writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
            for rank, entry in enumerate(full_data[race_num - 1]):
                if string_to_tuple(entry)[0] == user_id and rank + 1 >= worst[1]:
                    worst = (race_num, rank + 1)
                    break
    return worst


def get_best_rank(user_id):
    best = (0, 101)
    for race_num in range(1, 146 + 1):
        if race_num != 107 and race_num != 143:
            if str(race_num) not in loaded_races:
                if not writelbtosheet.load_race(race_num):
                    continue
                full_data[race_num - 1] = [cell.value for cell in
                                           writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
            for rank, entry in enumerate(full_data[race_num - 1]):
                if string_to_tuple(entry)[0] == user_id and rank + 1 <= best[1]:
                    best = (race_num, rank + 1)
                    break
    return best
