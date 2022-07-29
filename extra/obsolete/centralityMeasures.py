import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


def draw(G, pos, measures, measure_name):

    nodes = nx.draw_networkx_nodes(G, pos, node_size=250, cmap=plt.cm.plasma,
                                   node_color=list(measures.values()),
                                   nodelist=measures.keys())
    nodes.set_norm(mcolors.SymLogNorm(linthresh=0.01, linscale=1, base=10))
    # labels = nx.draw_networkx_labels(G, pos)
    edges = nx.draw_networkx_edges(G, pos)

    plt.title(measure_name)
    plt.colorbar(nodes)
    plt.axis('off')
    plt.show()


# G = nx.karate_club_graph()
G = nx.read_gml("graphs/envato.gml", label='id')
pos = nx.spring_layout(G, seed=675)

# close_centrality = nx.closeness_centrality(G)
# deg_centrality = nx.degree_centrality(G)
# bet_centrality = nx.betweenness_centrality(G, normalized=True, endpoints=False)
# pr = nx.pagerank(G, alpha=0.8)

# print(deg_centrality)
# draw(G, pos, nx.betweenness_centrality(G), 'Betweenness Centrality')
draw(G, pos, nx.pagerank(G, alpha=0.8), 'Page Rank')
