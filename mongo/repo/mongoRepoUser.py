import pymongo 
import repoUser
import json
import os 
import time
import checkMongo

start=time.time()

def updateContributors(orgName,full_name):
    cluster = pymongo.MongoClient(
        "mongodb+srv://superman:mongo123@cluster0.4soxef8.mongodb.net/test")
    db=cluster['repoStruct']
    collection=db[orgName]

    results=collection.update_one({"full_name":full_name},{"$set":{"contributors":repoUser.baseAuthorDict(full_name)}})
    print("written to ",collection)

def getListOfRepos(orgName):
    full_name_list=[]
    with open('baseDict/'+orgName+'.json','r') as f:
        repoList=json.load(f)
        for repo in repoList:
            full_name_list.append(repo['full_name'])
    return full_name_list

def runAllOrg():
    orgList = os.listdir('baseDict')
    orgList = {x.replace('.json', '') for x in orgList}
    orgList=sorted(orgList,reverse=True)

    for orgName in orgList:
        print(orgName)
        full_name_list=getListOfRepos(orgName)
        for full_name in full_name_list:
            if(orgName != '10gen' and checkMongo.checkIfContributorsEmpty(orgName, full_name)):
                print(full_name)
                updateContributors(orgName,full_name)
            # time.sleep(5)
runAllOrg()
end=time.time()

print(int(end-start))