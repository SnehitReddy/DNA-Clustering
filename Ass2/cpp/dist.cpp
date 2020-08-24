#include <iostream>
#include <fstream>
#include <vector>
#include<stdlib.h>
#include<string.h>



int get_min ( int a, int b ) { return a < b ? a : b; }

int get_distance(const char* sequenceA, const char* sequenceB){
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

int main(int argc, char **argv) {
    if (argc < 2) {
        std::cerr << " Wrong format: " << argv[0] << " [infile] " << std::endl;
        return -1;
    }

    std::ifstream input(argv[1]);
    if (!input.good()) {
        std::cerr << "Error opening: " << argv[1] << " . You have failed." << std::endl;
        return -1;
    }
    std::string line, id, DNA_sequence;
	std::vector<std::string> seqlist;

      while (std::getline(input, line)) {

        // line may be empty so you *must* ignore blank lines
        // or you have a crash waiting to happen with line[0]
        if(line.empty())
            continue;

        if (line[0] == '>') {
            // output previous line before overwriting id
            // but ONLY if id actually contains something
            if(!id.empty())
               // std::cout << id << " : " << DNA_sequence << std::endl;
				seqlist.push_back(DNA_sequence);
            id = line.substr(1);
            DNA_sequence.clear();
        }
        else {
            DNA_sequence += line;
        }
    }

    // output final entry
    // but ONLY if id actually contains something
    if(!id.empty())
		seqlist.push_back(DNA_sequence);
	
	//for(auto it = seqlist.begin(); it != seqlist.end(); ++it) {
		//std::cout<<"LOL : "<< *it<<std::endl;
	//}
	std::cout<<"Finished reading file!"<<std::endl;
	int n = seqlist.size();
	
	//std::cout<<"Total sequences are : "<< seqlist.size()<< std::endl;
	//std::cout<<"Last seq is "<< seqlist[n-1]<< std::endl;
	//std::cout<<"First seq is : "<< seqlist[0]<< std::endl;
	
	int dist_matrix[n][n];
	for(int p=0;p<n;p++){
		for(int j=0;j<n;j++){
			dist_matrix[p][j] = -1;
		}
	}
	std::cout<<"Finished init of matrix!"<<std::endl;
	
	for(int i=0; i<n;i++) {
		for(int j=0; j<n; ++j) {
			dist_matrix[i][j] = get_distance((seqlist[i]).c_str(), (seqlist[j]).c_str());
			dist_matrix[j][i] = dist_matrix[i][j];
		}
	}
	std::cout<<"Finished Processing!"<<std::endl;
	
	std::cout<<"Writing outputfile!"<<std::endl;
	
	std::ofstream outfile ("out.txt", std::ofstream::out);
	 for(int p=0;p<n;p++){
		for(int j=0;j<n;j++){
			outfile<<dist_matrix[p][j]<<", ";
		}
		outfile<<std::endl;
	}
	outfile.close();
	 std::cout<<"Finished writing file!"<<std::endl;

}