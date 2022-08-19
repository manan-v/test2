import networkx as nx
import numpy as np
import community
import matplotlib.pyplot as plt
import matplotlib.cm as cm

# org='reddit'

def createFromEL(orgName, activityType, source='../step5_convertB_xGraphsToG_xGraphs/data/user-user-EL/', destDir='data/user-user-GML/'):
    G = nx.read_edgelist(source+orgName+'_'+activityType+'.edgelist')
    nx.write_gml(G, destDir+orgName+'_'+activityType+'.gml')

def findCommunity(org, activityType, source='data/user-user-GML/', dest='data/plots/'):
    createFromEL(org,activityType)
    G = nx.read_gml(source+org+'_'+activityType+'.gml', label='label')
    partition = community.community_louvain.best_partition(G)
    k=partition.values()
    print("No of communities found: "+str(len(set(k))))
    pos = nx.spring_layout(G, k=0.25, iterations=50)
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                        cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    plt.title("No of communities in "+org+" "+activityType+": "+str(len(set(k))))
    if activityType=='starred':
        plt.savefig(dest+org+'/'+org+'_P8_louvain.png')
        plt.clf()
    else:
        plt.savefig(dest+org+'/'+org+'_P7_louvain.png')
        plt.clf()

findCommunity('yeebase','starred')