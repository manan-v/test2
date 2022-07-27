import networkx as nx
import numpy as np
import community
import matplotlib.pyplot as plt
import matplotlib.cm as cm

org='reddit'
G = nx.read_gml('gml/user-user-GML/'+org+'.gml', label='label')
partition = community.community_louvain.best_partition(G)
k=partition.values()
# print(type(k))
print("No of communities found: "+str(len(set(k))))
# print(G)
# draw the graph
pos = nx.spring_layout(G, k=0.25, iterations=50)
# color the nodes according to their partition
cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                       cmap=cmap, node_color=list(partition.values()))
nx.draw_networkx_edges(G, pos, alpha=0.5)
plt.title("No of communities in "+org+" : "+str(len(set(k))))
# plt.show()
# plt.show()
plt.savefig('individualEdgeLists/plot/louvain'+org+'.png')
