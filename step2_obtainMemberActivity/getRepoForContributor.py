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
        # print(contributor, len(List), counter, type(List))
        fullList.extend(List)
        counter = counter+1
    return contributor, counter, fullList

orgList=['yeebase']
for org in orgList:
    contributorList=createStarredAndSub.getContributorList(org)
    reqCounter=0
    for contributor in contributorList:
        contributor,counter,fullList=getFullJSON(contributor, 'starred')
        json.dump(fullList,open('data/test/'+contributor+'.json','w'))
        print(contributor,counter)
        reqCounter=reqCounter+counter
    print("noOfContributors:",len(contributorList),"noOfRequests:",reqCounter,"timeInSecs:",round(time.time()-start))