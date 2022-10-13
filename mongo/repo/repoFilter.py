
import json
import sys
import os
sys.path.append('../step1_obtainRepoDetails')
sys.path.append('../extra/misc')
from helper_methods import getRandomAPIToken
import apiRobin
import requests

def filterContributionByAuthor(repoList):
    for repo in range(len(repoList)):
        count = 0
        for contributor in range(len(repoList[repo]['contributors_url'])):
            # nameFromContributorList = repoList[repo]['contributors_url'][contributor]['login']
            for contribution in range(len(repoList[repo]['contribution_details'])):
                # print(repoList[repo]['contribution_details'][contribution]['author']['login'])
                # nameFromCommitDetails = repoList[repo]['contribution_details'][contribution]['author']['login']
                try:
                    nameFromContributorList = repoList[repo]['contributors_url'][contributor]['login']
                    nameFromCommitDetails = repoList[repo]['contribution_details'][contribution]['author']['login']
                    if(nameFromContributorList == nameFromCommitDetails):
                        count = count+1
                        # contributionDetailsValue = repoList[repo]['contribution_details'][contribution]
                        # repoList[repo]['contributors_url'][contributor]['contribution_details']=contributionDetailsValue
                        # print(repoList[repo]['contribution_details'][contribution])
                except:
                    pass
            print(nameFromContributorList, count)
            count = 0
        # print(repoList[repo]['contributors_url'][0]['login'])
        # if(repoList[repo]['contributors_url']['login']==commitList['author']['login']):
        #     print("YES")
        break

    return repoList


def getSHAForAllContributions(repoList):
    apiDeque = apiRobin.parseConfig('../project.config')
    headers = getRandomAPIToken(apiDeque)
    for repo in range(len(repoList)):
        print("OBTAINING COMMIT SHA FOR REPO "+repoList[repo]['full_name'])
        reqUrl = 'https://api.github.com/repos/' + \
            repoList[repo]['full_name']+'/commits'
        pageNo = 1
        commitList = []
        while(True):
            response = requests.get(
                reqUrl+'?page='+str(pageNo), headers=headers).json()
            print(reqUrl+'?page='+str(pageNo))

            if(len(response) == 0):
                break
            commitList.extend(response)
            pageNo = pageNo+1
        repoList[repo]['contribution_details'] = commitList
        break
    return repoList
