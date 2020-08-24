import pickle

def save_tofile(obj, name):
    with open('obj/'+name+'.pkl', 'wb') as fp:
        pickle.dump(obj, fp, pickle.HIGHEST_PROTOCOL)

def read_fromfile(name):
    with open('obj/'+name+'.pkl', 'rb') as fp:
        return pickle.load(fp)

proximity_table = read_fromfile('proximity')
cluster_dic = read_fromfile('clusterdic')
