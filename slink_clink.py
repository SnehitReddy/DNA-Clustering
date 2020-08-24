def slink(proximity_table, i, j, cluster_dic):
    proximity_table[i] = [min(ix,jx) for ix, jx in zip(proximity_table[i],proximity_table[j])]
    for x in range(start_clusters):
        proximity_table[x][i] = proximity_table[i][x]

def clink(proximity_table, i, j, cluster_dic):
    proximity_table[i] = [max(ix,jx) for ix, jx in zip(proximity_table[i],proximity_table[j])]
    for x in range(start_clusters):
        proximity_table[x][i] = proximity_table[i][x]
