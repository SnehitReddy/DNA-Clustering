import numpy as np
import ctypes
import datetime
from Bio import SeqIO
import pickle

libdiff = ctypes.cdll.LoadLibrary(r"G:\Study\2-2\DataMining\Ass2\libdiff.so")
filename = 'hg16.fasta'
k = 3
num_clusters = 0
start_clusters = 0
deleted_clusters = set()

def get_distance(seq1, seq2):
    return libdiff.get_distance(seq1.encode('ASCII'), seq2.encode('ASCII'))

def save_tofile(obj, name):
    with open('obj/'+name+'.pkl', 'wb') as fp:
        pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)

def read_fromfile(name):
    with open('obj/'+name+'.pkl', 'rb') as fp:
        return pickle.load(fp)

def init_clusters():
    #Return proximity_table and cluster_dic
    return None, None

def print_clusters(cluster_dic):
    for i, list in cluster_dic.items():
        print('Cluster', i, 'has size', len(list))


def avg_dist(proximity_table, i, j, cluster_dic):
    ilen = len(cluster_dic[i])
    jlen = len(cluster_dic[j])
    proximity_table[i] = [(ix * ilen + jx * jlen)/(ilen+jlen) for ix, jx in zip(proximity_table[i],proximity_table[j])]
    for x in range(start_clusters):
        proximity_table[x][i] = proximity_table[i][x]

#For separating two specefic clusters
def separate_clusters(cluster_dic, i, j):
    global num_clusters
    #do something
    num_clusters = num_clusters + 1

def update_distance(proximity_table, i, j, cluster_dic):
    # slink(proximity_table, i)
    # clink(proximity_table, i)
    avg_dist(proximity_table, i, j, cluster_dic)

def divide_clusters(proximity_table, cluster_dic):
    pass
    #do something

with open(filename, "r") as datafile:
    records = list(SeqIO.parse(datafile, "fasta"))
    num_clusters = len(records)
    start_clusters = num_clusters


print('Operations commencing at', datetime.datetime.now().time())
proximity_table, cluster_dic = init_clusters()
print('Created Initial Proximity table! Created initial Clusters!', datetime.datetime.now().time())
while num_clusters > k:
    merge_clusters(proximity_table, cluster_dic)
print('Operations finished at',datetime.datetime.now().time())
print('Clusters left are', num_clusters)

print_clusters(cluster_dic)
