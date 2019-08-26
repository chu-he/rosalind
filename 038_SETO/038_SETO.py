file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

n = int(data[0])
A = [int(x) for x in data[1][1:-1].split(', ')]
B = [int(x) for x in data[2][1:-1].split(', ')]

union     = {}
intersect = {}
A_minus_B = {}
B_minus_A = {}
A_c       = {}
B_c       = {}

for k in range(1, n+1):
    union[k]     = 0
    intersect[k] = 0
    A_minus_B[k] = 0
    B_minus_A[k] = 0
    A_c[k]       = 1
    B_c[k]       = 1
    
for a in A:
    union[a]      = 1
    intersect[a] += 1
    A_minus_B[a]  = 1
    B_minus_A[a] -= 1
    A_c[a]        = 0
    
for b in B:
    union[b]      = 1
    intersect[b] += 1
    A_minus_B[b] -= 1
    B_minus_A[b] += 1
    B_c[b]        = 0
    
results = [[] for _ in range(6)]
for k in range(1, n+1):
    if union[k] == 1:     results[0].append(str(k))
    if intersect[k] == 2: results[1].append(str(k))
    if A_minus_B[k] == 1: results[2].append(str(k))
    if B_minus_A[k] == 1: results[3].append(str(k))
    if A_c[k] == 1:       results[4].append(str(k))
    if B_c[k] == 1:       results[5].append(str(k))
    
result = ''
for i in range(len(results)):
    result += '{' + ', '.join(results[i]) + '}\n'

print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()