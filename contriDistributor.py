import json, os

orgList = os.listdir('starredAndSub/orgJSON/starred/')
contriDict = {}
for org in orgList: 
    print(org)
    with open('starredAndSub/orgJSON/starred/'+org,"r") as f: 
        orgDict=json.load(f)

    contriDict[org]=len(orgDict.keys())
with open('starredAndSub/orgJSON/userDict.json', 'w') as f:
    json.dump(contriDict, f)
