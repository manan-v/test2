import multiprocessing
from typing import Type
from joblib import Parallel, delayed
import json
import requests
from operator import itemgetter
import apiRobin
from helper_methods import getRandomAPIToken
import os
import time
import logging

logging.basicConfig(
    filename="similarity_matrix/createRepo.log", filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

start = time.time()

num_cores = multiprocessing.cpu_count()-1

def getContributorList(orgName, repo_details_dir='repo_details/'):
    with open(repo_details_dir+orgName) as f:
        data = json.load(f)
    contributorList = []
    for repo in data['repoDetails']:
        for contributorUrl in repo['contributors']:
            if contributorUrl['login'] not in contributorList:
                contributorList.append(contributorUrl['login'])
    contributorList.sort()
    print("no of contri are "+str(len(contributorList)))
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
    # print(type(List))
    try:
        NodeID=[att['node_id'] for att in List]
    except TypeError as e:
        logger.error(str("Error for org "+contributor+": "+str(e)))
        pass
    # print(NodeID)
    NodeID = list(map(itemgetter('node_id'), List))
    NodeID.sort()
    # print(NodeID)
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


def sample(org):
    startOrg = time.time()

    # Sample Usage
    apiDeque = apiRobin.parseConfig('project.config')
    reqUrl = 'https://api.github.com/users/'

    json.dump(createContributorDict(getContributorList(orgName=org), activityType='starred'),
              open('similarity_matrix/createRepo/starred/'+org, 'w'))
    json.dump(createContributorDict(getContributorList(orgName=org), activityType='subscriptions'),
              open('similarity_matrix/createRepo/starred/'+org, 'w'))


    endOrg = time.time()
    logger.info(str("Time taken for "+org+": "+str(round(endOrg-startOrg))+" sec"))

orgList = os.listdir('repo_details')
# orgList.sort()
# print(orgList)
# Parallel(n_jobs=num_cores)(delayed(sample)(
#     org=org) for org in orgList)
for org in orgList:
    sample(org)
end = time.time()
print("Time taken: "+str(round(end-start))+" sec")
