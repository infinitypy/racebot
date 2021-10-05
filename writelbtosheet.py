import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
import json
import datetime
import sheets

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
client = gspread.authorize(creds)
sheet = client.open_by_key('16WGnLuUGxalfNEFND-YUfplhXIZMxJ1zzkESc3ISgn4')
fulldata = sheet.worksheet('main')


all_races = {}
all_ids = [cell.value for cell in sheets.race_info.range(2, 3, 147, 3)]


def lb(race_num):
    times = []
    newtimes = []
    complete = []

    race_id = all_ids[race_num - 1]
    race_url = 'https://priority-static-api.nkstatic.com/storage/static/appdocs/11/leaderboards/Race_' + race_id + '.json'
    data = requests.get(race_url).json()
    entries = json.loads(data["data"])['scores']['equal']
    stuff = [(entry['metadata'].split(',')[0], entry['score'], entry['userID']) for entry in entries]

    for i in range(len(stuff)):
        if str(stuff[i][1])[-1] == '9':
            times.append(str(stuff[i][1])[0:-1] + '8')
        else:
            times.append(str(stuff[i][1]))

    for i in range(len(times)):
        newtimes.append(str(datetime.timedelta(milliseconds=999999999 - int(times[i])))[3:-3])
    
    for  i in range(len(stuff)):
        complete.append(stuff[i][2] + ',' + stuff[i][0] + ',' + newtimes[i])

    return complete


testing = lb(146)

for i in range(len(testing)):
    fulldata.update_cell(i+2, 2, testing[i])


#for z in range(len(145)):
#    testing = lb(z+1)
#    for i in range(len(testing)):
#        fulldata.update_cell(i+2, z+2, testing[i])