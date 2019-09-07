#pragma once
#include <unordered_map>

using namespace std;

typedef unordered_map<string, int> Hashmap;

namespace ScoringMatrix {
	Hashmap read(string filename);
}