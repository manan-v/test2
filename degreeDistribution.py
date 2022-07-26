import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

import time
start=time.time()
import logging

logging.basicConfig(
    filename="rudi-analysis/degreeDistribution/nonSingularOccurence-degreeDistribution.log", filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


def plotGraph(orgName, userDegree, repoDegree, G, dest='plots/'):
    
    if not os.path.exists(dest+orgName):
        os.makedirs(dest+orgName)

    # Organisation
    X, Y = nx.bipartite.sets(G)
    pos = dict()
    pos.update((n, (1, i))
               for i, n in enumerate(X))  # put nodes from X at x=1
    pos.update((n, (2, i))
               for i, n in enumerate(Y))  # put nodes from Y at x=2
    nx.draw(G, pos=pos, with_labels=True)
    # plt.show()
    plt.savefig(dest+orgName+'/'+orgName+'_bipartite.png')
    plt.clf()
    
    # P1
    x,y=np.unique(repoDegree,return_counts=True)
    plt.plot(x,y,'o-')
    plt.xlabel("Number of repos")
    plt.ylabel("Degree")
    plt.title("P1: Degree distribution (B_w) for repos: "+orgName)
    # plt.show()
    plt.savefig(dest+orgName+'/'+orgName+'_P1.png')
    plt.clf()
    
    # P2
    x, y = np.unique(userDegree, return_counts=True)
    plt.plot(x, y, 'o-')
    plt.xlabel("Number of users")
    plt.ylabel("Degree")
    plt.title("P2: Degree distribution (B_w) for users: "+orgName)
    # plt.show()
    plt.savefig(dest+orgName+'/'+orgName+'_P2.png')
    plt.clf()

    # P5
    allDegree=userDegree+repoDegree
    x, y = np.unique(allDegree, return_counts=True)
    plt.plot(x, y, 'o-')
    plt.xlabel("Number of users")
    plt.ylabel("Degree")
    plt.title("P5: Degree distribution: "+orgName)
    # plt.show()
    plt.savefig(dest+orgName+'/'+orgName+'_P5.png')
    plt.clf()

def calcDegreeDist(orgName, source="graphs/gmlFiles/", dest="gml/user-repo-GML/"):
    try:
        G = nx.read_gml(source+orgName+".gml", label='label')
        users = [x for x, y in G.nodes(data=True) if y['bipartite'] == 0]
        repos = [x for x, y in G.nodes(data=True) if y['bipartite'] == 1]
        
        repoDegree=[]
        userDegree=[]
        for repo in repos:
            repoDegree.append(int(G.degree(repo)))
        for user in users:
            userDegree.append(G.degree(user))
        
        # print(repoDegree)
        # print(userDegree)
        return G, userDegree, repoDegree
    except Exception as e:
        print("errr")
        logger.error(str("Error for org "+orgName+": "+str(e)))
    

org='dummy'
destFolder = "gml/user-repo-GML/"
logger.info(str("Computing sequentially"))

G,userDegree, repoDegree =calcDegreeDist(orgName=org, source='gml/user-repo-GML/',dest=destFolder)

plotGraph(org, userDegree, repoDegree, G)

end = time.time()
logger.info(str("Computing completed in "+str(round(end-start))+" seconds for "+org))