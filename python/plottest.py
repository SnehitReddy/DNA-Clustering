import plotly
import plotly.graph_objs as go
import numpy as np
import plotly.figure_factory as ff
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

filename = 'hg16.fasta'
#filename = 'DNASequences.fasta'

linkage_matrix = np.load('dataFinal/'+filename[:3]+'_final.npy')
fig = plt.figure(figsize=(25, 10))
dn = dendrogram(linkage_matrix)
plt.show()