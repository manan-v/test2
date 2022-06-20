import apiRobin
import json
import requests
import argparse
from time import sleep
import networkx as nx
import matplotlib.pyplot as plt


def getAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.rotateAPI(apiDeque)

    # Create the new header
    headers_new = {'Authorization': 'token ' + apiDeque[0]}
    print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new


def getRandomAPIToken(apiDeque):
    # Rotate the API queue
    apiDeque = apiRobin.randomRotateAPI(apiDeque)

    # Create the new header
    headers_new = {'Authorization': 'token ' + apiDeque[0]}
    # print(" ** TOKEN SELECTED: {} **".format(headers_new))
    return headers_new


def orgViz(orgName, source="graphs/gmlFiles/", dest="rudi-analysis/orgViz/"):
    G = nx.read_gml(source+orgName+".gml", label='label')
    top_nodes = set(n for n, d in G.nodes(data=True) if d['bipartite'] == 0)
    bottom_nodes = set(G) - top_nodes

    color_dict = {0: 'b', 1: 'r'}
    color_list = [color_dict[i[1]] for i in G.nodes.data('bipartite')]
    # Draw bipartite graph
    pos = dict()
    pos.update((n, (1, i)) for i, n in enumerate(
        bottom_nodes))  # put nodes from X at x=1
    pos.update((n, (2, i))
               for i, n in enumerate(top_nodes))  # put nodes from Y at x=2

    # nx.draw(G, pos=nx.drawing.layout.bipartite_layout(G, top_nodes),width=0.5,node_color=color_list)
    nx.draw(G, pos=pos, with_labels=True,
            node_color=color_list, edge_color="g", width=0.5, font_color="black")
    plt.figtext(0.1, 0.01, "User", ha="left", fontsize=12, bbox={
                "facecolor": "red", "alpha": 1, "pad": 5}, color="black")
    plt.figtext(0.5, 0.01, orgName, ha="center", fontsize=12, bbox={
                "facecolor": "green", "alpha": 1, "pad": 5}, color="black")
    plt.figtext(0.9, 0.01, "Repo", ha="right", fontsize=12, bbox={
                "facecolor": "blue", "alpha": 1, "pad": 5}, color="black")
    # plt.show()
    plt.savefig(dest+orgName+".png")
    plt.clf()
    print("Visualised for "+orgName)
