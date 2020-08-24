import numpy
import matplotlib.pyplot as plt
import pickle
from scipy.cluster import hierarchy
import scipy.spatial.distance as ssd


def read_fromfile(name):
    with open('data/'+name+'.pkl', 'rb') as fp:
        return pickle.load(fp)

def read_fasta(fp):
        name, seq = None, []
        for line in fp:
            line = line.rstrip()
            if line.startswith(">"):
                if name: yield (name, ''.join(seq))
                name, seq = line, []
            else:
                seq.append(line)
        if name: yield (name, ''.join(seq))


def init_clusters():
    clusters=[list(range(num_records))]

def split_cluster():
    max_c = None
    max_sum = -1
    max_i=-1
    max_j=-1

    for c in clusters:
        sum=0
        max_di=-1
        max_dj=-1
        for i in range(len(c)):
            for j in range(i + 1, len(c)):
                d = get_distance(c[i],c[j])
                if(d>max_d):
                    max_di = c[i]
                    max_dj = c[j]
                sum= sum + d
        if sum > max_sum:
            max_c, max_sum, max_i, max_j = clusters.index(c), sum , max_di, max_dj

    avg_dist = max_sum / ((len(clusters[max_c]))*(len(clusters[max_c])-1)/2)
    sub_cluster_1=[]
    sub_cluster_2=[]
    for e in clusters[max_c]:
        if(get_distance(e,max_i)>get_distance(e,max_j)):
            sub_cluster_1.append(e);
        else:
            sub_cluster_2.append(e);

    orginal_cluster = clusters[max_c];
    clusters[max_c].clear()
    clusters.append(sub_cluster_1)
    clusters.append(sub_cluster_2)

    linkage_matrix[count, 0] = len(clusters) - 2
    linkage_matrix[count, 1] = len(clusters) - 1
    linkage_matrix[count, 2] = avg_dist
    linkage_matrix[count, 3] = len(orginal_cluster)
    
    count = count- 1


def terminate(k):
    for c in clusters:
        if len(c)>k:
            return 0
    return 1

def get_distance(s1, s2):
	matrix = read_fromfile('distance_matrix' + filename[:3])

	return matrix[s1][s2]

def divisive(k=1):
    while(not terminate(k)):
        split_cluster()





filename = 'hg16.fasta'
#filename = 'DNASequences.fasta'
with open(filename, "r") as datafile:
    records = list(read_fasta(datafile))
    num_records = len(records)




clusters=[]
linkage_matrix = numpy.zeros((num_records-1,4))
count = num_records-2

divisive()
numpy.save('dataFinal/'+filename[:3]+'_final', linkage_matrix)
for row in linkage_matrix:
    for elem in row:
        print(elem, end=', ')
    print()

plt.figure()
dn = hierarchy.dendrogram(linkage_matrix)
hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
dn1 = hierarchy.dendrogram(Z, ax=axes[0], above_threshold_color='y',
                            orientation='top')
dn2 = hierarchy.dendrogram(Z, ax=axes[1], above_threshold_color='#bcbddc', orientation='right')
hierarchy.set_link_color_palette(None)  # reset to default after use
plt.show()
