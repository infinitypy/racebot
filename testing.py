import leaderboard

unique_ids = set()
for race_lb in leaderboard.full_data:
    for entry in race_lb:
        if entry:
            unique_ids.add(entry[0:entry.index(',')])
for id in unique_ids:
    nicks = leaderboard.get_nicks(id)
    if not nicks:
        most_used = ' NONE'
    else:
        most_used = nicks[0][0]
    print(f'{id}: {most_used}')
