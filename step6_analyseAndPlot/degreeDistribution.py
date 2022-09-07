import os
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import json
import operator

import time
start = time.time()


def genIndiPlots(orgName, userDict, repoDict, activityType, dest='data/plots/'):
    # Users with num of repo in desc plot
    user = list(userDict.keys())
    deg = list(userDict.values())
    # print(user)
    plt.figure(figsize=(300, 10))
    plt.plot(user, deg, 'o-')
    # plt.figure(figsize=(20, 10))
    plt.xlabel("Which user")
    plt.xticks(rotation=90)
    plt.ylabel("Number of repos")
    plt.title("Desc order of user: "+orgName)
    # plt.show()
    path = dest+orgName
    path = path.replace('_subscriptions', '').replace('_starred', '')
    orgName = orgName.replace('_subscriptions', '').replace('_starred', '')

    # print(path)
    if activityType == 'subscriptions':
        plt.savefig(path+'/'+orgName+'_P9_'+activityType+'_userDesc.png')
    elif activityType == 'starred':
        plt.savefig(path+'/'+orgName+'_P11_'+activityType+'_userDesc.png')
    plt.clf()
    print("[Y] Generated IndiUser for "+orgName)

    # Repos with num of users in desc plot
    repo = list(repoDict.keys())
    deg = list(repoDict.values())
    # print(user)
    plt.figure(figsize=(300, 10))
    plt.plot(repo, deg, 'o-')
    # plt.figure(figsize=(20, 10))
    plt.xlabel("Which repo", size=2)
    plt.xticks(rotation=90)
    plt.ylabel("Number of users on this repo")
    plt.title("Desc order of repo: "+orgName)
    # plt.show()
    path = dest+orgName
    path = path.replace('_subscriptions', '').replace('_starred', '')
    orgName = orgName.replace('_subscriptions', '').replace('_starred', '')
    # print(path)
    if activityType == 'subscriptions':
        plt.savefig(path+'/'+orgName+'_P10_'+activityType+'_repoDesc.png')
    elif activityType == 'starred':
        plt.savefig(path+'/'+orgName+'_P12_'+activityType+'_repoDesc.png')
    plt.clf()
    print("[Y] Generated IndiRepo for "+orgName)


