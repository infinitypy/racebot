import requests
import json 


raceid = 'ku7sesrm'
raceurl = 'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_' + raceid + '.json'

data = requests.get(raceurl).json()

d = json.loads(data["data"])
raw = []
times = []
names = []
scoreoffset = []
nameoffset = []

for i in range(99):
    raw.append(str(d["scores"]["equal"][i]))
for i in range(99):
    scoreoffset.append(int(raw[i].find('score')))
    nameoffset.append(raw[i].find('metadata'))


for i in range(99):
    times.append(raw[i][scoreoffset[i]+8:scoreoffset[i]+17])
print(times[49])