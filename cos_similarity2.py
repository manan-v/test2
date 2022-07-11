import json
from collections import Counter
from createStarredAndSub import getContributorList
import math

import time
start = time.time()


def readList(orgName, file_directory='similarity_matrix/'):
    with open(file_directory+orgName+'.json') as f:
        data = json.load(f)

    return data


def mergedContributorList(orgName, contributorList):
    mergedContributorList = {}
    data = readList(orgName)
    # print(data['0x4d31-sfdc']['starred'])
    for contributor in contributorList:
        nodeID = []
        mergedContributorList[contributor] = {}
        for type in data[contributor]:
            nodeID.extend(data[contributor][type])
        mergedContributorList[contributor] = nodeID

    return mergedContributorList


def cos_methodI(a, b):
    # count word occurrences
    a_vals = Counter(a)
    b_vals = Counter(b)

    # convert to word-vectors
    words = list(a_vals.keys() | b_vals.keys())
    a_vect = [a_vals.get(word, 0) for word in words]
    b_vect = [b_vals.get(word, 0) for word in words]

    # find cosine
    len_a = sum(av*av for av in a_vect) ** 0.5
    len_b = sum(bv*bv for bv in b_vect) ** 0.5
    dot = sum(av*bv for av, bv in zip(a_vect, b_vect))
    cosine = dot / (len_a * len_b)

    return cosine


def cos_methodII(c1, c2):
    terms = set(c1).union(c2)
    dotprod = sum(c1.get(k, 0) * c2.get(k, 0) for k in terms)
    magA = math.sqrt(sum(c1.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(c2.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)


contributorList = getContributorList('salesforce')
json.dump(mergedContributorList('salesforce', contributorList=contributorList),
          open('similarity_matrix/merged_salesforce.json', 'w'))

data = readList('merged_salesforce', file_directory='similarity_matrix/')
errCount = 0
totCount = 0
nonZeroCosSim = 0
for source in contributorList:
    a = data[source]
    for target in contributorList:
        if target is not source:
            totCount += 1
            b = data[target]
            try:
                if(cos_methodII(Counter(a), Counter(b))) > 0:
                    nonZeroCosSim += 1
            except:
                errCount += 1

print("nonZeroCosSim pairs: "+str(nonZeroCosSim))
print("error pairs: "+str(errCount))
print("total pairs: "+str(totCount))
print("error perc: "+str(round((errCount/totCount)*100))+"%")

end = time.time()
print("Time taken: "+str(round(end-start))+" sec")