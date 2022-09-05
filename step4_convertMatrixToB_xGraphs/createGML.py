import networkx as nx 
import pandas as pd

def createFromCSV(orgName, activityType, source='../step3_convertJSONToMatrix/data/matrix_user_repo/', destDir='data/gml/user-repo-GML'):
    try: 
        # initialise
        df = pd.read_csv(source+activityType+'/'+orgName+'.csv')
        B = nx.Graph()
        edges = []

        # add users and repos
        repos = df.columns.values.tolist()
        repos.pop(0)
        users = df[df.columns[0]].values.tolist()
        B.add_nodes_from(users, bipartite=0)
        B.add_nodes_from(repos, bipartite=1)

        # populate edges list
        userC = 0
        for user in users:
            # print(user)
            repo_list = []
            repoC = 1
            for repo in repos:
                if(df.iloc[userC, repoC] == 1):
                    edges.append([user, repo])
                repoC = repoC+1
            userC = userC+1

        # add edges
        for u, r in edges:
            B.add_edges_from(([(u, r)]))
        gmlPath = destDir+'/'+orgName+'_'+activityType+'.gml'
        print(gmlPath)
        nx.write_gml(B, gmlPath)
    except:
        print("err for "+orgName)

def createFromEL(orgName, activityType, source='gml/user-user-EL/', destDir='gml/user-user-GML/'):
    G = nx.read_edgelist(source+orgName+'_'+activityType+'.edgelist')
    nx.write_gml(G, destDir+orgName+'_'+activityType+'.gml')

createFromCSV('10gen','starred')
createFromCSV('10gen', 'subscriptions')
