# Improvements:
#   * Switching to numpy arrays for better size/performance
#   * Removed Node() class, now each matrix just keeps track of the score
#   * New B matrix (best score) to track the best score at each step

import datetime
import numpy
import itertools

import sys

sys.path.append('../read_FASTA')
from read_FASTA import *

sys.path.append('../read_scoring_matrix')
from read_scoring_matrix import *

# Algorithm: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf
# Modified to allow zeroes for local alignment
def local_align(a, b, scoring_matrix):

    print(f'String sizes: {len(a)} x {len(b)}')
    GAP_START = -11
    GAP_EXTEND = -1
    
    # Initialize alignment matrices
    # Only set up the first row
    print('Creating matrices')
    
    # M matrix - match
    M = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    # X matrix - score if gap in A taken
    X = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    # Y matrix - score if gap in B taken
    Y = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    # B matrix - best score at each step
    B = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    
    # Fill in matrices
    last_i = 0
    t = datetime.datetime.now()
    for i, j in itertools.product(range(1, len(a)+1), range(1, len(b)+1)):
        if j == 1 and i % 100 == 0:
            last_i = i
            tn = datetime.datetime.now()
            print(f'{i} - {tn - t}')
            t = tn
        
        # Best match score is always equal to the best score at the previous step plus the current match score
        M[i, j] = B[i-1, j-1] + scoring_matrix[f'{a[i-1]}{b[j-1]}']
        
        # Best a-gap score is the maximum of either starting a new gap or extending a previous a-gap
        X[i, j] = max(B[i-1, j] + GAP_START, X[i-1, j] + GAP_EXTEND)
        
        # Best b-gap score is the maximum of either starting a new gap or extending a previous b-gap
        Y[i, j] = max(B[i, j-1] + GAP_START, Y[i, j-1] + GAP_EXTEND)
        
        # Determine best score at this step
        B[i, j] = max(M[i, j], X[i, j], Y[i, j], 0)
            
    # Determine the best score and indices of
    i, j = numpy.unravel_index(numpy.argmax(B), B.shape)
    best_score = B[i, j]
    
    # Backtrack from best score and build aligned strings
    local_a = ''
    local_b = ''
    while B[i, j]:
        if B[i, j] == M[i, j]:
            local_a = a[i-1] + local_a
            local_b = b[j-1] + local_b
            i -= 1
            j -= 1
        elif B[i, j] == X[i, j]:
            local_a = a[i-1] + local_a
            i -= 1
        elif B[i, j] == Y[i, j]:
            local_b = b[j-1] + local_b
            j -= 1
            
    return (best_score, local_a, local_b)
    
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=='__main__':
    scoring_matrix = read_scoring_matrix('BLOSUM62.txt')
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    start_time = datetime.datetime.now()
    print(f'{start_time}')
    
    best_score, local_a, local_b = local_align(a, b, scoring_matrix)

    end_time = datetime.datetime.now()
    print(f'{start_time}')
    print(f'{end_time}')
    print(f'{end_time - start_time}')
    
    result = f'{best_score}\n{local_a}\n{local_b}'
    print(result)
    
    write_result(result)