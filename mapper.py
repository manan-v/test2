import networkx as nx
import os
import sys
import random
import json

edges = []
nodes = []

with open(sys.argv[1],'r') as fr:
	content = fr.read().split('\n')

	for vals in content:
		if vals:
			nodes.append(vals.split(' ')[0])
			nodes.append(vals.split(' ')[1])

mapper_dict = dict()
i = 0
for word in nodes:
    if word not in mapper_dict:
        mapper_dict[str(i)] = word
        i += 1

final_edges = []
for vals in content:
	if vals:
		s = vals.split(' ')[0]
		d = vals.split(' ')[1]
		#print(mapper_dict[s], mapper_dict[d])


print("JSON dumped to file")
with open(sys.argv[1] + '.mapper.json', 'w') as outfile:
    json.dump(mapper_dict, outfile)
