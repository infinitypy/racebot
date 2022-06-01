import requests
import sheets
from json import JSONDecodeError


def get_profile(user_id):
    user_url = f'https://priority-static-api.nkstatic.com/storage/static/11/{user_id}/public-stats'
    try:
        data = requests.get(user_url, headers={'User-Agent': 'btd6-'}).json()
    except JSONDecodeError:
        return None
    medals = data['raceMedals']

    medal_names = ['BlackDiamond', 'RedDiamond', 'Diamond', 'GoldDiamond', 'DoubleGold',
                   'GoldSilver', 'DoubleSilver', 'Silver', 'Bronze']
    medal_counts = [medals.get(name, 0) for name in medal_names]

    return ('<:BlackDiamondMedal:896548315548762133> {}\n' +
            '<:RedDiamondMedal:896548361321201764> {}\n<:DiamondMedal:896548376164843540> {}\n' +
            '<:Top50:897738138636664883> {}\n<:DoubleGoldMedal:896548449489682462> {}\n' +
            '<:GoldSilverMedal:896548496860127302> {}\n<:DoubleSilverMedal:896548568075231233> {}\n' +
            '<:SilverMedal:896548595581481011> {}\n<:BronzeMedal:896548636211683339> {}\n\n' +
            '<:ParticipationMedal:896548662111531028> {}') \
        .format(*medal_counts, sum(medal_counts))


def get_medal_counts(user_id):
    user_url = f'https://priority-static-api.nkstatic.com/storage/static/11/{user_id}/public-stats'
    try:
        data = requests.get(user_url, headers={'User-Agent': 'btd6-'}).json()
    except JSONDecodeError:
        return [0, 0, 0, 0]
    medals = data['raceMedals']

    medal_names = ['BlackDiamond', 'RedDiamond', 'Diamond']
    medal_counts = [medals.get(name, 0) for name in medal_names]
    medal_counts.append(sum(medal_counts))

    return medal_counts


def generate_badge_lb():
    blb = {}
    for i in range(len(sheets.known_ids) - 1):
        blb[sheets.known_players[i + 1]] = get_medal_counts(sheets.known_ids[i + 1])

    sortedbytotal = sorted(blb.items(), key=lambda x: x[1][-1], reverse=True)

    output_str = '\n``{:<18}``<:BlackDiamondMedal:896548315548762133>``{:<3}``' \
                 '<:RedDiamondMedal:896548361321201764>``{:<3}``' \
                 '<:DiamondMedal:896548376164843540>``{:<3}{:<3}``' \
        .format('RandyZ524', len(sheets.all_ids) - 1, 0, 0, len(sheets.all_ids) - 1)
    for i in range(10):
        output_str += '\n``{:<18}``<:BlackDiamondMedal:896548315548762133>``{:<3}``' \
                      '<:RedDiamondMedal:896548361321201764>``{:<3}``' \
                      '<:DiamondMedal:896548376164843540>``{:<3}{:<3}``' \
            .format(sortedbytotal[i][0], *sortedbytotal[i][1])
    output_str += '\n``{:<18}``<:BlackDiamondMedal:896548315548762133>``{:<3}``' \
                  '<:RedDiamondMedal:896548361321201764>``{:<3}``' \
                  '<:DiamondMedal:896548376164843540>``{:<3}{:<3}``'\
        .format('Chocbox', 0, 0, 0, 0)
    return output_str
