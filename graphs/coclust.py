import networkx as nx
from sklearn.cluster import SpectralClustering
from matplotlib import pyplot as plt
import pandas as pd
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.decomposition import PCA
import os, argparse

# Sample run: python3 coclust.py --orgName salesforce

parser = argparse.ArgumentParser()
parser.add_argument('--orgName')
args = vars(parser.parse_args())

orgName = args['orgName']
fh = open(orgName+".tsv", 'wb')
# Load GML file and export as TSV using networkX
G = nx.read_gml(orgName+".gml", label='id')
nx.write_edgelist(G, fh)
print("Done writting to TSV!")


#input file
fin = open(orgName+".tsv", "rt")
#output file to write the result to
fout = open(orgName+".csv", "wt")
#for each line in the input file
for line in fin:
	#read replace the string and write to output file
	fout.write(line.replace(' ', ','))
#close input and output files
fin.close()
fout.close()
print("Done converting to CSV!")
os.remove(orgName+".tsv")

raw_df = pd.read_csv(orgName+".csv")
raw_df = raw_df.iloc[:, :-1]
# Preprocessing the data to make it visualizable
# Scaling the Data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(raw_df)
# Normalizing the Data
X_normalized = normalize(X_scaled)
# Converting the numpy array into a pandas DataFrame
X_normalized = pd.DataFrame(X_normalized)
# Reducing the dimensions of the data
pca = PCA(n_components=2)
X_principal = pca.fit_transform(X_normalized)
X_principal = pd.DataFrame(X_principal)
X_principal.columns = ['P1', 'P2']


# Building the clustering model
spectral_model_rbf = SpectralClustering(n_clusters=2, affinity='rbf')
# Training the model and Storing the predicted cluster labels
labels_rbf = spectral_model_rbf.fit_predict(X_principal)
# Visualizing the clustering
plt.scatter(X_principal['P1'], X_principal['P2'],
            c=SpectralClustering(n_clusters=2, affinity='rbf') .fit_predict(X_principal), cmap=plt.cm.winter)
# plt.show()
plt.savefig(orgName+".png")
print("Plot stored as "+orgName+".png!")
