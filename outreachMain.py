import requests as r
from pprint import pprint as pp
from datetime import datetime
import json
from Work import parseMailings
from time import sleep

runTime = datetime.now()

start = 5001
end = 6000
timerange = str(start) + '..' + str(end)
reportDate ='2019-08-05'
runDate = datetime.utcnow().strftime("%m-%d-%YT%H.%M.%S")
token = 'https://api.outreach.io/oauth/token'
mailings = 'https://api.outreach.io/api/v2/mailings' #filter[createdAt]=2019-08-06..2019-08-06& #page[limit]=1000' #&filter[createdAt]=' + reportDate
prospects = 'https://api.outreach.io/api/v2/prospects'#sort=-createdAt' #page[limit]=1000&filter[id]=3001..4000'
sequences = 'https://api.outreach.io/api/v2/sequences'
tasks = 'https://api.outreach.io/api/v2/tasks'
#callDispositions = 'https://api.outreach.io/api/v2/callDispositions'
calls = 'https://api.outreach.io/api/v2/calls'
users = 'https://api.outreach.io/api/v2/users'
accounts = 'https://api.outreach.io/api/v2/accounts' #page[limit]=1000&filter[id]='


def getFileName(callType):
    dataFolder = r'C:\Users\JefferyMcCain\OneDrive - Databrains\Documents\PythonFiles\outreach\DataFiles'
    if callType == 'prospects':
        fileName = dataFolder + '\Prospects\ProspectData_' + runDate + '.json'
    elif callType == 'mailings':
        fileName = dataFolder + '\Mailings\MailingsData_' + runDate + '.json'
    elif callType == 'sequences':
        fileName = dataFolder + '\Sequences\SequencesData_' + runDate + '.json'
    elif callType == 'tasks':
        fileName = dataFolder + '\Tasks\TasksData_' + runDate + '.json'
    elif callType == 'callDispositions':
        fileName = dataFolder + '\CallDispositions\Data_' + runDate + '.json'
    elif callType == 'calls':
        fileName = dataFolder + '\Calls\CallsData_' + runDate + '.json'
    elif callType == 'users':
        fileName = dataFolder + '\\Users\\Users' + runDate + '.json'
    elif callType == 'accounts':
        fileName = dataFolder + '\Accounts\AccountData_' + runDate + '.json'
    return fileName


def getMaxIDNumber(apiCallType, headers):
    print('Getting Max ID Number')
    urlAddition = '?sort=-createdAt'
    url = apiCallType + urlAddition
    print(runDate + ' - API Call Running - ' + apiCallType)
    call = r.get(url, headers=headers)
    if call.status_code == 200:
        print(runDate + ' - API Call Successful')
        data = call.json()
        data = data['data']
        idNumber = data[0]['id']
    return idNumber



def apiCall(callType, headers, fileName):
    print(runDate + ' - API Call Running - ' + callType)
    call = r.get(callType, headers=headers)
    print(call.status_code)
    print(call.content)
    if call.status_code == 504:
        print('Call Failed - retrying: ' + callType)
        sleep(10)
        apiCall(callType, headers, fileName)
    if call.status_code == 200:
        print(runDate + ' - API Call Successful')
        data = call.json()
        fileN = getFileName(fileName)
        with open(fileN, 'w') as file:
            json.dump(data, file)
            print(fileN)
            print('API Call Complete')
        return data
    else:
        print(runDate + ' - API Call Unsuccessful - ' + callType)

def loopThroughData(start, maxAccount, callVariable, headers, callType):
    urlAdditions = '?page[limit]=1000&[filter]id='
    while start < maxAccount:
        end = start + 499
        timerange = str(start) + '..' + str(end)
        url = callVariable + urlAdditions + timerange
        data = apiCall(url, headers, callType)
        parse = parseMailings.ParseJSON()
        if callType == 'prospects':
            parse.parseProspects(data)
        elif callType == 'mailings':
            parse.parseMailings(data)
        elif callType == 'sequences':
          parse.parseSequences(data)
        elif callType == 'tasks':
            parse.parseTasks(data)
        elif callType == 'calls':
            parse.parseCalls(data)
        elif callType == 'users':
            parse.parseUsers(data)
        elif callType == 'accounts':
            parse.parseAccounts(data)
        print('***Range ' + timerange + ' has been completed***')
        sleep(5)
        start = start + 500
        print('New starting value is: ' + str(start))
