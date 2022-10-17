import requests
import json 
import sys
import os
sys.path.append('../../step1_obtainRepoDetails')
sys.path.append('../../extra/misc')

import apiRobin
from helper_methods import getRandomAPIToken

import repoUser

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
            contributorList[contributor]['contribution_details']=[]
        repoList[repo]['contributors_url']=contributorList
        break
    return repoList
        # break

def getRepoListForAllOrg():
    
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    reqUrl='https://api.github.com/orgs/'

    # orgList = os.listdir('../step1_obtainRepoDetails/data/repo_details')
    # orgList = {x.replace('.json', '') for x in orgList}
    # orgList=sorted(orgList)

    orgList=['Kadaza']

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
        repoList=getContributorForRepo(repoList)

        with open('../repoList/'+org+'.json','w') as f:
            json.dump(repoList,f)
        print(org, len(repoList))
        # break
        # print(org)

getRepoListForAllOrg()
# import ghMongo
# orgList = os.listdir('repoList')
# orgList = {x.replace('.json', '') for x in orgList}
# orgList = sorted(orgList)
# for org in orgList:
#     repoList=getRelevantFields(org)
#     ghMongo.connectAndPush(repoList)

# getRepoListForAllOrg()
# orgName='yeebase'
# finalJSON=getRelevantFields(orgName)
# print(finalJSON)
# with open('baseDict/'+orgName+'.json','w') as f:
#     json.dump(finalJSON,f)

# print(list)