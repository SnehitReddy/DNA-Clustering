// A Naive recursive C++ program to find minimum number 
// operations to convert str1 to str2 
#include<bits/stdc++.h> 
using namespace std; 
  
// Utility function to find minimum of three numbers 
int min(int x, int y, int z) 
{ 
   return min(min(x, y), z); 
} 
  
int editDist(string str1 , string str2 , int m ,int n) 
{ 
    // If first string is empty, the only option is to 
    // insert all characters of second string into first 
    if (m == 0) return n; 
  
    // If second string is empty, the only option is to 
    // remove all characters of first string 
    if (n == 0) return m; 
  
    // If last characters of two strings are same, nothing 
    // much to do. Ignore last characters and get count for 
    // remaining strings. 
    if (str1[m-1] == str2[n-1]) 
        return editDist(str1, str2, m-1, n-1); 
  
    // If last characters are not same, consider all three 
    // operations on last character of first string, recursively 
    // compute minimum cost for all three operations and take 
    // minimum of three values. 
    return 1 + min ( editDist(str1,  str2, m, n-1),    // Insert 
                     editDist(str1,  str2, m-1, n),   // Remove 
                     editDist(str1,  str2, m-1, n-1) // Replace 
                   ); 
} 
  
// Driver program 
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
			dist_matrix[i][j] = editDist(seqlist[i], seqlist[j], seqlist[i].length(), seqlist[j].length());
			dist_matrix[j][i] = dist_matrix[i][j];
		}
	}
	std::cout<<"Finished Processing!"<<std::endl;
	
	std::cout<<"Writing outputfile!"<<std::endl;
	
	std::ofstream outfile ("someotherfun.txt", std::ofstream::out);
	 for(int p=0;p<n;p++){
		for(int j=0;j<n;j++){
			outfile<<dist_matrix[p][j]<<", ";
		}
		outfile<<std::endl;
	}
	outfile.close();
	 std::cout<<"Finished writing file!"<<std::endl;

} 