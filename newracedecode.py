import json

import discord
import requests

import misc
import sheets

f = open('eventlink.txt', 'r')
info_url = f.read()
f.close()
tower_categories = ['Primary', 'Military', 'Magic', 'Support']
canon_to_nick = {'DartMonkey': 'Dart', 'BoomerangMonkey': 'Boomer', 'BombShooter': 'Bomb',
                 'TackShooter': 'Tack', 'IceMonkey': 'Ice', 'GlueGunner': 'Glue',
                 'SniperMonkey': 'Sniper', 'MonkeySub': 'Sub', 'MonkeyBuccaneer': 'Bucc', 'MonkeyAce': 'Ace',
                 'HeliPilot': 'Heli', 'MortarMonkey': 'Mortar', 'DartlingGunner': 'Dartling',
                 'WizardMonkey': 'Wizard', 'SuperMonkey': 'Super',
                 'NinjaMonkey': 'Ninja', 'Alchemist': 'Alch', 'Druid': 'Druid',
                 'BananaFarm': 'Farm', 'SpikeFactory': 'Spact', 'MonkeyVillage': 'Village', 'EngineerMonkey': 'Engi'}


def set_link(link: str) -> None:
    global info_url
    info_url = link
    f = open('eventlink.txt', 'w')
    f.write(info_url)
    f.close()
    sheets.add_race()


def decode(data_bytes):
    string = ''
    for i, byte in enumerate(data_bytes[14:]):
        string += chr(byte - 21 - i % 6)
    return string


def events():
    data = requests.get(info_url, headers={'User-Agent': 'btd6-'})
    decoded = json.loads(decode(data.content))
    decoded = json.loads(decoded['data'])['settings']['events']
    newest = {'start': 0}
    for i in range(len(decoded)):
        if decoded[i]['type'] == 'raceEvent':
            if decoded[i]['start'] > newest['start']:
                newest = decoded[i]
    return newest['name'], newest['id']


def racename():
    data = requests.get(
        'https://priority-static-api.nkstatic.com/storage/static/multi?appid=11&files=races/' + events()[0],
        headers={'User-Agent': 'btd6-'})
    decoded = json.loads(decode(data.content))
    decoded = json.loads(decoded['data'])
    try:
        decoded = json.loads(decoded['races/' + events()[0]])
    except KeyError:
        return None
    decoded = decoded['challenge']
    return decoded['name']


def raceinfo(update, name):
    data = requests.get(
        'https://priority-static-api.nkstatic.com/storage/static/multi?appid=11&files=races/' + name,
        headers={'User-Agent': 'btd6-'})
    decoded = json.loads(decode(data.content))
    decoded = json.loads(decoded['data'])
    try:
        decoded = json.loads(decoded['races/' + name])
    except KeyError:
        return None
    decoded = decoded['challenge']
    towers = decoded['towers']
    formatted_towers = {k: None for k in canon_to_nick.keys()}
    hero = ''
    for tower in towers:
        if tower['isHero'] and tower['max'] == 1:
            hero = tower['tower']
            continue
        if tower['max'] != 0:
            for i in range(1, 4):
                if tower[f'path{i}NumBlockedTiers'] == -1:
                    tower[f'path{i}NumBlockedTiers'] = 5
            blocked_tiers = [tower[f'path{i}NumBlockedTiers'] for i in range(1, 4)]
            avail_tiers = ''
            if blocked_tiers != [0, 0, 0]:
                avail_tiers = f'({"".join([str(5 - x) for x in blocked_tiers])})'
            count = ''
            if tower['max'] != -1:
                count = f'\[{tower["max"]}\]'
            formatted_towers[tower['tower']] = (count, avail_tiers)
    # always display
    race_info = {'name': decoded['name'], 'canonname': name, 'map': misc.space_by_caps(decoded['map']),
                 'difficulty': decoded['difficulty'], 'mode': misc.space_by_caps(decoded['mode']),
                 'rounds': [decoded['startRules']['round'], decoded['startRules']['endRound']],
                 'startcash': decoded['startRules']['cash'], 'maxtowers': decoded['maxTowers'], 'hero': hero}
    if race_info['startcash'] == -1:
        race_info['startcash'] = 325 if race_info['mode'] == 'HalfCash' else 650
    race_info['lives'] = decoded['startRules']['lives']
    if race_info['lives'] == -1:
        race_info['lives'] = 100 if race_info['difficulty'] == 'Hard' else \
            150 if race_info['difficulty'] == 'Medium' else \
            200

    # display if not default
    race_info['mk'] = decoded['disableMK']
    race_info['camo'] = decoded['bloonModifiers']['allCamo']
    race_info['regrow'] = decoded['bloonModifiers']['allRegen']
    race_info['selling'] = decoded['disableSelling']

    race_info['bloon speed'] = decoded['bloonModifiers']['speedMultiplier']
    race_info['moab speed'] = decoded['bloonModifiers']['moabSpeedMultiplier']
    race_info['ceram hp'] = decoded['bloonModifiers']['healthMultipliers']['bloons']
    race_info['moab hp'] = decoded['bloonModifiers']['healthMultipliers']['moabs']
    race_info['regrow rate'] = decoded['bloonModifiers']['regrowRateMultiplier']
    race_info['ability rate'] = \
        decoded['abilityCooldownReductionMultiplier'] if 'abilityCooldownReductionMultiplier' in decoded else 1
    race_info['object cost multi'] = \
        decoded['removeableCostMultiplier'] if 'removeableCostMultiplier' in decoded else 1

    if race_info['map'] == 'Tutorial':
        race_info['map'] = 'Monkey Meadow'
    elif race_info['map'] == 'Town Centre':
        race_info['map'] = 'Town Center'
    if race_info['mode'] == 'Clicks':
        race_info['mode'] = 'CHIMPS'
    if race_info['hero'] == 'ChosenPrimaryHero':
        race_info['hero'] = 'Any hero'

    if update:
        sheets.write_race(race_info)

    return race_info, formatted_towers