def genP1toP4(orgName, userDegree, repoDegree, dest='data/plots/'):
    plt.figure()
    if('_subscriptions' in orgName):
        orgName = orgName.replace("_subscriptions", "")

        # P1
        x, y = np.unique(repoDegree, return_counts=True)
        # print(repoDegree)
        plt.plot(x, y, 'o-')
        plt.xlabel("Degree")
        plt.ylabel("Number of repos")
        plt.title("P1: Degree distribution (B_w) for repos: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P1.png')
        plt.clf()
        print("[Y] Generated P1")

        # P1 - log
        x, y = np.unique(repoDegree, return_counts=True)
        # print(repoDegree)
        plt.plot(x, y, 'o-')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel("Degree")
        plt.ylabel("Number of repos")
        plt.title("P1: Degree distribution (B_w) for repos: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P1_log.png')
        plt.clf()
        print("[Y] Generated P1-log")

        # P2
        x, y = np.unique(userDegree, return_counts=True)
        plt.plot(x, y, 'o-')
        plt.xlabel("Degree")
        plt.ylabel("Number of users")
        plt.title("P2: Degree distribution (B_w) for users: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P2.png')
        plt.clf()
        print("[Y] Generated P2")

        # P2 - log
        x, y = np.unique(userDegree, return_counts=True)
        plt.plot(x, y, 'o-')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel("Degree")
        plt.ylabel("Number of users")
        plt.title("P2: Degree distribution (B_w) for users: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P2_log.png')
        plt.clf()
        print("[Y] Generated P2-log")

        # # P5
        # allDegree=userDegree+repoDegree
        # x, y = np.unique(allDegree, return_counts=True)
        # plt.plot(x, y, 'o-')

        # plt.xlabel("Degree")
        # plt.ylabel("Number of nodes (user+repo)")
        # plt.title("P5: Degree distribution (G_w): "+orgName)
        # # plt.show()
        # plt.savefig(dest+orgName+'/'+orgName+'_P5.png')
        # plt.clf()
        # print("[Y] Generated P5")

    else:
        orgName = orgName.replace("_starred", "")

        # P3
        x, y = np.unique(repoDegree, return_counts=True)
        # print(repoDegree)
        plt.plot(x, y, 'o-')
        plt.xlabel("Degree")
        plt.ylabel("Number of repos")
        plt.title("P3: Degree distribution (B_s) for repos: "+orgName)
        # plt.show()
        # path = dest+orgName+'/'+orgName+'_P3.png'
        # print(path)
        plt.savefig(dest+orgName+'/'+orgName+'_P3.png')
        plt.clf()
        print("[Y] Generated P3")

        # P3 - log
        x, y = np.unique(repoDegree, return_counts=True)
        # print(repoDegree)
        plt.plot(x, y, 'o-')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel("Degree")
        plt.ylabel("Number of repos")
        plt.title("P3: Degree distribution (B_s) for repos: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P3_log.png')
        plt.clf()
        print("[Y] Generated P3-log")

        #  P4
        x, y = np.unique(userDegree, return_counts=True)
        plt.plot(x, y, 'o-')
        plt.xlabel("Degree")
        plt.ylabel("Number of users")
        plt.title("P4: Degree distribution (B_s) for users: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P4.png')
        plt.clf()
        print("[Y] Generated P4")

        #  P4 - log
        x, y = np.unique(userDegree, return_counts=True)
        plt.plot(x, y, 'o-')
        plt.yscale('log')
        plt.xscale('log')
        plt.xlabel("Degree")
        plt.ylabel("Number of users")
        plt.title("P4: Degree distribution (B_s) for users: "+orgName)
        # plt.show()
        plt.savefig(dest+orgName+'/'+orgName+'_P4_log.png')
        plt.clf()
        print("[Y] Generated P4-log")

        # # P6
        # allDegree = userDegree+repoDegree
        # x, y = np.unique(allDegree, return_counts=True)
        # plt.plot(x, y, 'o-')

        # plt.xlabel("Degree")
        # plt.ylabel("Number of nodes (user+repo)")
        # plt.title("P6: Degree distribution (G_s): "+orgName)
        # # plt.show()
        # plt.savefig(dest+orgName+'/'+orgName+'_P6.png')
        # plt.clf()
        # print("[Y] Generated P6")


def P7toP8(orgName, activityType, source='../step5_convertB_xGraphsToG_xGraphs/data/user-user-EL/', dest='data/plots/'):
    # P8
    G = nx.read_edgelist(source+orgName+'_'+activityType+'.edgelist')
    pos = nx.spring_layout(G, k=0.25, iterations=50)
    plt.figure(figsize=(10, 6))
    d = dict(G.degree)
    nx.draw(G, pos=pos,
            with_labels=False,
            node_size=[30 for k in d])
    for node, (x, y) in pos.items():
        plt.text(x, y, node, fontsize=10, ha='center', va='center')
        # plt.show()
    if activityType == 'starred':
        plt.savefig(dest+orgName+'/'+orgName+'_P8_G_s'+'.png')
        plt.clf()
    else:
        plt.savefig(dest+orgName+'/'+orgName+'_P7_G_w'+'.png')
        plt.clf()


def calcDegreeDist(orgName, activityType, source):
    try:
        G = nx.read_gml(source+orgName+"_"+activityType+".gml", label='label')
        print(G)
        users = [x for x, y in G.nodes(data=True) if y['bipartite'] == 0]
        repos = [x for x, y in G.nodes(data=True) if y['bipartite'] == 1]
        repoDict = {}
        userDict = {}
        repoDegree = []
        userDegree = []
        for repo in repos:
            deg = G.degree(repo)
            repoDegree.append(deg)
            repoDict[repo] = deg
        for user in users:
            deg = G.degree(user)
            userDegree.append(deg)
            userDict[user] = deg
        print(len(userDegree), len(repoDegree))
        return userDegree, repoDegree, repoDict, userDict
    except Exception as e:
        print("errr "+orgName)


def calcDegreeAndPlot(org):
    userDegree, repoDegree, repoDict, userDict = calcDegreeDist(
        org, activityType, source='../step4_convertMatrixToB_xGraphs/data/gml/user-repo-GML/')
    repoDict = dict(
        sorted(repoDict.items(), key=operator.itemgetter(1), reverse=True))
    # path = 'latest-matrix-plots/'+org
    # path=path.replace('_sub','')
    activityType = 'starred'
    if '_subscriptions' in org:
        activityType = 'subscriptions'
    elif '_starred' in org:
        activityType = 'starred'
    path = 'latest-matrix-plots/' + \
        org.replace('_subscriptions', '').replace('_starred', '')
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.exists(path+'/indiDicts'):
        os.makedirs(path+'/indiDicts')
    with open(path+'/indiDicts/'+org+'_repoDict.json', 'w') as f:
        json.dump(repoDict, f)
    userDict = dict(
        sorted(userDict.items(), key=operator.itemgetter(1), reverse=True))
    with open(path+'/indiDicts/'+org+'_userDict.json', 'w') as f:
        json.dump(userDict, f)
    genP1toP4(org, userDegree, repoDegree)
    genIndiPlots(org, userDict, repoDict, activityType)


def allForOrg(org):
    org = org.replace('.gml', '')
    calcDegreeAndPlot(org)
    # org = org+'_sub'
    # calcDegreeAndPlot(org)

# org='99designs'
# destFolder = "gml/user-repo-GML/"
# logger.info(str("Computing sequentially"))
# orgList = os.listdir('latest-matrix/gml')
# for org in orgList:
#     org = 'reddit'
#     allForOrg(org)
#     break


org = '10gen'
# sOrg=org+'_sub'
allForOrg(org)
# allForOrg(sOrg)

# end=time.time()
# print("Total Time taken: "+str(round(end-start))+" sec")
