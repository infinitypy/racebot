import requests
import json 
import datetime
import sheets



def getleaderboard(racenum, first, last):

    raceid = str(sheets.race_info.cell(racenum + 1, 3).value)
    raceurl = 'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_' + raceid + '.json'

    data = requests.get(raceurl).json()

    entries = json.loads(data["data"])['scores']['equal']
    stuff = []
    stuff = [(entry['metadata'].split(',')[0], entry['score'], entry['userID']) for entry in entries]
    times = []

    for i in range(99):
        if str(stuff[i][1])[-1] == '9':
            times.append(str(stuff[i][1])[0:-1] + '8')
        else:
            times.append(str(stuff[i][1]))



    leaderboard = ''
    for i in range(last-first+1):
        leaderboard += "\n" + str(i+first) + ' ' + str(datetime.timedelta(seconds=(999999999-int(times[i+first-1]))/1000))[3:-4] + ' ' + str(stuff[i+first-1][0])
    return(str(leaderboard))


#lb for 145 and maybe some other races is fucked
#getleaderboard(145, 1, 5)
#print(sheets.race_info.cell(145 + 1, 3).value)