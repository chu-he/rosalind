import datetime
import numpy
import operator

import sys

sys.path.append('../read_FASTA')
from read_FASTA import *

# Modified to allow zeroes for local alignment
def get_max_gaps(a, b):
    print(a)
    print(b)
    
    '''
    Assuming that we get the maximum number of matches (longest common substring),
    the maximum number of gaps that can be inserted is determined by assuming that
    all non-matching characters are paired with a gap
    '''
    
    # M matrix - num matches
    M = numpy.zeros( (len(a)+1, len(b)+1), dtype=numpy.integer )
    
    # Find length of longest common subsequence
    last_i = 0
    t = datetime.datetime.now()
    for i in range(1, len(a)+1):
        if i % 100 == 0:
            last_i = i
            tn = datetime.datetime.now()
            print(f'{i} - {tn - t}')
            t = tn
            
        for j in range(1, len(b)+1):
            if a[i-1] == b[j-1]:
                M[i, j] = M[i-1, j-1] + 1
            else:
                M[i, j] = max(M[i-1, j], M[i, j-1])
                
    # Calculate maximum number of gaps
    gaps = len(a) + len(b) - 2*M[-1, -1]
    
    return gaps
    
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=='__main__':
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    result = str(get_max_gaps(a, b))
    
    print(result)
    
    write_result(result)