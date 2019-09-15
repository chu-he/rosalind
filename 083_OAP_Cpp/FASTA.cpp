#include "FASTA.h"
#include <fstream>

vector<string> FASTA::read(string filename) {
	vector<string> strings;
	ifstream fp(filename);
	if (fp.is_open()) {
		string current = "";
		for (string line; getline(fp, line); ) {
			if (line[0] == '>') {
				if (current != "") {
					strings.push_back(current);
					current = "";
				}
			}
			else {
				current += line;
			}
		}
		strings.push_back(current);
	}
	return strings;
}