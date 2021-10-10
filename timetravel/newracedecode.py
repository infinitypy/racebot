import requests, json

def decode(bytes):
    string = ''
    for i, byte in enumerate(bytes[14:]):
        string += chr(byte - 21 - i % 6)
    return string

racename = 'Exponential_4'

data = requests.get('https://priority-static-api.nkstatic.com/storage/static/multi?appid=11&files=races/'+racename)
decoded = json.loads(decode(data.content))
decoded = json.loads(decoded['data'])
decoded = json.loads(decoded['races/'+racename])

info = decoded['challenge']['towers']
formattedinfo = {}

for i in range(len(info)):
    formattedinfo[info[i]['tower']] = (info[i]['max'], info[i]['path1NumBlockedTiers'], info[i]['path2NumBlockedTiers'], info[i]['path3NumBlockedTiers'], info[i]['isHero'])

print(formattedinfo)