#include "ScoringMatrix.h"
#include <fstream>
#include <sstream>
#include <iostream>

using namespace std;

Hashmap ScoringMatrix::read(string filename) {
	Hashmap scoringMatrix;

	ifstream fp(filename);
	if (fp.is_open()) {
		bool isHeader = true;
		vector<string> header;
		for (string line; getline(fp, line); ) {
			if (isHeader) {
				// Save column headers into a vector for later access
				istringstream iss(line);
				string column;
				while (iss >> column) {
					header.push_back(column);
				}
				isHeader = false;
			}
			else {
				string row;
				int value;
				int headerIndex = 0;
				istringstream iss(line);
				iss >> row;
				// Save each row/header --> value pairing into the map
				while (iss >> value) {
					string column = header[headerIndex++];
					scoringMatrix[row + column] = value;
				}
			}
		}
	}
	else {
		cout << "Unable to open file " + filename << endl;
		exit(0);
	}

	return scoringMatrix;
}