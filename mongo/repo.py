import requests
import json 
import sys
import os
sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')

import apiRobin
from helper_methods import getRandomAPIToken

def getSHAForAllCommits(repoList):
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    for repo in range(len(repoList)):
        print("OBTAINING COMMIT SHA FOR REPO "+repoList[repo]['full_name'])
        reqUrl = 'https://api.github.com/repos/'+repoList[repo]['full_name']+'/commits'
        pageNo = 1
        commitList = []
        while(True):
            response = requests.get(reqUrl+'?page='+str(pageNo), headers=headers).json()
            print(reqUrl+'?page='+str(pageNo))

            if(len(response) == 0):
                break
            commitList.extend(response)
            pageNo = pageNo+1
        repoList[repo]['contribution_details']=commitList
    return repoList

def getContributorForRepo(repoList):
    print("OBTAINING CONTRIBUTOR LIST FOR REPOS")
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    for repo in range(len(repoList)):
        print(repoList[repo]['full_name'])
        reqUrl=repoList[repo]['contributors_url']
        pageNo=1
        contributorList=[]
        while(True):
            response = requests.get(reqUrl+'?page='+str(pageNo),headers=headers).json()
            if(len(response) == 0):
                break
            contributorList.extend(response)
            pageNo = pageNo+1
        for contributor in range(len(contributorList)):
            contributorList[contributor]['contribution_details']=''
        repoList[repo]['contributors_url']=contributorList
        # break
    return repoList
        # break

def getRepoListForAllOrg():
    
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    reqUrl='https://api.github.com/orgs/'

    orgList = os.listdir('../step1_obtainRepoDetails/data/repo_details')
    orgList = {x.replace('.json', '') for x in orgList}
    orgList=sorted(orgList)

    for org in orgList:
        pageNo=1
        repoList=[]
        # Get primary data
        while(True):
            response = requests.get(reqUrl+org+'/repos?page='+str(pageNo),headers=headers).json()
            if(len(response)==0):
                break
            repoList.extend(response)
            pageNo=pageNo+1
        
        # Get list of contributors
        # repoList=getContributorForRepo(repoList)

        # Get SHA for all commits of a particular repo
        repoList=getSHAForAllCommits(repoList)

        with open('repoList/'+org+'.json','w') as f:
            json.dump(repoList,f)
        print(org, len(repoList))
        break
        # print(org)

def getRelevantFields(org):
    with open('repoList/'+org+'.json','r') as f: 
        repoList=json.load(f)
        updatedList=[]
        # repo['org']=org
        reqKeys = ["full_name","language", "topics", "node_id","created_at","updated_at" ]
        for d in repoList:
            repo = {}
            for key in reqKeys:
                repo[key]=d.get(key)
            repo.update(repo)
            updatedList.append(repo)
            # updatedList.extend(repo)
        print(updatedList)
    return updatedList

# import ghMongo
# orgList = os.listdir('repoList')
# orgList = {x.replace('.json', '') for x in orgList}
# orgList = sorted(orgList)
# for org in orgList:
#     repoList=getRelevantFields(org)
#     ghMongo.connectAndPush(repoList)

getRepoListForAllOrg()

# getRelevantFields('yeebase')
# print(list)