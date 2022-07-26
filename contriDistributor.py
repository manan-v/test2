import json
import os
import matplotlib.pyplot as plt

orgList = os.listdir('starredAndSub/orgJSON/starred/')
contriDict = {}
numOfUser = []
for org in orgList:
    with open('starredAndSub/orgJSON/starred/'+org, "r") as f:
        orgDict = json.load(f)
    contriDict[org] = len(orgDict.keys())
    numOfUser.append(len(orgDict.keys()))
with open('starredAndSub/orgJSON/userDict.json', 'w') as f:
    json.dump(contriDict, f)

values, bins, bars = plt.hist(numOfUser, 30, edgecolor='white')
plt.title('Distribution of Org vs Num of Users')
plt.xlabel('Number of Users')
plt.ylabel('Number of Orgs')
plt.bar_label(bars, fontsize=8, color='black')
plt.savefig('starredAndSub/orgJSON/userDict.png')