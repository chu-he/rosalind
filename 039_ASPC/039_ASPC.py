import sys
from math import factorial

def C(n, k):
    return factorial(n) / ( factorial(k) * factorial(n-k) )

(n, m) = [int(x) for x in sys.argv[1:]]

sum = 0
for k in range(m, n+1):
    sum += C(n, k)

result = str(sum % 1000000)
print result

outfile = open('039_ASPC.result', 'w')
outfile.write(result)
outfile.close()