import sys
import numpy as np
import operator as op
import datetime

sys.path.append('../read_FASTA')
from read_FASTA import *
    
# Algorithm: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf
def overlap_align(a, b):
    print(f'{len(a)} - {len(b)}')
    GAP_PENALTY = -2
    
    M = np.zeros( (len(a)+1, len(b)+1), dtype=np.integer)
    # 1 - match
    # 2 - A-gap
    # 3 - B-gap
    D = np.zeros( (len(a)+1, len(b)+1), dtype=np.integer)
    for i in range(1, len(a)+1):
        M[i, 0] = 0
        D[i, 0] = 2
    for j in range(1, len(b)+1):
        M[0, j] = 0
        D[i, 0] = 3
    
    # Populate match score and direction arrays
    last_i = 0
    t = datetime.datetime.now()
    for i in range(1, len(a)+1):
        if i % 100 == 0:
            last_i = i
            tn = datetime.datetime.now()
            print(f'{i} - {tn - t}')
            t = tn
            
        for j in range(1, len(b)+1):
            a_ch = a[i-1]
            b_ch = b[j-1]
            
            match = (M[i-1, j-1] + (1 if a_ch == b_ch else -2), 1)
            a_gap = (M[i-1, j] + GAP_PENALTY,                   2)
            b_gap = (M[i, j-1] + GAP_PENALTY,                   3)
            
            possibilities = [match, a_gap, b_gap]
            
            M[i, j], D[i, j] = max(possibilities, key=op.itemgetter(0))
            
    #display_alignment(a, b, M)
            
    # Move the j-pointer to the position at which all of A has been consumed
    # and the best score has been found
    best_score = M[-1, 0]
    i = len(a)
    for k in range(len(b)+1):
        if M[i, k] > best_score:
            best_score = M[i, k]
            j = k
    
    # Backtrack until either string has been completely consumed
    local_a = ''
    local_b = ''
    while True:
        a_ch = a[i-1]
        b_ch = b[j-1]
        
        if D[i, j] == 1:
            local_a = a_ch + local_a
            local_b = b_ch + local_b
            i -= 1
            j -= 1
        elif D[i, j] == 2:
            local_a = '-' + local_a
            local_b = b_ch + local_b
            i -= 1
        elif D[i, j] == 3:
            local_a = a_ch + local_a
            local_b = '-' + local_b
            j -= 1
            
        if i == 0 or j == 0: break
            
    return (best_score, local_a, local_b)
    
def display_alignment(a, b, alignment):
    # Header (b)
    size = 3
    print(' '*2*size + ''.join(f'{i:{size}}' for i in range(len(b)+1)))
    print(' '*3*size + ''.join([f'{x:>{size}}' for x in b]))
    
    # First row
    print(' '*2*size + ''.join([f'{n:>{size}}' for n in alignment[0]]))
    
    # Other rows
    for i in range(len(a)):
        print(f'{i:{size}}' + f'{a[i]:>{size}}' + ''.join([f'{n:>{size}}' for n in alignment[i+1]]))
        
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=="__main__":
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    best_score, local_a, local_b = overlap_align(a, b)
    
    result = f'{best_score}\n{local_a}\n{local_b}'
    print(result)
    
    write_result(result)