import networkx as nx 
import pandas as pd 
import matplotlib.pyplot as plt

def createGML(csvFile, destDir='gml/user-repo-GML'):
    df = pd.read_csv('matrix/starred/adjacency/'+csvFile)
    # print(df.iloc[[0,1]])

    B = nx.Graph()
    repos=df.columns.values.tolist()
    repos.pop(0)
    users = df[df.columns[0]].values.tolist()
    # repos.pop(0)

    B.add_nodes_from(users,bipartite=0)
    B.add_nodes_from(repos, bipartite=1)

    print(users)
    print(repos)

createGML('dummy.csv')
