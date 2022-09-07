import networkx as nx
import os 

def calcDegreeDist(orgName, activityType, source):
    G = nx.read_gml(source+orgName+"_"+activityType+".gml", label='label')
    # print(G)
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
    print(orgName+", "+activityType+", "+str(len(userDegree))+", "+str(len(repoDegree)))


print("orgName, activityType, users, repos")
dirList=os.listdir('/home/parth/Desktop/Code/projects/github-recommendation-project/step4_convertMatrixToB_xGraphs/data/gml/user-repo-GML')
dirList.sort()
for file in dirList: 
    orgName=file.split("_")[0]
    activityType=file.split("_")[1].split(".")[0]
    calcDegreeDist(orgName,activityType,'../../step4_convertMatrixToB_xGraphs/data/gml/user-repo-GML/')