from operator import eq
import json

import time
start = time.time()

threshold = 5
with open('similarity_matrix/merged_salesforce.json') as f:
    data = json.load(f)
print("recieved data")
with open('similarity_matrix/salesforce.json') as f:
    contributorList = json.load(f)
print("recieved userList")
similar_users = {}

for source in contributorList:
    similar_users[source] = {}
    userA = data[source]
    for target in contributorList:
        if source != target:
            # print("calculating for source: "+source+" & target: "+target)
            userB = data[target]
            res = sum(map(eq, userA, userB))
            if(res >= 5):
                print("found similar pair: ("+source+", "+target+")")
                similar_users[source] = target

empty_keys = [k for k, v in similar_users.items() if not v]
for k in empty_keys:
    del similar_users[k]

json.dump(similar_users,
          open('similarity_matrix/countBasedSimilarity_salesforce.json', 'w'))

end = time.time()
print("Time taken: "+str(round(end-start))+" sec")