import numpy
import SeqIO from Bio

clusters=[]
linkage_matrix = numpy.zeroes(num_records-1,4)

with open(filename, "r") as datafile:
    records = list(SeqIO.parse(datafile, "fasta"))
    num_records = len(records)

def init_clusters():
    clusters=[list(range(num_records)))]

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
    for e in clusters[max_c]
        if(get_distance(e,max_i)>get_distance(e,max_j))
            sub_cluster_1.append(e);
        else
            sub_cluster_2.append(e);

    orginal_cluster = clusters.pop(mac_c);
    clusters.append(sub_cluster_1)
    clusters.append(sub_cluster_2)

    linkage_matrix[num_records - len(clusters), 0] = sub_cluster_1
    linkage_matrix[num_records - len(clusters), 1] = sub_cluster_2
    linkage_matrix[num_records - len(clusters), 2] = avg_dist
    linkage_matrix[num_records - len(clusters), 3] = len(orginal_cluster)


def terminate():
    for c in clusters:
        if len(c)>1:
            return 0
    return 1

def get_distance(s1, s2):
    str1=records[s1]
    str2=records[s2]
	MATCH, MISMATCH, GAP=(0, 1, 2)
	score_mat=numpy.zeros([len(str1)+1, len(str2)+1])
	score_mat[0,1:]=numpy.array([j*GAP for j in range(1,len(str2)+1)])
	score_mat[1:,0]=numpy.array([i*GAP for i in range(1, len(str1)+1)])
	for i in range(1, len(str1)+1):
		for j in range(1, len(str2)+1):
			is_match=(str1[len(str1)-i]==str2[len(str2)-j])
			score_mat[i,j]=min((score_mat[i, j-1]+GAP), (score_mat[i-1, j]+GAP), score_mat[i-1, j-1]+(MATCH*(is_match)+MISMATCH*(not is_match)))
	return score_mat[len(str1), len(str2)]

def divisive():
    while(not terminate()):
        split_cluster()
