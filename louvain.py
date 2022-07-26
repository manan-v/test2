import networkx as nx
import numpy as np
import community
import matplotlib.pyplot as plt

G = nx.read_gml('gml/user-repo-GML/dummy.gml', label='label')
comms = community.community_louvain.best_partition(G)

unique_coms = np.unique(list(comms.values()))
cmap = {
    0: 'red',
    1: 'teal',
    2: 'black',
    3: 'orange',
    4: 'purple',
    5: 'yellow'
}

node_cmap = [cmap[v] for _, v in comms.items()]

X, Y = nx.bipartite.sets(G)
pos = dict()
pos.update((n, (1, i))
           for i, n in enumerate(X))  # put nodes from X at x=1
pos.update((n, (2, i))
           for i, n in enumerate(Y))  # put nodes from Y at x=2
nx.draw(G, pos=pos, with_labels=True,node_size = 75, alpha = 0.8, node_color=node_cmap)
plt.savefig('rough/louvain_dummy.png')
