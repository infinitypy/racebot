import requests


def getprofile(user_id):
    user_url = 'https://priority-static-api.nkstatic.com/storage/static/11/' + user_id + '/public-stats'
    data = requests.get(user_url, headers={'User-Agent': 'btd6-'}).json()

    name = data['playerName']
    medals = data['raceMedals']

    medal_names = ['BlackDiamond', 'RedDiamond', 'Diamond', 'GoldDiamond', 'DoubleGold',
                   'GoldSilver', 'DoubleSilver', 'Silver', 'Bronze']
    medal_counts = [medals.get(name, 0) for name in medal_names]
    sum(medal_counts)

    return 'Race Stats for **{}**\n```User ID: {}\n1st: {}\n2nd: {}\n3rd: {}\nTop 50: {}\n' \
           'Top 1%: {}\nTop 10%: {}\nTop 25%: {}\nTop 50%: {}\nTop 75%: {}\n\nTotal: {}```' \
        .format(name, user_id, *medal_counts, sum(medal_counts))
