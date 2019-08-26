import sys
from math import factorial

n = int(sys.argv[1])
k = int(sys.argv[2])

print factorial(n)/factorial(n-k) % 1000000