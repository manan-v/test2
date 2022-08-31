
from networkx.algorithms import bipartite
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np 
import math


def calcClusteringCoefficient(orgName, activityType, source='../step4_convertMatrixToB_xGraphs/data/gml/user-repo-GML/', dest='data/plots/'):
    B=nx.read_gml(source+orgName+'_'+activityType+'.gml')
    c=bipartite.clustering(B)
    cValues=list(c.values())
    avgClustCoeff=sum(cValues)/len(cValues)
    bins = np.linspace(math.ceil(min(cValues)),
                       math.floor(max(cValues)),
                       100)
    plt.xlim([0, 1.01])
    plt.hist(cValues, bins=bins, alpha=0.5)
    plt.title("Avg Clustering Coefficient for ("+orgName+', '+activityType+'): '+str(avgClustCoeff))
    plt.xlabel('Clustering Coefficient')
    plt.ylabel('Number of nodes')
    # plt.show()
    path = dest+orgName+'/'+orgName+'_P14_'+activityType+'_clusteringCoefficient.png'
    # print(path)
    plt.savefig(path)
    plt.clf()
    print("[Y] Generated Clustering Coefficient Graph")

calcClusteringCoefficient('10gen','starred')
calcClusteringCoefficient('10gen', 'subscriptions')
