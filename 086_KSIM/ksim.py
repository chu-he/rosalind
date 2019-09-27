import sys
import numpy as np
import operator as op
import datetime

sys.path.append('../read_FASTA')
from read_FASTA import *
    
def motifs(a, b, k):
    print(f'{len(a)} - {len(b)}')
    
    # Alignment (edit distance score)
    A = np.zeros( (len(a)+1, len(b)+1), dtype=np.integer)
    # Root (starting position in b string)
    R = np.zeros( (len(a)+1, len(b)+1), dtype=np.integer)
    
    # Initialize root values
    for j in range(0, len(b)+1):
        R[0, j] = j
    
    # Populate alignment array
    last_i = 0
    t = datetime.datetime.now()
    for i in range(1, len(a)+1):
    
        if i % 100 == 0:
            last_i = i
            tn = datetime.datetime.now()
            print(f'{i} - {tn - t}')
            t = tn
            
        for j in range(0, len(b)+1):
            score = -99999999
            if i == 0 and j == 0:
                score = 0
                root = 0
             
            if i > 0:
                new_score = A[i-1, j] - 1
                if new_score > score:
                    score = new_score
                    root  = R[i-1, j]
                    
            if j > 0:
                new_score = A[i, j-1] - 1
                if new_score > score:
                    score = new_score
                    root  = R[i, j-1]
                    
            if i > 0 and j > 0:
                new_score = A[i-1, j-1] + ( -1 if a[i-1] != b[j-1] else 0 )
                if new_score > score:
                    score = new_score
                    root  = R[i-1, j-1]
                    
            A[i, j] = score
            R[i, j] = root
            
    display_alignment(a, b, A)
    display_alignment(a, b, R)
    
    result = []
    for j in range(0, len(b)+1):
        # Check for all aligment scores that match our condition
        if -A[-1, j] <= k:
            root = R[-1, j]
            length = j - root
            
            # Rosalind accepts 1-indexed
            result.append( (root+1, length) )
            
    return result
    
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
    with open('dataset.txt', 'r') as fp:
        k, s, t = fp.read().split('\n')
        
    substrings = motifs(s, t, int(k))
    
    result = '\n'.join([f'{r} {l}' for r, l in substrings])
    print(result)
    
    write_result(result)