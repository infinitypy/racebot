import requests
import json 


raceid = 'ku7sesrm'
raceurl = 'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_' + raceid + '.json'

data = requests.get(raceurl).json()

entries = json.loads(data["data"])['scores']['equal']
stuff = [(entry['metadata'].split(',')[0], entry['score'], entry['userID']) for entry in entries]
print(stuff)
