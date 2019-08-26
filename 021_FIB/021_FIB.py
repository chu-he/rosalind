import sys

n = int(sys.argv[1])
k = int(sys.argv[2])

F = {}
F[1] = 1
F[2] = 1

for i in range(3, n+1):
    F[i] = F[i-1] + k*F[i-2]
    
print F[n]