import numpy as np
import ctypes
import datetime
import pickle

libdiff = ctypes.cdll.LoadLibrary(r"C:\Users\Pratik\Downloads\DataMining-master\Ass2\libdiff.so")
filename = 'hg16.fasta'
#filename = 'DNASequences.fasta'
num_clusters = 0
cached_dist = {}

def get_distance(seq1, seq2, seq1ID, seq2ID):
    tempset = frozenset([seq1ID, seq2ID])
    if tempset in cached_dist:
        return cached_dist[tempset]
    distance = libdiff.get_distance(seq1.encode('ASCII'), seq2.encode('ASCII'))
    cached_dist[tempset] = distance
    return distance

def save_tofile(obj, name):
    with open('data/'+name+'.pkl', 'wb') as fp:
        pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)

def calculate_distance_matrix():

    distance_matrix = [[get_distance(str(records[i][1]), str(records[j][1]),
    records[i][0], records[j][0])
    for j in range(num_clusters)] for i in range(num_clusters)]
    # proximity_table = []
    # for i in range(num_clusters):
    #     proximity_table.append([])
    #     for j in range(num_clusters):
    #         proximity_table[i].append(get_distance(records[i],records[j]))
    save_tofile(distance_matrix, 'distance_matrix'+filename[:3])

def print_clusters(cluster_dic):
    for i, list in cluster_dic.items():
        print('Cluster', i, 'has size', len(list))

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


print('Commencing Operations at', datetime.datetime.now().time())
with open(filename, "r") as datafile:
    #records is a list of (name, sequence) tuples
    records = list(read_fasta(datafile))
    num_clusters = len(records)
print('Input parsed at', datetime.datetime.now().time())
calculate_distance_matrix()
print('Procedure completed at', datetime.datetime.now().time())
