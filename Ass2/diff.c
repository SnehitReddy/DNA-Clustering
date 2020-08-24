//#include<Python.h>
#include"diff.h"
#include<stdio.h>
#include<stdlib.h>
#include<string.h>



int get_min ( int a, int b ) { return a < b ? a : b; }

int get_distance(char* sequenceA, char* sequenceB){
        if(strcmp(sequenceA, sequenceB) == 0){
            return 0;
        }
        // The penalties to apply
        int gap = 2, substitution = 1, match = 0;
        int seqA_len = strlen(sequenceA);
        int seqB_len = strlen(sequenceB);
        //printf("Got the lengths! %d x %d\n",seqA_len, seqB_len);

        int **opt = (int**)malloc(sizeof(int*)*(seqA_len+1));
        for (int i = 0; i <= seqA_len; i++)
            opt[i] = (int*)malloc(sizeof(int)*(seqB_len+1));
        //printf("Created Array of said lengths\n");
        //Fill the first element
        opt[0][0] = 0;
        // First of all, compute insertions and deletions at 1st row/column
        for (int i = 1; i <= seqA_len; i++){
            opt[i][0] = opt[i - 1][0] + gap;
        }

        //printf("Filled col of said arr\n");
        for (int j = 1; j <= seqB_len; j++){
            opt[0][j] = opt[0][j - 1] + gap;
        }

        for (int i = 1; i <= seqA_len; i++) {
            for (int j = 1; j <= seqB_len; j++) {
                int scoreDiag = opt[i - 1][j - 1] +
                        (sequenceA[i-1] == sequenceB[j-1] ?
                            match : // same symbol
                            substitution); // different symbol
                int scoreLeft = opt[i][j - 1] + gap; // insertion
                int scoreUp = opt[i - 1][j] + gap; // deletion
                // we take the minimum
                opt[i][j] = get_min(get_min(scoreDiag, scoreLeft), scoreUp);

            }
        }
        int dist = opt[seqA_len][seqB_len];
        //printf("Final distance = %d\n",dist);

        for (int i = 0; i <= seqA_len; i++)
            free(opt[i]);
        free(opt);
        return dist;
}


// int main(int argc, char** argv){
//     printf("%d",get_distance(argv[1], argv[2]));
//     return 0;
// }
