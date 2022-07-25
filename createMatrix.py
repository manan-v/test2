import createRepoList, cos_similarity2
import numpy as np
import json
import os

from joblib import Parallel, delayed
import multiprocessing
num_cores = multiprocessing.cpu_count()-1
import argparse
# from helper_methods import buzzer
import time
start=time.time()

def createOrgJSON(orgName, contributorDict, activityType, directory='matrix/orgJSON'):
    directory=directory+'/'+activityType
    if not os.path.exists(directory):
        os.makedirs(directory)
    json.dump(contributorDict,open(directory+'/'+orgName+'.json', 'w'))

def getDictByActivity(orgName,activityType,repo_details_dir='repo_details/'):
    contributorList=createRepoList.getContributorList(orgName,repo_details_dir)
    contributorDict=createRepoList.createContributorDict(contributorList,activityType=activityType)
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
    np.savetxt(csvName,np.asarray(matrix).astype(int), delimiter=",")

def createMatrixByActivityType(org,activityType):
    org=org.replace('.json','')
    print("starting for "+org+", "+activityType)
    contributorList, contributorDict=getDictByActivity(orgName=org,activityType=activityType)
    createOrgJSON(orgName=org,contributorDict=contributorDict,activityType=activityType)    
    adjMatrix=createAdjMatrix(contributorList=contributorList,contributorDict=contributorDict,activityType=activityType)
    cos_similarity2.show_heatmap(vmax=1,matrix=adjMatrix,directory='matrix/'+activityType+'/adjacency/',filename=org+'_adjMatrixHeatmap.png')
    
    writeMatrixToCSV(matrix=adjMatrix,csvName=org+"_adjMatrix",directory='matrix/'+activityType+'/adjacency')
    countMatrix=createCountMatrix(contributorList=contributorList,contributorDict=contributorDict,activityType=activityType)
    cos_similarity2.show_heatmap(vmax=np.max(countMatrix),matrix=countMatrix,directory='matrix/'+activityType+'/count/', filename=org+'_countMatrixHeatmap.png')
    writeMatrixToCSV(matrix=countMatrix,csvName=org+"_countMatrix",directory='matrix/'+activityType+'/count')

def createAllMatrixForOrg(org,activityList):
    for activity in activityList:
        createMatrixByActivityType(org,activity)
    # Parallel(n_jobs=num_cores)(delayed(createMatrixByActivityType)(org=org,activityType=activity) for activity in activityList)

# orgList = os.listdir('repo_details')

# Small orgs
orgList=['a2c','elevatedrails','mangos','lrug','yeebase']

# orgList=['mangos']
# orgList = ['reddit']


# Big orgs
# orgList = ['reddit', 'yahoo', 'php', 'vim-ruby','git']


# orgList = ['yahoo']
# orgList = ['php']
# orgList = ['Khan','envato']
# orgList = ['git']

# parser = argparse.ArgumentParser()
# parser.add_argument('--org')
# args = vars(parser.parse_args())
# orgList.append(args['org'])
activityList=['starred','subscriptions']
# activityList = ['subscriptions']


for org in orgList:
    startForOrg = time.time()
    createAllMatrixForOrg(org=org,activityList=activityList)
    endForOrg = time.time()
    print("done for "+org+" in "+str(round(endForOrg-startForOrg))+" sec")


end=time.time()
print("Total Time taken: "+str(round(end-start))+" sec")
# buzzer(file='rough/buzzer.wav')
