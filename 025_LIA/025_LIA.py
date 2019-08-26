import sys
from math import factorial

def c(k, n):
    return factorial(n)/(factorial(k)*factorial(n-k))

(k, N) = [int(x) for x in sys.argv[1:3]]

# children per couple
cpc = 2.0

# Generation 1
   # AA   Aa   aa
A = [0.0, 1.0, 0.0]
# B is the same as A

# AA from AAxAA (1.0  chance)
#         AAxAa (0.5  chance) X
#         AaxAa (0.25 chance) X

# Aa from AAxAa (0.5  chance) X
#         AAxaa (1.0  chance)
#         AaxAA (0.5  chance)
#         AaxAa (0.5  )       X
#         Aaxaa (0.25 )
#         aaxAA (1.0  )
#         aaxAa (0.5  )       X

# aa from AaxAa (0.25 )       X
#         Aaxaa (0.5  )
#         aaxAa (0.5  )       X
#         aaxaa (1.0  )
for gen in range(1, k+1):
    T = [ 0.5 * A[0] + 0.25 * A[1],
          0.5 * A[0] + 0.5 * A[1] + 0.5 * A[0],
          0.25 * A[1] + 0.5 * A[0] ]
    A = T
    
    print gen
    print A
    print ''
    
AaBb = A[1]**2
numChildren = 2**(k)

prob = 0.0
for n in range(N, numChildren+1):
    # Ways to choose n organisms of genotype AaBb out of x children...
    # times probability of n AaBb organisms
    # times probability of (x-n) non AaBb organisms
    prob += c(n,numChildren)*(AaBb**n)*((1-AaBb)**(numChildren-n))
    print n, prob
    
print prob
print round(prob, 3)