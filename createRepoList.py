import json
import requests
from operator import itemgetter
import apiRobin
from helper_methods import getRandomAPIToken

import time
start = time.time()


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
    NodeID = list(map(itemgetter('node_id'), List))
    NodeID.sort()
    return NodeID


def createContributorDict(contributorList,activityType='starred'):
    contributorDict = {}
    count = 1
    for contributor in contributorList:
        contributorDict[contributor] = {}
        contributorDict[contributor][activityType] = getRepoForContributor(
            contributor=contributor, activityType=activityType)
        # contributorDict[contributor]['subscriptions'] = getRepoForContributor(
        #     contributor=contributor, activityType='subscriptions')
        # print(str(count)+") "+contributor)
        count += 1
        # break
    return contributorDict


def sample():
    # Sample Usage
    apiDeque = apiRobin.parseConfig('project.config')
    reqUrl = 'https://api.github.com/users/'

    json.dump(createContributorDict(getContributorList(orgName='salesforce')),
              open('similarity_matrix/salesforce.json', 'w'))

    end = time.time()
    print("Time taken: "+str(round(end-start))+" sec")
