#include <iostream>
#include <assert.h>
#include "FASTA.h"
#include <time.h>
#include <algorithm>
#include <chrono>

using namespace std;

int ind(int i, int j, int width) {
	return i * width + j;
}

void semiglobalAlign(const string a, const string b) {
	int sa = a.length() + 1;
	int sb = b.length() + 1;

	// Initialize arrays
	cout << "Initializing arrays" << endl;
	// S matrix - score
	int* S = new int[100000000];
	// D matrix - direction
	//   0 = match
	//   1 = A - gap
	//   2 = B - gap
	int* D = new int[100000000];
	
	for (int i = 0; i < sa; ++i) {
		int index = ind(i, 0, sb);
		S[index] = 0;
		D[index] = 1;
	}
	for (int j = 0; j < sb; ++j) {
		int index = ind(0, j, sb);
		S[index] = 0;
		D[index] = 2;
	}

	// Fill in matrices
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

		for (int j = 1; j < sb; ++j) {

			// Character match (or not)
			int match = S[ind(i - 1, j - 1, sb)] + (a[i - 1] == b[j - 1] ? 1 : -1);
			int best = match;
			int best_dir = 0;

			// A-gap
			int aGap = S[ind(i - 1, j, sb)] - (j == (sb - 1) ? 0 : 1);
			if (aGap > best) {
				best = aGap;
				best_dir = 1;
			}

			// B-gap
			int bGap = S[ind(i, j - 1, sb)] - (i == (sa - 1) ? 0 : 1);
			if (bGap > best) {
				best = bGap;
				best_dir = 2;
			}

			S[ind(i, j, sb)] = best;
			D[ind(i, j, sb)] = best_dir;
		}
	}


	// Backtrack from final score and build aligned strings
	int c = sa - 1;
	int d = sb - 1;
	string local_a = "";
	string local_b = "";

	cout << S[ind(c, d, sb)] << endl;

	while (c > 0 or d > 0) {
		if (D[ind(c, d, sb)] == 0) {
			local_a = string() + a[c - 1] + local_a;
			local_b = string() + b[d - 1] + local_b;
			c -= 1;
			d -= 1;
		}
		else if (D[ind(c, d, sb)] == 1) {
			local_a = string() + a[c - 1] + local_a;
			local_b = "-" + local_b;
			c -= 1;
		}
		else if (D[ind(c, d, sb)] == 2) {
			local_b = string() + b[d - 1] + local_b;
			local_a = "-" + local_a;
			d -= 1;
		}
	}

	cout << local_a << endl;
	cout << local_b << endl;

	delete[] S;
	delete[] D;
}

int main()
{
	cout << "Reading dataset" << endl;
	vector<string> strings = FASTA::read("dataset.txt");
	cout << strings[0] << endl << strings[1] << endl;

	string a = strings[0];
	string b = strings[1];
	semiglobalAlign(a, b);
}