import json
import requests
from operator import itemgetter
import sys 
sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')

import apiRobin
from helper_methods import getRandomAPIToken

import time, os, logging

logging.basicConfig(
    filename="createStarredAndSub.log", filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


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

def getRepoForContributor(contributor, activityType):
    apiDeque = apiRobin.parseConfig('../project.config')
    reqUrl = 'https://api.github.com/users/'
    headers = getRandomAPIToken(apiDeque)
    counter=1
    while(True):
        currentReq = requests.get(reqUrl+contributor+'/' +
                            activityType+'?page='+str(counter), headers=headers).json()
        List = requests.get('https://api.github.com/users/Torsten85/starred?page=1', headers=headers).json()
        print(contributor, reqUrl+contributor+'/' +
              activityType+'?page='+str(counter),"length: "+str(len(currentReq)))
        if(len(currentReq)==0):
            break
        else:
            counter=counter+1
            del_key1 = 'license'
            del_key2 = 'owner'
            for items in List:
                if del_key1 in items:
                    del items[del_key1]
                if del_key2 in items:
                    del items[del_key2]
    try: 
        NodeID = list(map(itemgetter('node_id'), List))
        NodeID.sort()
        return NodeID
    except Exception as e: 
        logger.exception(e)
        logger.error(str("Error for contri "+contributor))
        return 1

def createContributorDict(contributorList,activityType):
    contributorDict = {}
    for contributor in contributorList:
        contributorDict[contributor] = {}
        resp = getRepoForContributor(
            contributor=contributor, activityType=activityType)
        if(resp != 1):
            contributorDict[contributor][activityType] = resp
    return contributorDict

def computeSingleOrg(org, activityType):
    start = time.time()
    print("computing for "+org)
    try:
        json.dump(createContributorDict(getContributorList(orgName=org), activityType),
                  open('step2_obtainMemberActivity/data/starredAndSub/orgJSON/'+activityType+'/'+org+'.json', 'w'))
    except Exception as e: 
        logger.exception(e)
        logger.error(str("Error for org "+org))
        print('err found & skipped for '+org)
    end = time.time()
    logger.info(str("Time taken: "+str(round(end-start))+" sec for "+org))
    print("Time taken: "+str(round(end-start))+" sec")

# orgList = os.listdir('repo_details')
# orgList = [x.split('.')[0] for x in orgList]
# orgList.sort()
# existingOrg = os.listdir('starredAndSub/orgJSON/starred')
# existingOrg = [x.split('.')[0] for x in existingOrg]
# existingOrg.sort()
# remOrg=list(set(orgList).symmetric_difference(set(existingOrg)))
# remOrg.sort()
# orgList=['99designs']
# print("list obtained "+str(orgList))
# print("===================================")
# print("existing org "+str(existingOrg))
# print("===================================")
# print("rem org "+str(remOrg))
orgList=['yeebase']

for org in orgList:
    computeSingleOrg(org,'starred')
    # computeSingleOrg(org, 'subscriptions')