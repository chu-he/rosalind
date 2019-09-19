import sys
import numpy as np
import operator as op
import datetime

sys.path.append('../read_FASTA')
from read_FASTA import *
    
def matrix_align(a, b):
    
    # Forward alignment
    F = np.zeros( (len(a)+1, len(b)+1), dtype=np.integer)
    
    # Populate forward match score array
    for i in range(0, len(a)+1):
        for j in range(0, len(b)+1):
            score = -99999999
            if i > 0:
                score = max( score, F[i-1, j] - 1 )
            if j > 0:
                score = max( score, F[i, j-1] - 1 )
            if i > 0 and j > 0:
                score = max( score, F[i-1, j-1] + ( 1 if a[i-1] == b[j-1] else -1 ) )
            if score == -99999999:
                score = 0
            F[i, j] = score
            
    #display_alignment(a, b, F)
            
    # Backwards alignment
    B = np.zeros( (len(a)+1, len(b)+1), dtype=np.integer)
    
    # Populate backward match score array
    for i in range(len(a), -1, -1):
        for j in range(len(b), -1, -1):
            score = -99999999
            if i+1 <= len(a):
                score = max( score, B[i+1, j] - 1 )
            if j+1 <= len(b):
                score = max( score, B[i, j+1] - 1 )
            if i+1 <= len(a) and j+1 <= len(b):
                score = max( score, B[i+1, j+1] + ( 1 if a[i] == b[j] else -1 ) )
            if score == -99999999:
                score = 0
            B[i, j] = score
        
    #display_alignment(a, b, B)
    
    M_sum = 0
    for i in range(1, len(a)+1):
        for j in range(1, len(b)+1):
            
            # Forward match score of prefix +
            # Backward match score of suffix +
            # Current char match score
            score = F[i-1, j-1] + B[i, j] + (1 if a[i-1] == b[j-1] else -1)
            M_sum += score
            
            '''
            a_prefix = a[:i-1]
            a_suffix = a[i:]
            a_ch = a[i-1]
            
            b_prefix = b[:j-1]
            b_suffix = b[j:]
            b_ch = b[j-1]
            
            prefix_size = max(len(a_prefix), len(b_prefix), 1)
            suffix_size = max(len(a_suffix), len(b_suffix), 1)
            
            print(f'{a_prefix:{prefix_size}} {a_ch} {a_suffix:{suffix_size}}')
            print(f'{b_prefix:{prefix_size}} {b_ch} {b_suffix:{suffix_size}}')
            #print(f'{i}, {j} --> {score} = {F[i-1, j-1]} + {B[i, j]} + {(1 if a[i-1] == b[j-1] else -1)}')
            '''
        #print()
    
    return F[-1, -1], M_sum
    
def display_alignment(a, b, alignment):
    # Header (b)
    size = 3
    print(' '*2*size + ''.join(f'{i:{size}}' for i in range(len(b)+1)))
    print(' '*3*size + ''.join([f'{x:>{size}}' for x in b]))
    
    # First row
    print(f'{0:{size}}' + ' '*size + ''.join([f'{n:>{size}}' for n in alignment[0]]))
    
    # Other rows
    for i in range(len(a)):
        print(f'{i+1:{size}}' + f'{a[i]:>{size}}' + ''.join([f'{n:>{size}}' for n in alignment[i+1]]))
        
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=="__main__":
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    max_score, matrix_sum = matrix_align(a, b)
    
    result = f'{max_score}\n{matrix_sum}'
    print(result)
    
    write_result(result)