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
    json.dump(fullList, open('data/test/'+contributor+'.json', 'w'))
    return contributor, counter

def filterJSON(originalFile,path):
    updatedJSON=json.load(open(path+originalFile))
    print(len(updatedJSON))
    del_keys=['license','owner']
    for key in del_keys:
        for item in updatedJSON:
            if key in item:
                del item[key]
    # print('updated:',len(updatedJSON))
    json.dump(updatedJSON,open(path+originalFile,'w'))
        

orgList=['yeebase']
path='data/test/'
for org in orgList:
    contributorList=createStarredAndSub.getContributorList(org)
    reqCounter=0
    for contributor in contributorList:
        # contributor,counter=getFullJSON(contributor, 'starred')
        # print(contributor,counter)
        # reqCounter=reqCounter+counter

        filterJSON(contributor+'.json',path)
    # print("noOfContributors:",len(contributorList),"noOfRequests:",reqCounter,"timeInSecs:",round(time.time()-start))