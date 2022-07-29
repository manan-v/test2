import networkx as nx
import numpy as np
import networkx_addon

import seaborn as sns
import matplotlib.pyplot as plt

import time
start = time.time()


def read_org_graph(orgName):
    G = nx.read_gml("graphs/gmlFiles/"+orgName+".gml", label='id')
    type = nx.get_node_attributes(G, "bipartite")
    user_nodes = [node for node in G.nodes if type[node] == 1]
    # repo_nodes = [node for node in G.nodes if type[node] == 0]

    user_G = nx.Graph(G.subgraph(user_nodes))
    # repo_G = nx.Graph(G.subgraph(repo_nodes))

    user_list = []
    for key in user_G.nodes:
        user_list.append(key)
    return G, user_nodes, user_list

def calculate_similarity(source, target):
    simrank=nx.simrank_similarity(G, source, target)
    return simrank

def fill_inner_matrix(G, source, user_list,source_index,matrix):
    # inner_matrix = []
    for i in range(len(user_list)):
        target=user_list[i]
        target_index=i

        # print("(source, target) is: ("+str(source)+", "+str(target)+")")
        # print("source_index: "+str(source_index))
        # print("target_index: "+str(target_index))

        # inner_matrix.append(s[source][target])

        matrix[source_index][target_index]=calculate_similarity(source,target)
        print(matrix[source_index][target_index])
        if(i == 1):
            break
    return matrix


def fill_sim_matrix(G, user_list):
    sim_matrix = [[0]*len(user_list)]*len(user_list)
    for i in range(len(user_list)):
        # print("source is: "+str(i))
        # sim_matrix.append(fill_inner_matrix(G, source=user_list[i], user_list=user_list,source_index=i))
        sim_matrix = fill_inner_matrix(G, source=user_list[i], source_index=i, user_list=user_list, matrix=sim_matrix)
        if(i == 1):
            break
    return sim_matrix


def show_heatmap(matrix):
    ax = sns.heatmap(matrix, linewidth=0.5, cmap="YlGnBu")
    plt.show()

G, user_nodes, user_list = read_org_graph("salesforce")
# s = networkx_addon.similarity.simrank(G)
# print("here")
outer_matrix = fill_sim_matrix(G, user_list)
# print(type(outer_matrix))
similarity_matrix = np.asarray(outer_matrix)
# print(type(similarity_matrix))

# show_heatmap(similarity_matrix)

np.savetxt("similarity_matrix/simrank_salesforce.csv",
           similarity_matrix, delimiter=",")

end = time.time()
print("Time taken: "+str(round(end-start))+" sec")
