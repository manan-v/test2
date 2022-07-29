import time
import numpy as np
import json
import os

start = time.time()


def getDictByActivity(orgName, activityType):
    with open('starredAndSub/orgJSON/' + activityType + '/' + orgName + ".json", "r") as json_file:
        contributorDict = json.load(json_file)
    contributorList = list(contributorDict.keys())
    contributorList.sort()
    # print(contributorDict)
    return contributorList, contributorDict


def checkIfCommonRepo(contributorA, contributorB, contributorDict, activityType):
    repoOfA = contributorDict[contributorA][activityType]
    flag = 0
    commonBool = False
    numOfCommonRepos = 0
    try:
        repoOfB = contributorDict[contributorB][activityType]
    except:
        print("no repo for " + contributorB + ", " + activityType)
        flag = 1
    # print(flag)
    if (flag == 0):
        if (any(check in repoOfA for check in repoOfB)):
            commonRepos = list(set(repoOfA).intersection(repoOfB))
            numOfCommonRepos = len(commonRepos)
            commonBool = True
    else:
        commonBool = False
        numOfCommonRepos = 0
    return commonBool, numOfCommonRepos


def createAdjMatrix(contributorList, contributorDict, activityType):
    adjMatrix = []
    for contributorA in contributorList:
        innerAdjMatrix = []
        for contributorB in contributorList:
            commonBool, numOfCommonRepos = checkIfCommonRepo(
                contributorA, contributorB, contributorDict, activityType=activityType)
            if (commonBool == True):
                innerAdjMatrix.append(1)
            else:
                innerAdjMatrix.append(0)
        adjMatrix.append(innerAdjMatrix)
    return adjMatrix


def createCountMatrix(contributorList, contributorDict, activityType):
    countMatrix = []
    for contributorA in contributorList:
        innerCountMatrix = []
        for contributorB in contributorList:
            commonBool, numOfCommonRepos = checkIfCommonRepo(
                contributorA, contributorB, contributorDict, activityType=activityType)
            innerCountMatrix.append(numOfCommonRepos)
        countMatrix.append(innerCountMatrix)
    return countMatrix


def writeMatrixToCSV(matrix, csvName, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    csvName = directory + '/' + csvName + ".csv"
    np.savetxt(csvName, np.asarray(matrix).astype(int), delimiter=",")


def createMatrixByActivityType(org, activityType):
    org = org.replace('.json', '')
    print("starting for " + org + ", " + activityType)
    contributorList, contributorDict = getDictByActivity(
        orgName=org, activityType=activityType)
    adjMatrix = createAdjMatrix(contributorList=contributorList,
                                contributorDict=contributorDict, activityType=activityType)
    writeMatrixToCSV(matrix=adjMatrix, csvName=org + "_adjMatrix",
                     directory='matrix/' + activityType + '/adjacency')
    countMatrix = createCountMatrix(
        contributorList=contributorList, contributorDict=contributorDict, activityType=activityType)
    writeMatrixToCSV(matrix=countMatrix, csvName=org +
                                                 "_countMatrix", directory='matrix/' + activityType + '/count')


activityList = ['starred']
orgList = os.listdir('repo_details')
orgList.sort()
for org in orgList:
    createMatrixByActivityType(org=org, activityType='starred')
    createMatrixByActivityType(org=org, activityType='subscriptions')

end = time.time()
print("Time taken: " + str(round(end - start)) + " sec")