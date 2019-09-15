#include <iostream>
#include "FASTA.h"

using namespace std;

int ind(int i, int j, int width) {
	return i * width + j;
}

void overlapAlign(const string a, const string b) {
	int sa = a.length() + 1;
	int sb = b.length() + 1;

	int* S = new int[100000000];
	int* D = new int[100000000];

	for (int i = 0; i < sa; ++i) {
		int index = ind(i, 0, sb);
		S[index] = 0;
		D[index] = 2;
	}
	for (int j = 0; j < sb; ++j) {
		int index = ind(0, j, sb);
		S[index] = 0;
		D[index] = 3;
	}
	
	for (int i = 1; i < sa; ++i) {
		for (int j = 1; j < sb; ++j) {

			int match = S[ind(i - 1, j - 1, sb)] + (a[i - 1] == b[j - 1] ? 1 : -2);
			int best = match;
			int best_dir = 1;

			int aGap = S[ind(i - 1, j, sb)] - 2;
			if (aGap > best) {
				best = aGap;
				best_dir = 2;
			}

			int bGap = S[ind(i, j - 1, sb)] - 2;
			if (bGap > best) {
				best = bGap;
				best_dir = 3;
			}

			S[ind(i, j, sb)] = best;
			D[ind(i, j, sb)] = best_dir;
		}
	}

	int best_score = S[ind(sa - 1, 0, sb)];
	int i = sa - 1;
	int j = 0;
	for (int k = 0; k < sb; ++k) {
		if (S[ind(i, k, sb)] >= best_score) {
			best_score = S[ind(i, k, sb)];
			j = k;
		}
	}

	string local_a = "";
	string local_b = "";

	cout << best_score << endl;

	while (1) {
		int dir = D[ind(i, j, sb)];
		if (dir == 1) {
			local_a = string() + a[i - 1] + local_a;
			local_b = string() + b[j - 1] + local_b;
			i -= 1;
			j -= 1;
		}
		else if (dir == 2) {
			local_a = string() + a[i - 1] + local_a;
			local_b = "-" + local_b;
			i -= 1;
		}
		else if (dir == 3) {
			local_a = "-" + local_a;
			local_b = string() + b[j - 1] + local_b;
			j -= 1;
		}

		if (i == 0 || j == 0) {
			break;
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
	overlapAlign(a, b);
}