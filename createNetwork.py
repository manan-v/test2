import os
import json
import networkx as nx
from itertools import product
from networkx.algorithms import bipartite

with open('repo_details/salesforce.json','r') as fr:
	orgDetails = json.loads(fr.read())

B = nx.Graph()

edges = []
for repos in orgDetails['repoDetails']:
	contributor_list = []
	for contributor in repos['contributors']:
		if contributor['login'] not in contributor_list:
			contributor_list.append(contributor['login'])

	# print(f"Repo : {repos['name']}, Contributor Page: {contributor_list}")
	unique_combinations = list(list(zip([repos['name']], element))
                           for element in product(contributor_list, repeat = len([repos['name']])))

	for combinations in unique_combinations:
		edges.extend(combinations)

left_nodes = [vals[0] for vals in edges]
right_nodes = [vals[1] for vals in edges]

B.add_nodes_from(left_nodes, bipartite=0)
B.add_nodes_from(right_nodes, bipartite=1)
B.add_edges_from(edges)

print(f"Network connected: {nx.is_connected(B)}")
print(f"Network bipartite: {nx.is_bipartite(B)}")
# top = nx.bipartite.sets(B)[0]
# pos = nx.bipartite_layout(B, top)
nx.write_gml(B, "salesforce.gml")