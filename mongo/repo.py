import requests
import json 
import sys
import os

sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')

def getRepoListForAllOrg():
    import apiRobin
    from helper_methods import getRandomAPIToken
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    reqUrl='https://api.github.com/orgs/'

    orgList = os.listdir('../step1_obtainRepoDetails/data/repo_details')
    orgList = {x.replace('.json', '') for x in orgList}
    orgList=sorted(orgList)

    for org in orgList:
        pageNo=1
        repoList=[]
        while(True):
            response = requests.get(reqUrl+org+'/repos?page='+str(pageNo),headers=headers).json()
            if(len(response)==0):
                break
            repoList.extend(response)
            pageNo=pageNo+1
        with open('repoList/'+org+'.json','w') as f:
            json.dump(repoList,f)
        print(org, len(repoList))
        # print(org)

def getRelevantFields(org):
    with open('repoList/'+org+'.json','r') as f: 
        repoList=json.load(f)
        updatedList=[]
        # repo['org']=org
        reqKeys = ['full_name','language', 'topics', 'node_id','created_at','updated_at' ]
        for d in repoList:
            repo = {}
            for key in reqKeys:
                repo[key]=d.get(key)
            repo.update(repo)
            updatedList.append(repo)
            # updatedList.extend(repo)
        # print(updatedList)
    return updatedList

# import ghMongo
# orgList = os.listdir('repoList')
# orgList = {x.replace('.json', '') for x in orgList}
# orgList = sorted(orgList)
# for org in orgList:
#     repoList=getRelevantFields(org)
#     ghMongo.connectAndPush(repoList)

getRepoListForAllOrg()