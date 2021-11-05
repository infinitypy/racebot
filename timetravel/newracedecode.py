import json
import requests


def decode(data_bytes):
    string = ''
    for i, byte in enumerate(data_bytes[14:]):
        string += chr(byte - 21 - i % 6)
    return string


def events(name=None):
    data = requests.get('https://static-api.nkstatic.com/nkapi/skusettings/de23c3d3985a143c77e50966c56cab22.json')
    decoded = json.loads(decode(data.content))
    decoded = json.loads(decoded['data'])['settings']['events']
    newest = {'start' : 0}
    for i in range(len(decoded)):
        if decoded[i]['type'] == 'raceEvent':
            if decoded[i]['start'] > newest['start']:
                newest = decoded[i]
    if name == 'name':
        return newest['name']
    else:
        return f'newest race name: {newest["name"]}\nnewest race id: {newest["id"]}'  

def raceinfo(name):
    race_info = {}

    data = requests.get('https://priority-static-api.nkstatic.com/storage/static/multi?appid=11&files=races/' + name)
    decoded = json.loads(decode(data.content))
    decoded = json.loads(decoded['data'])
    decoded = json.loads(decoded['races/' + name])
    decoded = decoded['challenge']

    # towers
    tower_list = ['DartMonkey', 'BoomerangMonkey', 'BombShooter', 'TackShooter', 'IceMonkey', 'GlueGunner',
                  'SniperMonkey', 'MonkeySub', 'MonkeyBuccaneer', 'MonkeyAce', 'HeliPilot', 'MortarMonkey',
                  'DartlingGunner', 'WizardMonkey', 'SuperMonkey', 'NinjaMonkey', 'Alchemist', 'Druid', 'BananaFarm',
                  'SpikeFactory', 'MonkeyVillage', 'EngineerMonkey']

    ntower_list = ['Dart', 'Boomer', 'Bomb', 'Tack', 'Ice', 'Glue',
                  'Sniper', 'Sub', 'Boat', 'Ace', 'Heli', 'Mortar',
                  'Dartling', 'Wizard', 'Super', 'Ninja', 'Alch', 'Druid', 'Farm',
                  'Spac', 'Village', 'Engi']

    towers = decoded['towers']
    formatted_towers = {}
    hero = ''
    for i in range(len(towers)):
        if towers[i]['isHero'] and towers[i]['max'] == 1:
            hero = towers[i]['tower'] + ', '
        formatted_towers[towers[i]['tower']] = (
            towers[i]['max'], towers[i]['path1NumBlockedTiers'], towers[i]['path2NumBlockedTiers'],
            towers[i]['path3NumBlockedTiers'], towers[i]['isHero'])

    enabled = hero

    for i in range(len(tower_list)):
        if formatted_towers[tower_list[i]][0] != 0:
            enabled += (ntower_list[i])
            if ''.join(map(str, [5 - x for x in formatted_towers[tower_list[i]][1:4]])) != '555':
                enabled += '(' + ''.join(map(str, [5 - x for x in formatted_towers[tower_list[i]][1:4]])) + ')'
            if formatted_towers[tower_list[i]][0] != -1:
                enabled += '[' + str(formatted_towers[tower_list[i]][0]) + ']'

            enabled += ', '
    enabled = enabled[:-2]

    # other info

    # always display
    race_info['name'] = decoded['name']
    race_info['map'] = decoded['map']
    race_info['difficulty'] = decoded['difficulty']
    race_info['mode'] = decoded['mode']
    race_info['rounds'] = [decoded['startRules']['round'], decoded['startRules']['endRound']]
    race_info['startcash'] = decoded['startRules']['cash']
    race_info['lives'] = decoded['startRules']['lives']
    if race_info['lives'] == -1:
        if race_info['difficulty'] == 'Hard':
            race_info['lives'] = 100
        elif race_info['difficulty'] == 'Medium':
            race_info['lives'] = 150
        elif race_info['difficulty'] == 'Easy':
            race_info['lives'] = 200

    # display if not default
    race_info['mk'] = decoded['disableMK']
    race_info['camo'] = decoded['bloonModifiers']['allCamo']
    race_info['regrow'] = decoded['bloonModifiers']['allRegen']
    race_info['selling'] = decoded['disableSelling']

    race_info['bloon speed'] = decoded['bloonModifiers']['speedMultiplier']
    race_info['moab speed'] = decoded['bloonModifiers']['moabSpeedMultiplier']
    race_info['ceram hp'] = decoded['bloonModifiers']['healthMultipliers']['bloons']
    race_info['moab hp'] = decoded['bloonModifiers']['healthMultipliers']['moabs']

    # make into a cute string
    corngrats = f'Full info for {race_info["name"]}'
    corngrats += '\n' + ', '.join((race_info['map'], race_info['difficulty'], race_info['mode']))

    if race_info['mk']:
        corngrats += '\nno MK'
    if race_info['camo']:
        corngrats += '\nall camo'
    if race_info['regrow']:
        corngrats += '\nall regrow'
    if race_info['selling']:
        corngrats += '\nno selling'

    corngrats += f'\nRounds: {str(race_info["rounds"][0])}-{str(race_info["rounds"][1])}'
    corngrats += f'\nCash: {str(race_info["startcash"])}\nLives: {str(race_info["lives"])}'
    corngrats += f'\nTowers: {enabled[]}'

    corngrats += f'\n\nModifiers:\nBloon Speed: {race_info["bloon speed"]}\nCeram hp: {race_info["ceram hp"]}\n' \
                 f'Moab Speed: {race_info["moab speed"]}\nMoab hp: {race_info["moab hp"]}'

    return corngrats
