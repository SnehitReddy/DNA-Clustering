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
    clusters.append(list(range(num_records)))

def split_cluster():
    max_c = None
    max_sum = -1
    for c in clusters:
        if(len(c)<2):
            continue
        sum=0
        for i in range(len(c)):
            for j in range(len(c)):
                d = get_distance(c[i],c[j])
                sum= sum + d
        if sum > max_sum:
            max_c, max_sum = clusters.index(c), sum

    avg = max_sum / (len(c)*len(c))

    max_dissim = 0
    splinter = None
    for e in clusters[max_c]:
        dissim = 0
        for e_1 in clusters[max_c]:
            dissim = dissim + get_distance(e,e_1)
        if(dissim >= max_dissim):
            max_dissim = dissim
            splinter = e


    l = len(clusters[max_c])
    clusters[max_c].remove(splinter)

    sub_cluster_1=[]
    sub_cluster_2=[splinter]

    for ele in clusters[max_c]:
        original_dist = numpy.mean(list(get_distance(ele,ele_1) for ele_1 in clusters[max_c]))
        splinter_dist = numpy.mean(list(get_distance(ele,ele_1) for ele_1 in sub_cluster_2))

        if(splinter_dist < original_dist):
            sub_cluster_2.append(ele)
        else:
            sub_cluster_1.append(ele)

    clusters[max_c].clear()
    clusters.append(sub_cluster_1)
    clusters.append(sub_cluster_2)

    global count

    linkage_matrix[count, 0] = len(clusters) - 2
    linkage_matrix[count, 1] = len(clusters) - 1
    linkage_matrix[count, 2] = avg
    linkage_matrix[count, 3] = l

    count = count- 1


def terminate(k):
    for c in clusters:
        if len(c)>k:
            return 1
    return 0

def get_distance(s1, s2):
	return matrix[s1][s2]

def divisive(k=1):
    while(terminate(k)):
        split_cluster()





filename = 'hg16.fasta'
#filename = 'DNASequences.fasta'
with open(filename, "r") as datafile:
    records = list(read_fasta(datafile))
    num_records = len(records)




clusters=[]
linkage_matrix = numpy.zeros((num_records-1,4))
count = num_records-2
matrix = read_fromfile('distance_matrix' + filename[:3])

init_clusters()
'''for row in matrix:
    for elem in row:
        print(elem, end=', ')
    print()'''
divisive()
numpy.save('dataFinal/'+filename[:3]+'_final', linkage_matrix)


plt.figure()
dn = hierarchy.dendrogram(linkage_matrix)
hierarchy.set_link_color_palette(['m', 'c', 'y', 'k'])
fig, axes = plt.subplots(1, 2, figsize=(8, 3))
dn1 = hierarchy.dendrogram(linkage_matrix, ax=axes[0], above_threshold_color='y',
                            orientation='top')
dn2 = hierarchy.dendrogram(linkage_matrix, ax=axes[1], above_threshold_color='#bcbddc', orientation='right')
hierarchy.set_link_color_palette(None)  # reset to default after use
plt.show()
