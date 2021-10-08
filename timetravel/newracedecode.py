import requests


def decode(data):
    data = data.encode()
    for i in range(len(data)-14):
        data[i+14] = data[i+14] - 21
        data[i+14] = data[i+14] - ((i-28)%6)
        return data.decode()

data = requests.get('https://static-api.nkstatic.com/nkapi/skusettings/4db0c10e1647310be1eb71b77f2df364.json').json()
print(data)