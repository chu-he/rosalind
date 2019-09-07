#include <iostream>
#include <assert.h>
#include "ScoringMatrix.h"
#include "FASTA.h"
#include <time.h>
#include <algorithm>
#include <chrono>

using namespace std;

int ind(int i, int j, int width) {
	return i * width + j;
}

void localAlign(const string a, const string b, Hashmap scoringMatrix) {
	int GAP_START = -11;
	int GAP_EXTEND = -1;

	int sa = a.length() + 1;
	int sb = b.length() + 1;

	// Initialize arrays
	cout << "Initializing arrays" << endl;
	int* X = new int[100000000];
	int* Y = new int[100000000];
	int* B = new int[100000000];

	for (int j = 0; j < sb; ++j) {
		int index = ind(0, j, sb);
		X[index] = 0;
		Y[index] = 0;
		B[index] = 0;
	}

	// Fill in matrices
	int bestScore = 0;
	int c = 0, d = 0;
	int last_i = 0;
	auto t = chrono::high_resolution_clock::now();
	for (int i = 1; i < sa; ++i) {
		if (i % 100 == 0) {
			last_i = i;
			auto tn = chrono::high_resolution_clock::now();
			auto dur = tn - t;
			auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(dur).count();
			cout << i << " " << ms << endl;
			t = tn;
		}

		int index = ind(i, 0, sb);
		X[index] = 0;
		Y[index] = 0;
		B[index] = 0;
			
		for (int j = 1; j < sb; ++j) {
			string pair = string() + a[i - 1] + b[j - 1];

			int index_i_j   = ind(i    , j    , sb);
			int index_i_jm  = ind(i    , j - 1, sb);
			int index_im_jm = ind(i - 1, j - 1, sb);
			int index_im_j  = ind(i - 1, j    , sb);

			B[index_i_j] = B[index_im_jm] + scoringMatrix[pair];

			X[index_i_j] = max(B[index_im_j] + GAP_START, X[index_im_j] + GAP_EXTEND);

			Y[index_i_j] = max(B[index_i_jm] + GAP_START, Y[index_i_jm] + GAP_EXTEND);

			B[index_i_j] = max({ B[index_i_j], X[index_i_j], Y[index_i_j], 0 });

			if (B[index_i_j] > bestScore) {
				bestScore = B[index_i_j];
				c = i;
				d = j;
			}
		}
	}

	// Backtrack from best score and build aligned strings
	string local_a = "", local_b = "";
	while (B[ind(c, d, sb)] != 0) {
		if (B[ind(c, d, sb)] == X[ind(c, d, sb)]) {
			local_a = string() + a[c - 1] + local_a;
			c -= 1;
		}
		else if (B[ind(c, d, sb)] == Y[ind(c, d, sb)]) {
			local_b = string() + b[d - 1] + local_b;
			d -= 1;
		}
		else {
			local_a = string() + a[c - 1] + local_a;
			local_b = string() + b[d - 1] + local_b;
			c -= 1;
			d -= 1;
		}
	}

	cout << bestScore << endl;
	cout << local_a << endl;
	cout << local_b << endl;

	delete[] X;
	delete[] Y;
	delete[] B;
}

int main()
{
	cout << "Reading scoring matrix" << endl;
	Hashmap blosum62 = ScoringMatrix::read("BLOSUM62.txt");
	assert(blosum62["AA"] == 4);
	assert(blosum62["WC"] == -2);
	assert(blosum62["CW"] == -2);
	assert(blosum62["WW"] == 11);

	cout << "Reading dataset" << endl;
	vector<string> strings = FASTA::read("dataset.txt");
	cout << strings[0] << endl << strings[1] << endl;

	string a = strings[0];
	string b = strings[1];
	localAlign(a, b, blosum62);
}