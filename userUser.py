import networkx as nx
import matplotlib.pyplot as plt


org='reddit'
G=nx.read_edgelist('individualEdgeLists/user/'+org+'.csv.edgelist')
pos = nx.spring_layout(G, k=0.25, iterations=50)

plt.figure(figsize=(10, 6))
d = dict(G.degree)
nx.draw(G, pos=pos,
        with_labels=False,
        node_size=[30 for k in d])
for node, (x, y) in pos.items():
    plt.text(x, y, node, fontsize=10, ha='center', va='center')
# plt.show()
plt.savefig('individualEdgeLists/plot/'+org+'.png')
nx.write_gml(G,"gml/user-user-GML/"+org+'.gml')