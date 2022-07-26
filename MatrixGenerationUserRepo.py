import time
import numpy as np
import json
import os

start = time.time()


def getDictByActivity(orgName, activityType):
    with open(activityType + '/' + orgName + ".json", "r") as json_file:
        contributorDict = json.load(json_file)
    contributorList = list(contributorDict.keys())
    repoList=[]
    for contributor in contributorList:
        repoList.extend(contributorDict[contributor][activityType])
    repoList=list(set(repoList))
    contributorList.sort()
    repoList.sort()
    return contributorList, contributorDict, repoList

def createAdjMatrix(contributorList, contributorDict, repoList,activityType):
    adjMatrix = []
    for contributor in contributorList:
        curr_repoList=(contributorDict[contributor][activityType])
        innerAdjMatrix = []
        for repo in repoList:
            exist = curr_repoList.count(repo)
            if(exist):
                 innerAdjMatrix.append(1)
            else:
                 innerAdjMatrix.append(0)
        adjMatrix.append(innerAdjMatrix)
    return adjMatrix


def writeMatrixToCSV(matrix, csvName, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    csvName = directory + '/' + csvName + ".csv"
    np.savetxt(csvName, np.asarray(matrix).astype(int), delimiter=",")




def createMatrixByActivityType(org, activityType):
    org = org.replace('.json', '')
    print("starting for " + org + ", " + activityType)
    contributorList, contributorDict, repoList = getDictByActivity(
        orgName=org, activityType=activityType)
    adjMatrix = createAdjMatrix(contributorList=contributorList,
                                contributorDict=contributorDict,
                                repoList=repoList,
                                activityType=activityType)
    writeMatrixToCSV(matrix=adjMatrix, csvName=org + "_adjMatrix",
                      directory='matrix_user_repo/' + activityType + '/adjacency')



#orgList = os.listdir('starred')
orgList=["a2c.json"]
orgList.sort()
for org in orgList:
    createMatrixByActivityType(org=org, activityType='starred')
    createMatrixByActivityType(org=org, activityType='subscriptions')

end = time.time()
print("Time taken: " + str(round(end - start)) + " sec")