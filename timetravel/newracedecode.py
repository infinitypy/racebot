import requests


def decode(stuff):
    for i in range(14, len(stuff)):
        stuff[i] = chr(ord(stuff[i]) - 21)
        stuff[i] = chr(ord(stuff[i]) - ((i - 14) % 6))
    return stuff[14:]


data = requests.get('https://priority-static-api.nkstatic.com/storage/static/multi?appid=11&files=races/Exponential_4')
decoded = ''.join(decode(list(data.text)))
print(decoded)
