import os
import json
import networkx as nx
from itertools import product
from networkx.algorithms import bipartite
import requests
import json
import argparse

from joblib import Parallel, delayed
import multiprocessing
import time
import logging

logging.basicConfig(
    filename="graphs/createNetwork.log", filemode='w')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
start = time.time()
num_cores = multiprocessing.cpu_count()-1

# parser = argparse.ArgumentParser()
# parser.add_argument('--repo_file')
# parser.add_argument('--graph_dir')

# args = vars(parser.parse_args())


def createNetwork(orgName, source="repo_details/", dest="graphs/gmlFiles/"):
    with open(source+orgName+".json", 'r') as fr:
        orgDetails = json.loads(fr.read())

    B = nx.Graph()
    # orgName = args['repo_file'].split('/')[1][:-5]

    edges = []

    for repos in orgDetails['repoDetails']:
        contributor_list = []
        for contributor in repos['contributors']:
            try:
                if contributor['login'] not in contributor_list:
                    contributor_list.append(contributor['login'])
            except Exception as e:
                logger.error(str("Error for org "+orgName+": "+str(e)))
                return 0
                # pass

        # print(f"Repo : {repos['name']}, Contributor Page: {contributor_list}")
        unique_combinations = list(list(zip([repos['name']], element))
                                   for element in product(contributor_list, repeat=len([repos['name']])))

        for combinations in unique_combinations:
            edges.extend(combinations)

    left_nodes = [vals[0] for vals in edges]
    right_nodes = [vals[1] for vals in edges]

    B.add_nodes_from(left_nodes, bipartite=0)
    B.add_nodes_from(right_nodes, bipartite=1)
    B.add_edges_from(edges)

    # print(f"Network connected: {nx.is_connected(B)}")
    # print(f"Network bipartite: {nx.is_bipartite(B)}")
    # print(f"Network info: {nx.info(B)}")
    # top = nx.bipartite.sets(B)[0]
    # pos = nx.bipartite_layout(B, top)

    # Write gml to file
    nx.write_gml(B, os.path.join(dest, orgName + ".gml"))


orgList = os.listdir('repo_details')
# Strip extensions
orgList = [x.split('.')[0] for x in orgList]
orgList.sort()

logger.info(str("Computing sequentially"))
for orgName in orgList:
    createNetwork(str(orgName))

# logger.info(str("Computing parallely"))
# Parallel(n_jobs=num_cores)(delayed(createNetwork)(str(orgName)) for orgName in orgList)

end = time.time()
logger.info(str("Computing completed in "+str((end-start))+" sec"))