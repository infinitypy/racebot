import requests
import json

def getprofile(userid):
    userurl = 'https://priority-static-api.nkstatic.com/storage/static/11/' + userid + '/public-stats'
    data = requests.get(userurl, headers={'User-Agent':'btd6-'}).json()

    name = data['playerName']
    uid = data['playerId']
    medals = data['raceMedals']

    first = medals.get('BlackDiamond', 0)
    second = medals.get('RedDiamond', 0)
    third = medals.get('Diamond', 0)
    fifty = medals.get('GoldDiamond', 0)
    one = medals.get('DoubleGold', 0)
    ten = medals.get('GoldSilver', 0)
    twfive = medals.get('DoubleSilver', 0)
    fiftyp = medals.get('Silver', 0)
    seveny = medals.get('Bronze', 0)
    
    formattedinfo = '```Race Stats for ' + name + '\nuserid: ' + uid + '\n1st: ' + str(first) + '\n2nd: ' + str(second) + '\n3rd: ' + str(third) + '\ntop 50: ' + str(fifty) + '\ntop 1%: ' + str(one) + '\ntop 10%: ' + str(ten) + '\ntop 25%: ' + str(twfive) + '\ntop 50%: ' + str(fiftyp) + '\ntop 75%: ' + str(seveny) + '\n\nTotal: ' + str(first+second+third+fifty+one+ten+twfive+fiftyp+seveny) + '```'


    return formattedinfo