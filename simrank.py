from asyncore import read
import networkx as nx
import numpy as np

import time

from networkx_addon import similarity
start = time.time()

def read_org_graph(orgName):
    G = nx.read_gml("graphs/gmlFiles/"+orgName+".gml", label='id')
    type=nx.get_node_attributes(G,"bipartite")
    user_nodes= [node for node in G.nodes if type[node]==0]
    # repo_nodes = [node for node in G.nodes if type[node] == 1]

    user_G=nx.Graph(G.subgraph(user_nodes))
    # repo_G = nx.Graph(G.subgraph(repo_nodes))

    user_list=[]
    for key in user_G.nodes:
        user_list.append(key)
    return G,user_nodes,user_list

def fill_inner_matrix(G, source, user_list):
    inner_matrix=[]
    for i in range(len(user_list)):
        print("(source, target) is: ("+str(source)+", "+str(i)+")")
        inner_matrix.append(nx.simrank_similarity(G,source,user_list[i]))
        # if(i==3):
        #     break
    return inner_matrix

def fill_outer_matrix(G,user_list):
    outer_matrix=[]
    for i in range(len(user_list)):
        # print("source is: "+str(i))
        outer_matrix.append(fill_inner_matrix(G,i,user_list))
        # if(i==2):
        #     break
    return outer_matrix

G,user_nodes,user_list=read_org_graph("salesforce")
outer_matrix=fill_outer_matrix(G,user_list)
similarity_matrix=np.asarray(outer_matrix)

np.savetxt("similarity_matrix/salesforce.csv",similarity_matrix,delimiter=",")

end = time.time()
print("Time taken: "+str(round(end-start))+" sec")
