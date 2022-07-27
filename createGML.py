import networkx as nx 
import pandas as pd 
import matplotlib.pyplot as plt


def createGML(csvFile, destDir='latest-matrix/gml'):
    # initialise
    df = pd.read_csv('latest-matrix/matrix/'+csvFile+'.csv')
    B = nx.Graph()
    edges = []

    # add users and repos
    repos=df.columns.values.tolist()
    repos.pop(0)
    users = df[df.columns[0]].values.tolist()
    B.add_nodes_from(users,bipartite=0)
    B.add_nodes_from(repos, bipartite=1)

    # populate edges list
    userC = 0
    for user in users:
        # print(user)
        repo_list=[]
        repoC=1
        for repo in repos: 
            if(df.iloc[userC, repoC]==1):
                edges.append([user,repo])
            repoC=repoC+1
        userC=userC+1
        
    # add edges
    for u,r in edges:
        B.add_edges_from(([(u, r)]))

    # rearrange like a bipartite graph
    # X, Y = nx.bipartite.sets(B)
    # pos = dict()
    # pos.update((n, (1, i)) for i, n in enumerate(X))  # put nodes from X at x=1
    # pos.update((n, (2, i)) for i, n in enumerate(Y))  # put nodes from Y at x=2
    
    # # draw graph
    # nx.draw(B, pos=pos,with_labels=True)
    # plt.show()

    # export as gml
    gmlFile=csvFile.replace('.csv','')
    # print(gmlFile)
    nx.write_gml(B,destDir+'/'+gmlFile+'.gml')


# createGML('10gen.csv')
