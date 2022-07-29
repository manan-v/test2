import json
import os
from collections import Counter

# python3 orgChecker.py - Get top k organizatinos based on public_repos
with open('githubOrgDetails.txt','r') as fr:
	data = fr.read().split("\n")

item_dict = {}

for items in data:
	if items:
		repo = json.loads(items)['public_repos']
		name = json.loads(items)['login']
		# print(name, repo)
		item_dict[name] = repo

k = Counter(item_dict)
 
# Finding 3 highest values
high = k.most_common(100)

for i in high:
    print(i[0]," :",i[1]," ")