import numpy as np
import ctypes
import datetime
from Bio import SeqIO
import pickle

libdiff = ctypes.cdll.LoadLibrary(r"G:\Study\2-2\DataMining\Ass2\libdiff.so")
filename = 'hg16.fasta'
k = 1
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

    try:
        proximity_table = read_fromfile('proximity')
        cluster_dic = read_fromfile('clusterdic')
        return proximity_table, cluster_dic

    except IOError:
        print('Files not found! Creating new initial proximity table and cluster dictionary')

    cluster_dic = {i:[i] for i in range(num_clusters)}
    proximity_table = [[get_distance(str(records[i].seq), str(records[j].seq))
    for j in range(num_clusters)] for i in range(num_clusters)]
    # proximity_table = []
    # for i in range(num_clusters):
    #     proximity_table.append([])
    #     for j in range(num_clusters):
    #         proximity_table[i].append(get_distance(records[i],records[j]))
    save_tofile(proximity_table, 'proximity')
    save_tofile(cluster_dic, 'clusterdic')
    return proximity_table, cluster_dic

def print_clusters(cluster_dic):
    for i, list in cluster_dic.items():
        print('Cluster', i, 'has size', len(list))


def avg_dist(proximity_table, i, j, cluster_dic):
    ilen = len(cluster_dic[i])
    jlen = len(cluster_dic[j])
    proximity_table[i] = [(ix * ilen + jx * jlen)/(ilen+jlen) for ix, jx in zip(proximity_table[i],proximity_table[j])]
    for x in range(start_clusters):
        proximity_table[x][i] = proximity_table[i][x]
    # [proximity_table[x].pop(j) for x in range(num_clusters)]
    # The line above ain't gonna work because that would change the indices after j!! don do that

def join_clusters(cluster_dic, i, j):
    global num_clusters
    # print('clusters before adding',cluster_dic[i], cluster_dic[j])
    cluster_dic[i].extend(cluster_dic[j])##copy second list if this dont work
    # print('clusters after adding',cluster_dic[i], cluster_dic[j])
    del cluster_dic[j]
    # print('clusters after deleting',cluster_dic[i])
    deleted_clusters.add(j)
    # print('deleted_clusters are', deleted_clusters)
    num_clusters = num_clusters - 1

def update_distance(proximity_table, i, j, cluster_dic):
    # slink(proximity_table, i)
    # clink(proximity_table, i)
    avg_dist(proximity_table, i, j, cluster_dic)

def merge_clusters(proximity_table, cluster_dic):
    #i and j are the closest two clusters
    i, j = min((n, i, j) for i, L in enumerate(proximity_table) for j, n in enumerate(L)
    if(i not in deleted_clusters and j not in deleted_clusters and i != j))[1:]
    # print('Got i and j', i, j)
    #update distances in Proximity table
    update_distance(proximity_table, i, j, cluster_dic)
    #join clusters and delete old cluster
    join_clusters(cluster_dic, i, j)

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
