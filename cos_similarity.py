import networkx as nx
import networkx_addon
import numpy as np

import matplotlib.pyplot as plt
import seaborn as sns

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


def fill_inner_matrix(source, user_list):
    inner_matrix = []
    for i in range(len(user_list)):
        try:
            target=user_list[i]
            # print("(source, target) is: ("+str(source)+", "+str(target)+")")
            cosine_sim = all_cosine_sim[source][target]
        except KeyError:
            cosine_sim = 1.0
        inner_matrix.append(cosine_sim)
        if(i == 100):
            break
    return inner_matrix


def fill_outer_matrix(G, user_list):
    outer_matrix = []
    for i in range(len(user_list)):
        # print("source is: "+str(i))
        outer_matrix.append(fill_inner_matrix(user_list[i], user_list))
        if(i == 100):
            break
    return outer_matrix

def show_heatmap(matrix):
    ax = sns.heatmap(matrix, linewidth=0.5, cmap="YlGnBu")
    plt.show()

G, user_nodes, user_list = read_org_graph("salesforce")
all_cosine_sim = networkx_addon.similarity.cosine(G)
print(len(user_list))
cosine_similarity_matrix = np.asarray(fill_outer_matrix(G, user_list))
print(cosine_similarity_matrix)

np.savetxt("similarity_matrix/cos_salesforce.csv",
           cosine_similarity_matrix, delimiter=",")

show_plt(cosine_similarity_matrix)
plt.clf()

end = time.time()
print("Time taken: "+str(round(end-start))+" sec")
