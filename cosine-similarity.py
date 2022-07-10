import networkx as nx 
import networkx_addon

G = nx.read_gml("graphs/gmlFiles/"+"salesforce"+".gml", label='id')
cosineSim=networkx_addon.similarity.cosine(G)
# s=networkx_addon.similarity.simrank(G)

source=0
target=0

try: 
    cosine_sim=cosineSim[source][target]
except KeyError:
    cosine_sim=1.0

print(cosine_sim)