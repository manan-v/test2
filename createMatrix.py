import createRepoList
import numpy as np

from joblib import Parallel, delayed
import multiprocessing
num_cores = multiprocessing.cpu_count()-1

import time
start=time.time()

import os

def getDictByActivity(orgName,activityType,repo_details_dir='repo_details/'):
    contributorList=createRepoList.getContributorList(orgName,repo_details_dir)
    contributorDict=createRepoList.createContributorDict(contributorList,activityType)
    return contributorList, contributorDict

def checkIfCommonRepo(contributorA, contributorB, contributorDict,activityType):
    repoOfA=contributorDict[contributorA][activityType]
    repoOfB = contributorDict[contributorB][activityType]
    if(any(check in repoOfA for check in repoOfB)):
        commonRepos=list(set(repoOfA).intersection(repoOfB))
        numOfCommonRepos=len(commonRepos)
        commonBool=True
    else:
        commonBool=False
        numOfCommonRepos=0
    return commonBool,numOfCommonRepos

def createAdjMatrix(contributorList, contributorDict, activityType):
    adjMatrix=[]
    for contributorA in contributorList:
        innerAdjMatrix=[]
        for contributorB in contributorList:
            commonBool,numOfCommonRepos=checkIfCommonRepo(contributorA,contributorB,contributorDict,activityType=activityType)
            if(commonBool==True):
                innerAdjMatrix.append(1)
            else:
                innerAdjMatrix.append(0)
        adjMatrix.append(innerAdjMatrix)
    return adjMatrix

def createCountMatrix(contributorList, contributorDict, activityType):
    countMatrix=[]
    for contributorA in contributorList:
        innerCountMatrix=[]
        for contributorB in contributorList:
            commonBool,numOfCommonRepos=checkIfCommonRepo(contributorA,contributorB,contributorDict,activityType=activityType)
            innerCountMatrix.append(numOfCommonRepos)
        countMatrix.append(innerCountMatrix)
    return countMatrix

def writeMatrixToCSV(matrix,csvName,directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
    csvName=directory+'/'+csvName+".csv"
    np.savetxt(csvName,np.asarray(matrix), delimiter=",")

def createMatrixByActivityType(org,activityType):
    startForOrg=time.time()
    print("starting for "+org)
    contributorList, contributorDict=getDictByActivity(orgName=org,activityType=activityType)
    adjMatrix=createAdjMatrix(contributorList=contributorList,contributorDict=contributorDict,activityType=activityType)
    writeMatrixToCSV(matrix=adjMatrix,csvName=org+"_adjMatrix",directory='matrix/'+activityType+'/adjacency')
    countMatrix=createCountMatrix(contributorList=contributorList,contributorDict=contributorDict,activityType=activityType)
    writeMatrixToCSV(matrix=countMatrix,csvName=org+"_countMatrix",directory='matrix/'+activityType+'/count')
    endForOrg=time.time()
    print("done for "+org+" in "+str(round(endForOrg-startForOrg))+" sec")


orgList = ['yeebase', 'salesforce']
for org in orgList:
    createMatrixByActivityType(org,'starred')
    break
# Parallel(n_jobs=num_cores)(delayed(createMatrixByActivityType)(org=org,activityType='starred') for org in orgList)

end=time.time()
print("Total Time taken: "+str(round(end-start))+" sec")