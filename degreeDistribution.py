import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json 
import operator

import time
start=time.time()
import logging

logging.basicConfig(
    filename="rudi-analysis/degreeDistribution/nonSingularOccurence-degreeDistribution.log", filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def plotGraph(orgName, userDegree, repoDegree, userDict,repoDict,G, dest='latest-matrix-plots/'):
    
    if not os.path.exists(dest+orgName):
        os.makedirs(dest+orgName)

    # Organisation
    # X, Y = nx.bipartite.sets(G)
    # pos = dict()
    # pos.update((n, (1, i))
    #            for i, n in enumerate(X))  # put nodes from X at x=1
    # pos.update((n, (2, i))
    #            for i, n in enumerate(Y))  # put nodes from Y at x=2
    # pos = nx.spring_layout(G, k=0.15, iterations=30)
    # nx.draw(G)
    # print(G)
    # # labels={}
    # # labels=nx.get_node_attributes(G,'bipartite')
    # # nx.draw_networkx_labels(G,labels)
    # # plt.show()
    # plt.savefig(dest+orgName+'/'+orgName+'_bipartite.png')
    # plt.clf()
    
    # P1
    # x,y=np.unique(repoDegree,return_counts=True)
    # # print(repoDegree)
    # plt.plot(x,y,'o-')
    # plt.yscale('log')

    # plt.xlabel("Degree")
    # plt.ylabel("Number of repos")
    # plt.title("P1: Degree distribution (B_w) for repos: "+orgName)
    # # plt.show()
    # plt.savefig(dest+orgName+'/'+orgName+'_P1.png')
    # plt.clf()
    
    # # P2
    # x, y = np.unique(userDegree, return_counts=True)
    # plt.plot(x, y, 'o-')
    # plt.yscale('log')
    # plt.xlabel("Degree")
    # plt.ylabel("Number of users")
    # plt.title("P2: Degree distribution (B_w) for users: "+orgName)
    # # plt.show()
    # plt.savefig(dest+orgName+'/'+orgName+'_P2.png')
    # plt.clf()

    # # P5
    # allDegree=userDegree+repoDegree
    # x, y = np.unique(allDegree, return_counts=True)
    # plt.plot(x, y, 'o-')
    # plt.yscale('log')
    # plt.xlabel("Degree")
    # plt.ylabel("Number of users")
    # plt.title("P5: Degree distribution: "+orgName)
    # # plt.show()
    # plt.savefig(dest+orgName+'/'+orgName+'_P5.png')
    # plt.clf()

    # # Users with num of repo in desc plot 
    # user=list(userDict.keys())
    # deg=list(userDict.values())
    # # print(user)
    # plt.figure(figsize=(300, 10))
    # plt.plot(user, deg, 'o-')
    # # plt.figure(figsize=(20, 10))
    # # plt.yscale('log')
    # plt.xlabel("Which user")
    # plt.xticks(rotation=90)
    # plt.ylabel("Number of repos starred")
    # plt.title("Desc order of user(starred): "+orgName)
    # # plt.show()
    # path = dest+orgName+'/'+orgName+'_userDesc.png'
    # print(path)
    # plt.savefig(path)
    # plt.clf()

    # Repos with num of users in desc plot
    repo = list(repoDict.keys())
    deg = list(repoDict.values())
    # print(user)
    plt.figure(figsize=(300, 10))
    plt.plot(repo, deg, 'o-')
    # plt.figure(figsize=(20, 10))
    # plt.yscale('log')
    plt.xlabel("Which repo",size=2)
    plt.xticks(rotation=90)
    plt.ylabel("Number of users starring this repo")
    plt.title("Desc order of repo(starred): "+orgName)
    # plt.show()
    path = dest+orgName+'/'+orgName+'_repoDesc.png'
    print(path)
    plt.savefig(path)
    plt.clf()

def calcDegreeDist(orgName, source="graphs/gmlFiles/"):
    try:
        G = nx.read_gml(source+orgName+".gml", label='label')
        print(G)
        users = [x for x, y in G.nodes(data=True) if y['bipartite'] == 0]
        repos = [x for x, y in G.nodes(data=True) if y['bipartite'] == 1]
        repoDict={}
        userDict={}
        repoDegree=[]
        userDegree=[]
        for repo in repos:
            deg = G.degree(repo)
            repoDegree.append(deg)
            repoDict[repo]=deg
        for user in users:
            deg = G.degree(user)
            userDegree.append(deg)
            userDict[user]=deg
        print(len(userDegree),len(repoDegree))
        return G, userDegree, repoDegree, repoDict, userDict
    except Exception as e:
        print("errr "+orgName)
        logger.error(str("Error for org "+orgName+": "+str(e)))
    
def calcDegreeAndPlot(org):
    # destFolder = "gml/user-repo-GML/"
    G, userDegree, repoDegree,repoDict, userDict = calcDegreeDist(
        orgName=org, source='gml/user-repo-GML/')
    repoDict=dict(sorted(repoDict.items(), key=operator.itemgetter(1), reverse=True))
    with open('rough/'+org+'_repoDict.json','w') as f:
        json.dump(repoDict,f)
    userDict=dict(sorted(userDict.items(), key=operator.itemgetter(1), reverse=True))
    with open('rough/'+org+'_userDict.json','w') as f:
        json.dump(userDict,f)
    plotGraph(org, userDegree, repoDegree,userDict,repoDict, G)

# org='99designs'
# destFolder = "gml/user-repo-GML/"
# logger.info(str("Computing sequentially"))
orgList = os.listdir('gml/user-repo-GML')
for org in orgList:
    org=org.replace('.gml','')
    org = 'reddit'

    calcDegreeAndPlot(org)
    break
# G,userDegree, repoDegree =calcDegreeDist(orgName=org, source='gml/user-repo-GML/',dest=destFolder)

# plotGraph(org, userDegree, repoDegree, G)

# end = time.time()
# logger.info(str("Computing completed in "+str(round(end-start))+" seconds for "+org))