import sheets
import writelbtosheet

all_ids = sheets.race_info.col_values(3)[1:]
loaded_races = writelbtosheet.fulldata.row_values(1)
full_data = writelbtosheet.fulldata.get_values('B2:ER101', major_dimension='COLUMNS')


def string_to_tuple(entry):
    return tuple(map(str, entry.split(',')))


def column(num, res=''):
    return column(num // 26, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[num % 26] + res) if num > 1 else res


def get_leaderboard(race_num):
    if race_num is len(all_ids):
        output = writelbtosheet.lb(race_num)
        if not output:
            return None
        split_entries = [entry.split(',') for entry in output]
        for entry in split_entries:
            res = sheets.known(str(entry[0]))
            if res[0] == res[1]:
                entry[0] = ' ID: ' + res[1][0:3] + '...'
            else:
                entry[0] = res[1]
        return split_entries
    global loaded_races, full_data
    if str(race_num) not in loaded_races:
        return None
        #if not writelbtosheet.load_race(race_num):
        #    return None
        #full_data = writelbtosheet.fulldata.get_values('B2:' + column(race_num) + '101', major_dimension='COLUMNS')
        #full_data[race_num - 1] = [cell.value for cell in
        #                           writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
    return [string_to_tuple(entry) for entry in full_data[race_num - 1]]


def get_id(race_num, rank):
    if not get_leaderboard(race_num):
        return None
    if rank.isdigit():
        return string_to_tuple(full_data[race_num - 1][int(rank) - 1])[:2]
    else:
        user_id = sheets.known(rank)
        if user_id[0] != user_id[1]:
            return user_id
        for entry in full_data[race_num - 1]:
            if string_to_tuple(entry)[1].lower() == user_id.lower():
                return string_to_tuple(entry)[:2]


def get_nicks(user_id):
    race_nicks = []

    for race_num in range(1, len(all_ids)):
        if not get_leaderboard(race_num):
            continue
        for entry in full_data[race_num - 1]:
            if string_to_tuple(entry)[0] == user_id:
                if string_to_tuple(entry)[1] not in race_nicks:
                    race_nicks.append(string_to_tuple(entry)[1])
                break

    return race_nicks


def get_rank(race_num, user_id):
    full_lb = get_leaderboard(race_num)
    if not full_lb:
        return None
    for index, entry in enumerate(full_lb):
        if entry[0] == user_id:
            return index + 1


def get_all_rank(user_id):
    ranks = []
    for race_num in range(1, len(all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = get_rank(race_num, user_id)
            if rank:
                ranks.append((race_num, rank))
    return ranks


def get_worst_rank(user_id):
    worst = (0, -1)
    for race_num in range(1, len(all_ids) + 1):
        if race_num != 107 and race_num != 143:
            rank = get_rank(race_num, user_id)
            if rank and rank >= worst[1]:
                worst = (race_num, rank)
    return worst


def get_best_rank(user_id):
    best = (0, 101)
    for race_num in range(1, 146 + 1):
        if race_num != 107 and race_num != 143:
            rank = get_rank(race_num, user_id)
            if rank and rank <= best[1]:
                best = (race_num, rank)
    return best
