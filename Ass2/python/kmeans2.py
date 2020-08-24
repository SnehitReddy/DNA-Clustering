import numpy as npy
#from subprocess import check_output
import ctypes
import datetime
from Bio import SeqIO

reward = 0
mismatch = 1
gap = 2
libdiff = ctypes.cdll.LoadLibrary(r"G:\Study\2-2\DataMining\Ass2\libdiff.so")
process_name = "..\\a.exe"
comparison_counter = 0

def match_check(seq1, seq2, i, j):
    if(seq1[i] == seq2[j]):
        return reward
    else:
        return mismatch



def get_distance(seq1, seq2):
    #print('getting dist for two seq baby')
    # return int(check_output(process_name + " " + seq1 + " " + seq2, shell=True).decode())
    global comparison_counter
    comparison_counter = comparison_counter + 1
    returnValue = libdiff.get_distance(seq1.encode('ASCII'), seq2.encode('ASCII'))
    #print('Got distance', returnValue)
    #print('Have done',comparison_counter, 'comparisons uptill now')
    return returnValue

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

def init_centroid_list(filename, k):
    cluster_list = []
    i = 1
    with open(filename) as datafile:
        for name, seq in read_fasta(datafile):
            if i > k:
                break
            i = i+1
            cluster_list.append(seq)

    return cluster_list

def calculate_centroids(cluster_dic):
    #Do something
    npy.zeros([])
    return cluster_dic.keys()

def print_ans(dictionary):
    print('Operations finished at',datetime.datetime.now().time())
    i = 0
    print('*******************************************************************')
    print('Did',comparison_counter,'comparisons overall!')
    for i, (key, value) in enumerate(dictionary.items()):
        print('*******************************')
        print('For cluster', i)
        print('It has size',len(value))
        for item in value:
            print(item[0])


def k_means(filename, centroid_list, prev_cluster_dic, k=5):
    flag = 0
    # global comparison_counter
    # comparison_counter = 0
    cluster_dic = {centroid:[] for centroid in centroid_list}
    #First clusters
    with open(filename, "r") as datafile:
        # records = list(SeqIO.parse(datafile, "fasta"))
        # dist_dic = {get_distance(centroid, str(record.seq)):centroid for centroid in centroid_list for record in records}
        for record in SeqIO.parse(datafile, "fasta"):
            name, seq = record.id, str(record.seq)
            dist_dic = {get_distance(centroid, seq):centroid for centroid in centroid_list}
            #print(name, seq)
            min_dist = min(*(dist_dic.keys()))
            min_centroid = dist_dic[min_dist]
            cluster_dic[min_centroid].append((name, seq))
            if min_centroid in prev_cluster_dic.keys():
                if (name, seq) not in prev_cluster_dic[min_centroid]:
                    flag = 1
            else :
                flag = 1
    if flag:
        new_centroid_list = calculate_centroids(cluster_dic)
        k_means(filename, new_centroid_list, cluster_dic, k)
    else:
        #Yay
        print_ans(cluster_dic)


num_cluster = 3
filename = 'hg16.fasta'
centroid_list = init_centroid_list(filename, num_cluster)
print('Operations commencing at',datetime.datetime.now().time())
k_means(filename, centroid_list, {}, k= num_cluster)
