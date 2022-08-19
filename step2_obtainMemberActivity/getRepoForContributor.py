import createStarredAndSub
import requests
import json 

import sys 
sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')

import apiRobin
from helper_methods import getRandomAPIToken

import time
start=time.time()

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
    json.dump(fullList, open('data/test/'+contributor+'.json', 'w'))
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
        
orgList=['yeebase']
path='data/test/'
activityList=['starred']
for org in orgList:
    contributorList=createStarredAndSub.getContributorList(org)
    reqCounter=0
    for contributor in contributorList:
        for activity in activityList:
            fullList=getFullJSON(contributor, activity)
            nodeIDList=filterJSON(fullList)
            print(contributor,nodeIDList)