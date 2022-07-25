import json
import requests
from operator import itemgetter
import apiRobin
from helper_methods import getRandomAPIToken

import time, os, logging

logging.basicConfig(
    filename="starredAndSub/orgJSON/createStarredAndSub.log", filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def getContributorList(orgName, repo_details_dir='repo_details/'):
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
    apiDeque = apiRobin.parseConfig('project.config')
    reqUrl = 'https://api.github.com/users/'
    headers = getRandomAPIToken(apiDeque)
    List = requests.get(reqUrl+contributor+'/' +
                        activityType, headers=headers).json()
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
    print("comptuing for "+org)
    try:
        json.dump(createContributorDict(getContributorList(orgName=org), activityType),
                  open('starredAndSub/orgJSON/'+activityType+'/'+org+'.json', 'w'))
    except Exception as e: 
        logger.exception(e)
        logger.error(str("Error for org "+org))
        print('err found & skipped for '+org)
    end = time.time()
    logger.info(str("Time taken: "+str(round(end-start))+" sec for "+org))
    print("Time taken: "+str(round(end-start))+" sec")

orgList = os.listdir('repo_details')
orgList = [x.split('.')[0] for x in orgList]
orgList.sort()
existingOrg = os.listdir('starredAndSub/orgJSON/starred')
existingOrg = [x.split('.')[0] for x in existingOrg]
existingOrg.sort()
remOrg=list(set(orgList).symmetric_difference(set(existingOrg)))
remOrg.sort()
# orgList=['99designs']
# print("list obtained "+str(orgList))
# print("===================================")
# print("existing org "+str(existingOrg))
# print("===================================")
# print("rem org "+str(remOrg))

for org in remOrg:
    # computeSingleOrg(org,'starred')
    computeSingleOrg(org, 'subscriptions')