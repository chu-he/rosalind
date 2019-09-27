#include <iostream>
#include <fstream>
#include <vector>
#include <string>

using namespace std;

vector<string> readDataset(string filename) {
	vector<string> strings;
	ifstream fp(filename);
	if (fp.is_open()) {
		for (string line; getline(fp, line); ) {
			strings.push_back(line);
		}
	}
	return strings;
}

int ind(int i, int j, int width) {
	return i * width + j;
}

void motifs(string a, string b, int k) {
	int sa = a.length() + 1;
	int sb = b.length() + 1;

	// Arrays will consist of two rows only, holding the previous and current rows
	// This is sufficient because we don't need to backtrack through the array
	int* A = new int[100000];
	int* R = new int[100000];

	for (int j = 0; j < sb; ++j) {
		int index = ind(0, j, sb);
		A[index] = 0;
		R[index] = index;
	}

	int score, new_score, root, index;
	for (int i = 1; i < sa; ++i) {
		for (int j = 0; j < sb; ++j) {
			score = -99999999;

			index = ind(0, j, sb);
			new_score = A[index] - 1;
			if (new_score > score) {
				score = new_score;
				root = R[index];
			}

			if (j > 0) {
				index = ind(1, j - 1, sb);
				new_score = A[index] - 1;
				if (new_score > score) {
					score = new_score;
					root = R[index];
				}

				index = ind(0, j - 1, sb);
				new_score = A[index] + (a[i - 1] == b[j - 1] ? 0 : -1);
				if (new_score > score) {
					score = new_score;
					root = R[index];
				}
			}

			index = ind(1, j, sb);
			A[index] = score;
			R[index] = root;
		}

		// Copy current row to previous row
		for (int j = 0; j < sb; ++j) {
			int prev = ind(0, j, sb);
			int cur = ind(1, j, sb);
			A[prev] = A[cur];
			R[prev] = R[cur];
		}
	}

	for (int j = 0; j < sb; ++j) {
		index = ind(0, j, sb);
		if (-A[index] <= k) {
			int root = R[index];
			int length = j - root;
			cout << (root + 1) << ' ' << length << endl;
		}
	}

}

int main()
{
	cout << "Reading dataset" << endl;
	vector<string> strings = readDataset("dataset.txt");

	int k = stoi(strings[0]);
	string a = strings[1];
	string b = strings[2];

	cout << k << endl << a << endl << b << endl;

	motifs(a, b, k);
}