import numpy as np
import ctypes
import datetime
import pickle

filename = 'hg16.fasta'
#filename = 'DNASequences.fasta'

def read_fromfile(name):
    with open('data/'+name+'.pkl', 'rb') as fp:
        return pickle.load(fp)

matrix = read_fromfile('distance_matrix' + filename[:3])
for ithrow in matrix:
    for j in ithrow:
        print('{:.2e}'.format(j), end=", ")
    print()
