import requests,json,sys,time
start=time.time()
sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')

import apiRobin
from helper_methods import getRandomAPIToken

def getContributorList(orgName, source='../step1_obtainRepoDetails/data/repo_details/'):
    with open(source+orgName+'.json') as f:
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
        # print(List)
        counter = counter+1
    return fullList

def filterJSON(unfilteredList):
    filteredList=[]
    del_keys=['license','owner']
    for item in unfilteredList:
        for key in del_keys:
            if key in item:
                del item[key]
        if 'node_id' in item: 
            filteredList.append(item['node_id'])
    return filteredList

def createStarredAndSub(orgName,dest='data/test/'):
    print('computing for '+orgName)
    orgFile=open(dest+orgName+'.json','w')
    orgFile.close()
    activityList=['starred','subscriptions']
    contributorList=getContributorList(orgName)
    orgData={}
    for contributor in contributorList:
        try:
            orgData[contributor] = {}
            for activity in activityList:
                orgData[contributor][activity] = filterJSON(
                    getFullJSON(contributor, activity))
            json.dump(orgData, open(dest+orgName+'.json', 'r+'))
        except Exception as e:
            print(e)
            continue
    print('completed for '+orgName+' in '+str(round(time.time()-start))+' seconds')

orgList=['yeebase']
# orgList = ['envato','salesforce']
for orgName in orgList:
    createStarredAndSub(orgName)
print("Time taken: ",round(time.time()-start))