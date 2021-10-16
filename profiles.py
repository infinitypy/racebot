import requests


def get_profile(user_id):
    user_url = 'https://priority-static-api.nkstatic.com/storage/static/11/{}/public-stats'\
        .format(user_id)
    data = requests.get(user_url, headers={'User-Agent': 'btd6-'}).json()
    print(data)
    name = data['playerName']
    medals = data['raceMedals']

    medal_names = ['BlackDiamond', 'RedDiamond', 'Diamond', 'GoldDiamond', 'DoubleGold',
                   'GoldSilver', 'DoubleSilver', 'Silver', 'Bronze']
    medal_counts = [medals.get(name, 0) for name in medal_names]

    return ('Race Stats for **{}**\nUser ID: {}\n<:BlackDiamondMedal:896548315548762133> {}\n' +
            '<:RedDiamondMedal:896548361321201764> {}\n<:DiamondMedal:896548376164843540> {}\n' +
            '<:Top50:897738138636664883> {}\n<:DoubleGoldMedal:896548449489682462> {}\n' +
            '<:GoldSilverMedal:896548496860127302> {}\n<:DoubleSilverMedal:896548568075231233> {}\n' +
            '<:SilverMedal:896548595581481011> {}\n<:BronzeMedal:896548636211683339> {}\n\n' +
            '<:ParticipationMedal:896548662111531028> {}')\
        .format(name, user_id, *medal_counts, sum(medal_counts))
