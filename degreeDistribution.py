import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from joblib import Parallel, delayed
import multiprocessing
import time
from helper_methods import orgViz

start = time.time()
num_cores = multiprocessing.cpu_count()-1
# print('Total usable number of cores: {}'.format(num_cores))

# First parameter is orgName
# Add the other parameters only if source and dest folders are different


def calcDegreeDist(orgName, source="graphs/gmlFiles/", dest="rudi-analysis/degreeDistribution/"):

    G = nx.read_gml(source+orgName+".gml", label='id')
    # nx.draw_shell(G, with_labels=True)
    # nx.draw_networkx(G,pos=nx.drawing.layout.bipartite_layout(G, G_first_partition_nodes),width=edge_widths*5)
    # plt.show()
    # plt.clf()

    degree_sequence = sorted((d for n, d in G.degree()), reverse=True)
    dmax = max(degree_sequence)

    fig = plt.figure("Degree of a random graph", figsize=(8, 8))
    # Create a gridspec for adding subplots of different sizes
    axgrid = fig.add_gridspec(5, 4)

    ax0 = fig.add_subplot(axgrid[0:3, :])
    Gcc = G.subgraph(
        sorted(nx.connected_components(G), key=len, reverse=True)[0])
    pos = nx.spring_layout(Gcc, seed=10396953)
    nx.draw_networkx_nodes(Gcc, pos, ax=ax0, node_size=20)
    nx.draw_networkx_edges(Gcc, pos, ax=ax0, alpha=0.4)
    ax0.set_title("Connected components in organisation "+orgName+"")
    ax0.set_axis_off()

    ax1 = fig.add_subplot(axgrid[3:, :2])
    ax1.plot(degree_sequence, "b-", marker="o")
    ax1.set_title("Degree Rank Plot")
    ax1.set_ylabel("Degree")
    ax1.set_xlabel("Rank")

    ax2 = fig.add_subplot(axgrid[3:, 2:])
    ax2.bar(*np.unique(degree_sequence, return_counts=True))
    ax2.set_title("Degree histogram")
    ax2.set_xlabel("Degree")
    ax2.set_ylabel("# of Nodes")

    fig.tight_layout()
    # plt.show()
    fig.savefig(dest+orgName+".png")
    plt.clf()
    print("Completed for "+orgName)


orgList = os.listdir('graphs/gmlFiles/')
# Strip extensions
orgList = [x.split('.')[0] for x in orgList]
orgList.remove('envato')

# print("Computing sequentially")
# for org in orgList:
#     calcDegreeDist(org)

print("Computing parallely")
Parallel(n_jobs=num_cores)(delayed(calcDegreeDist)(org) for org in orgList)

# print("Computing sequentially")
# for orgName in orgList:
#     orgViz(orgName)

end = time.time()
print("Computing completed in "+str(round(end-start))+" seconds")
