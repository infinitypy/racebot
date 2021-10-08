import sheets
import writelbtosheet

all_ids = sheets.race_info.col_values(3)[1:]
loaded_races = writelbtosheet.fulldata.row_values(1)
full_data = writelbtosheet.fulldata.get_values('B2:ER101', major_dimension='COLUMNS')


def string_to_tuple(entry):
    return tuple(map(str, entry.split(',')))


def column(num, res=''):
    return column(num // 26, 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[num % 26] + res) if num > 1 else res


def get_leaderboard(race_num, first, last):
    leaderboard = ''
    if race_num is len(all_ids):
        full_lb = [entry.split(',') for entry in writelbtosheet.lb(race_num)]
        for i in range(last - first + 1):
            leaderboard += '\n' + str(i + first).ljust(2) + ' ' + full_lb[i + first - 1][2] + ' ' + full_lb[i + first - 1][1]
        return leaderboard
    global loaded_races, full_data
    loaded_races = writelbtosheet.fulldata.row_values(1)
    if str(race_num) not in loaded_races:
        if not writelbtosheet.load_race(race_num):
            return "No data"
        full_data = writelbtosheet.fulldata.get_values('B2:' + column(race_num) + '101', major_dimension='COLUMNS')
        full_data[race_num - 1] = [cell.value for cell in
                                   writelbtosheet.fulldata.range(2, race_num + 1, 101, race_num + 1)]
    stuff = [string_to_tuple(entry) for entry in full_data[race_num - 1]]

    for i in range(last - first + 1):
        leaderboard += "\n" + str(i + first).ljust(2) + ' ' + stuff[i + first - 1][2] + ' ' + stuff[i + first - 1][1]

    return str(leaderboard)


def get_id(race_num, rank):
    if str(race_num) not in loaded_races:
        if not writelbtosheet.load_race(race_num):
            return "No data"
        full_data[race_num - 1] = writelbtosheet.fulldata.col_values(race_num + 1, 101, race_num + 1)[1:]
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
            full_data[race_num - 1] = writelbtosheet.fulldata.col_values(race_num + 1, 101, race_num + 1)[1:]
        for entry in full_data[race_num - 1]:
            if string_to_tuple(entry)[0] == user_id:
                if string_to_tuple(entry)[1] not in race_nicks:
                    race_nicks.append(string_to_tuple(entry)[1])
                break

    return race_nicks


def get_rank(race_num, user_id):
    if str(race_num) not in loaded_races:
        if not writelbtosheet.load_race(race_num):
            return None
    full_data[race_num - 1] = writelbtosheet.lb(race_num)
    print(writelbtosheet.lb(race_num))
    for rank, entry in enumerate(full_data[race_num - 1]):
        if string_to_tuple(entry)[0] == user_id:
            return rank + 1


def get_average_rank(user_id):
    ranks = []
    for race_num in range(1, 146 + 1):
        if race_num != 107 and race_num != 143:
            if str(race_num) not in loaded_races:
                if not writelbtosheet.load_race(race_num):
                    continue
                full_data[race_num - 1] = writelbtosheet.fulldata.col_values(race_num + 1, 101, race_num + 1)[1:]
            rank = get_rank(race_num, user_id)
            if rank:
                ranks.append(rank)
    return len(ranks), sum(ranks)


def get_worst_rank(user_id):
    worst = (0, -1)
    for race_num in range(1, 146 + 1):
        if race_num != 107 and race_num != 143:
            if str(race_num) not in loaded_races:
                if not writelbtosheet.load_race(race_num):
                    continue
                full_data[race_num - 1] = writelbtosheet.fulldata.col_values(race_num + 1, 101, race_num + 1)[1:]
            rank = get_rank(race_num, user_id)
            if rank and rank >= worst[1]:
                worst = (race_num, rank)
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
            rank = get_rank(race_num, user_id)
            if rank and rank <= best[1]:
                best = (race_num, rank)
    return best
