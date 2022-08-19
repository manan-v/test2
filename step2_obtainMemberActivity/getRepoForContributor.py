import requests
import json 

import sys 
sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')

import apiRobin
from helper_methods import getRandomAPIToken

import time
start=time.time()

def getContributorList(orgName, repo_details_dir='../step1_obtainRepoDetails/data/repo_details/'):
    with open(repo_details_dir+orgName+'.json') as f:
        data = json.load(f)
    contributorList = []
    for repo in data['repoDetails']:
        for contributorUrl in repo['contributors']:
            if contributorUrl['login'] not in contributorList:
                contributorList.append(contributorUrl['login'])
    contributorList.sort()
    return contributorList

def getFullJSON(contributor, activityType):
    apiDeque = apiRobin.parseConfig('../project.config')
    reqUrl = 'https://api.github.com/users/'
    headers = getRandomAPIToken(apiDeque)
    counter = 1
    fullList=[]
    while(True):
        List = requests.get(reqUrl+contributor+'/'+activityType +
                            '?page='+str(counter), headers=headers).json()
        if(len(List) < 1):
            break
        fullList.extend(List)
        counter = counter+1
    # json.dump(fullList, open('data/test/'+contributor+'.json', 'w'))
    return fullList

def filterJSON(unfilteredList):
    nodeIDList=[]
    del_keys=['license','owner']
    for item in unfilteredList:
        for key in del_keys:
            if key in item:
                del item[key]
        if 'node_id' in item: 
            nodeIDList.append(item['node_id'])
    return nodeIDList
        
def createStarredAndSub(orgList):
    path='data/test/'
    activityList=['starred','subscriptions']
    for org in orgList:
        contributorList=getContributorList(org)
        orgData={}
        for contributor in contributorList:
            orgData[contributor] = {}
            for activity in activityList:
                orgData[contributor][activity] = filterJSON(getFullJSON(contributor, activity))
                print(contributor,activity)
            json.dump(orgData,open('data/test/'+org+'.json','r+'))

orgList = ['yeebase']
createStarredAndSub(orgList)
print("Time taken: ",round(time.time()-start))