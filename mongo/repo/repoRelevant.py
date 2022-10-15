import json 
import os 
import ghMongo

def getRelevantFields(org):
    with open('../repoList/'+org+'.json', 'r') as f:
        repoList = json.load(f)
        updatedList = []
        reqKeys = ["full_name", "language", "topics",
                   "node_id", "created_at", "updated_at"]
        for repo in repoList:
            print(repo['full_name'])
            finRepo = {}
            finRepo['contributors']={}
            for key in reqKeys:
                finRepo[key] = repo.get(key)
                # print(finRepo[key])
            # break
            # finRepo['contributors'] = repoUser.baseAuthorDict(finRepo['full_name'])
            updatedList.append(finRepo)
        return updatedList

mydb=ghMongo.connect('repoStruct')
orgList = os.listdir('../repoList')
orgList = {x.replace('.json', '') for x in orgList}
orgList = sorted(orgList)
for orgName in orgList:
    # print(orgName)
    dataDict=getRelevantFields(orgName)
    if len(dataDict)>0:
        json.dump(dataDict, open('baseDict/'+orgName+'.json', 'w'))
        ghMongo.dataToPush(mydb,dataDict,orgName)
# orgName='yeebase'