def infotoembed(race_info, formatted_towers):
    game_modifiers = f'{"No MK " if race_info["mk"] else ""}{"All camo " if race_info["camo"] else ""}' \
                     f'{"All regrow " if race_info["regrow"] else ""}{"No selling " if race_info["selling"] else ""}'
    bloon_modifiers = []
    if race_info['bloon speed'] != 1.0:
        bloon_modifiers.append(f'{race_info["bloon speed"] * 100:.0f}% bloon speed')
    if race_info['ceram hp'] != 1.0:
        bloon_modifiers.append(f'{race_info["ceram hp"] * 100:.0f}% ceramic health')
    if race_info['moab speed'] != 1.0:
        bloon_modifiers.append(f'{race_info["moab speed"] * 100:.0f}% blimp speed')
    if race_info['moab hp'] != 1.0:
        bloon_modifiers.append(f'{race_info["moab hp"] * 100:.0f}% blimp health')
    if race_info['regrow rate'] != 1.0:
        bloon_modifiers.append(f'{race_info["regrow rate"] * 100:.0f}% regrow rate')
    if race_info['ability rate'] != 1.0:
        bloon_modifiers.append(f'{race_info["ability rate"] * 100:.0f}% ability cooldowns')
    if race_info['object cost multi'] != 1.0:
        if race_info['object cost multi'] == 12.0:
            bloon_modifiers.append('Obstacles not removable')
        else:
            bloon_modifiers.append(f'{race_info["object cost multi"]}x removable cost multiplier')
    description = ', '.join((race_info['map'], race_info['difficulty'], race_info['mode']))
    description += f'\n{game_modifiers}' if game_modifiers else ''
    description += f'\n{", ".join(bloon_modifiers)}' if bloon_modifiers else ''
    description += f'\n{misc.space_by_caps(race_info["hero"])}'
    max_towers = race_info['maxtowers']
    description += f'\n{f"{max_towers} towers only" if max_towers != -1 else ""}'

    embed = discord.Embed(
        title=f'Full info for {race_info["name"]}',
        description=description,
        colour=discord.Colour.orange(),
        url=('https://fast-static-api.nkstatic.com/storage/static/appdocs/11/races/' + race_info['canonname'])
    )

    embed.add_field(name='Rounds', value='{}-{}'.format(*race_info['rounds']))
    embed.add_field(name='Start cash', value=race_info['startcash'])
    embed.add_field(name='Lives', value=race_info['lives'])
    categorized = [[], [], [], []]
    for index, (tower, stats) in enumerate(formatted_towers.items()):
        if stats:
            output = f'{canon_to_nick[tower]}{stats[0]}{stats[1]}'
            if index < 6:
                categorized[0].append(output)
            elif index < 13:
                categorized[1].append(output)
            elif index < 18:
                categorized[2].append(output)
            else:
                categorized[3].append(output)
    for index, category in enumerate(categorized):
        if category:
            embed.add_field(name=tower_categories[index], value=', '.join(category), inline=False)
    return embed
