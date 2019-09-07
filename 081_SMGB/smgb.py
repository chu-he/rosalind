import datetime
import numpy
import operator

import sys

sys.path.append('../read_FASTA')
from read_FASTA import *

# Modified to allow zeroes for local alignment
def semiglobal_align(a, b):
    print(a)
    print(b)
    
    # S matrix - score
    S = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    # D matrix - direction
    #   0 = match
    #   1 = A-gap
    #   2 = B-gap
    D = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    for i in range(1, len(a)+1):
        D[i, 0] = 1
    for j in range(1, len(b)+1):
        D[0, j] = 2
    
    # Fill in matrices
    last_i = 0
    t = datetime.datetime.now()
    for i in range(1, len(a)+1):
        if i % 100 == 0:
            last_i = i
            tn = datetime.datetime.now()
            print(f'{i} - {tn - t}')
            t = tn
            
        for j in range(1, len(b)+1):
            possibilities = []
            
            # Character match (or not)
            possibilities.append( (S[i-1, j-1] + (1 if a[i-1] == b[j-1] else -1), 0) )
            
            # A-gap
            possibilities.append( (S[i-1, j] - (0 if j == len(b) else 1), 1) )
            
            # B-gap
            possibilities.append( (S[i, j-1] - (0 if i == len(a) else 1), 2) )
            
            # Determine best score
            S[i, j], D[i, j] = max(possibilities, key=operator.itemgetter(0))
    
    # Backtrack from final score and build aligned strings
    i = len(a)
    j = len(b)
    local_a = ''
    local_b = ''
    while i or j:
        if D[i, j] == 0:
            local_a = a[i-1] + local_a
            local_b = b[j-1] + local_b
            i -= 1
            j -= 1
        elif D[i, j] == 1:
            local_a = a[i-1] + local_a
            local_b = '-' + local_b
            i -= 1
        elif D[i, j] == 2:
            local_b = b[j-1] + local_b
            local_a = '-' + local_a
            j -= 1
            
    return (S[-1, -1], local_a, local_b)
    
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=='__main__':
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    best_score, local_a, local_b = semiglobal_align(a, b)
    
    result = f'{best_score}\n{local_a}\n{local_b}'
    print(result)
    
    write_result(result)