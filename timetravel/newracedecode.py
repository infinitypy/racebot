import requests, json

def decode(bytes):
    string = ''
    for i, byte in enumerate(bytes[14:]):
        string += chr(byte - 21 - i % 6)
    return string

def raceinfo(name):
    raceinfo = {}

    data = requests.get('https://priority-static-api.nkstatic.com/storage/static/multi?appid=11&files=races/'+name)
    decoded = json.loads(decode(data.content))
    decoded = json.loads(decoded['data'])
    decoded = json.loads(decoded['races/'+name])
    decoded = decoded['challenge']

    #towers
    tlist = ['DartMonkey', 'BoomerangMonkey', 'BombShooter', 'TackShooter', 'IceMonkey', 'GlueGunner', 'SniperMonkey', 'MonkeySub', 'MonkeyBuccaneer', 'MonkeyAce', 'HeliPilot', 'MortarMonkey', 'DartlingGunner', 'WizardMonkey', 'SuperMonkey', 'NinjaMonkey', 'Alchemist', 'Druid', 'BananaFarm', 'SpikeFactory', 'MonkeyVillage', 'EngineerMonkey']

    towers = decoded['towers']
    formattedtowers = {}
    for i in range(len(towers)):
        formattedtowers[towers[i]['tower']] = (towers[i]['max'], towers[i]['path1NumBlockedTiers'], towers[i]['path2NumBlockedTiers'], towers[i]['path3NumBlockedTiers'], towers[i]['isHero'])
    
    enabled = ''

    for i in range(len(tlist)):
        if formattedtowers[tlist[i]][0] != 0:
            enabled+= (tlist[i])
            if ''.join(map(str, [5-x for x in formattedtowers[tlist[i]][1:4]])) != '555':
                enabled+= '(' + ''.join(map(str, [5-x for x in formattedtowers[tlist[i]][1:4]])) + ')'
            if formattedtowers[tlist[i]][0] != -1:
                enabled+= '[' + str(formattedtowers[tlist[i]][0]) + ']'

            enabled+=', '

    ###other info

    #always display
    raceinfo['name'] = decoded['name']
    raceinfo['map'] = decoded['map']
    raceinfo['difficulty'] = decoded['difficulty']
    raceinfo['mode'] = decoded['mode']
    raceinfo['rounds'] = [decoded['startRules']['round'], decoded['startRules']['endRound']]
    raceinfo['startcash'] = decoded['startRules']['cash']
    raceinfo['lives'] = decoded['startRules']['lives']

    #display if not default
    raceinfo['mk'] = decoded['disableMK']
    raceinfo['camo'] = decoded['bloonModifiers']['allCamo']
    raceinfo['regrow'] = decoded['bloonModifiers']['allRegen']
    raceinfo['selling'] = decoded['disableSelling']

    
    raceinfo['bloon speed'] = decoded['bloonModifiers']['speedMultiplier']
    raceinfo['moab speed'] = decoded['bloonModifiers']['moabSpeedMultiplier']
    raceinfo['ceram hp'] = decoded['bloonModifiers']['healthMultipliers']['bloons']
    raceinfo['moab hp'] = decoded['bloonModifiers']['healthMultipliers']['moabs']




    #make into a cute string
    corngrats = 'Full info for ' + raceinfo['name']
    corngrats+= '\n' + ', '.join((raceinfo['map'], raceinfo['difficulty'], raceinfo['mode']))


    if raceinfo['mk']: corngrats+='\nno MK'
    if raceinfo['camo']: corngrats+='\nall camo'
    if raceinfo['regrow']: corngrats+='\nall regrow'

    corngrats+= '\nRounds: ' + str(raceinfo['rounds'][0]) + '-' + str(raceinfo['rounds'][1])
    corngrats+= '\nCash: ' + str(raceinfo['startcash']) + '\nLives: ' + str(raceinfo['lives'])
    corngrats+= '\nTowers: ' + enabled[:-2]

    return corngrats
