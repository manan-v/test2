import numpy as np
from matplotlib import pyplot as plt

data = np.genfromtxt('similarity_matrix/cos2_salesforce.csv',delimiter=",")
clipped_data = data[(data > 0.1)]
nonZero=data[(data>0)]
print(clipped_data.size*(100)/data.size)
fig = plt.figure(figsize=(10, 7))

plt.hist(clipped_data, bins=[0, 0.1, 0.2, 0.30,
                  0.40, 0.50, 0.60, 0.70,
                  0.80, 0.90, 1.00])

plt.title("Salesforce entire")

# show plot
plt.savefig('similarity_matrix/cosSimDist_Salesforce_above0.1.png',dpi=600)
