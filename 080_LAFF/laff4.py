# This implementation saves even more on memory by:
#   1) Only keeping the current row and the previous row
#   2) Manually running the garbage collect to remove dead Nodes
#
# Memory issue is now solved! But still runs very slowly for the huge dataset...

import psutil
import datetime

import gc
import sys

sys.path.append('../read_FASTA')
from read_FASTA import *

sys.path.append('../read_scoring_matrix')
from read_scoring_matrix import *

class Node():
    def __init__(self, score=0, parent=None, a_value='', b_value=''):
        self.score = score
        self.parent = parent
        self.a_value = a_value
        self.b_value = b_value
        
def bytes2human(n):
    # http://code.activestate.com/recipes/578019
    # >>> bytes2human(10000)
    # '9.8K'
    # >>> bytes2human(100001221)
    # '95.4M'
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix = {}
    for i, s in enumerate(symbols):
        prefix[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if n >= prefix[s]:
            value = float(n) / prefix[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n

# Algorithm: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf
# Modified to allow zeroes for local alignment
def local_align(a, b, scoring_matrix):

    process = psutil.Process()

    print(f'String sizes: {len(a)} x {len(b)}')
    GAP_START = -10
    GAP_EXTEND = -1
    MINIMUM_FOR_GAP = -(GAP_START + GAP_EXTEND)
    MINIMUM_FOR_GAP_EXTEND = -GAP_EXTEND
    
    # Initialize alignment matrices
    # Only set up the first row
    print('Creating matrices')
    M = [[None for j in range(len(b)+1)]]
    X = [[None for j in range(len(b)+1)]]
    Y = [[None for j in range(len(b)+1)]]
    
    best_score = 0
    end_node = None
    
    # Fill in matrices
    for a_index in range(1,len(a)+1):
        print(f'Row {a_index} - {bytes2human(process.memory_info().rss)}')
    
        # Initialize first column of this row 
        for arr in [M, X, Y]:
            arr.append([None])
            
        x = a[a_index-1]
            
        for j in range(1,len(b)+1):
            y = b[j-1]
            
            # List of possibilities for M
            best_m = (0, None, '', '')
            match_score = scoring_matrix[f'{x}{y}']
            
            match_from_m = M[0][j-1]
            match_from_x = X[0][j-1]
            match_from_y = Y[0][j-1]
            for m in [match_from_m, match_from_x, match_from_y]:
                prev_score = m.score if m else 0
                new_score = prev_score + match_score
                if new_score > best_m[0]:
                    best_m = (new_score, m, x, y)
            
            if best_m[0] is 0:
                node_m = None
            else:
                node_m = Node(score=best_m[0], parent=best_m[1], a_value=best_m[2], b_value=best_m[3])
            M[1].append(node_m)
            
            if node_m and node_m.score > best_score:
                best_score = node_m.score
                end_node = node_m
            
            # List of possibilities for X
            best_x = (0, None, '', '')
            
            x_gap_from_m = M[1][j-1]
            if x_gap_from_m and x_gap_from_m.score > MINIMUM_FOR_GAP:
                new_score_x_m = x_gap_from_m.score + GAP_START + GAP_EXTEND
                if new_score_x_m > best_x[0]:
                    best_x = (new_score_x_m, x_gap_from_m, '', y)
            
            x_gap_from_x = X[1][j-1]
            if x_gap_from_x and x_gap_from_x.score > MINIMUM_FOR_GAP_EXTEND:
                new_score_x_x = x_gap_from_x.score + GAP_EXTEND
                if new_score_x_x > best_x[0]:
                    best_x = (new_score_x_x, x_gap_from_x, '', y)
            
            x_gap_from_y = Y[1][j-1]
            if x_gap_from_y and x_gap_from_y.score > MINIMUM_FOR_GAP:
                new_score_x_y = x_gap_from_y.score + GAP_START + GAP_EXTEND
                if new_score_x_y > best_x[0]:
                    best_x = (new_score_x_y, x_gap_from_y, '', y)
                    
            if best_x[0] is 0:
                node_x = None
            else:
                node_x = Node(score=best_x[0], parent=best_x[1], a_value=best_x[2], b_value=best_x[3])
            X[1].append(node_x)
            
            if node_x and node_x.score > best_score:
                best_score = node_x.score
                end_node = node_x
                
            # List of possibilities for Y
            best_y = (0, None, '', '')
            
            y_gap_from_m = M[0][j]
            if y_gap_from_m and y_gap_from_m.score > MINIMUM_FOR_GAP:
                new_score_y_m = y_gap_from_m.score + GAP_START + GAP_EXTEND
                if new_score_y_m > best_y[0]:
                    best_y = (new_score_y_m, y_gap_from_m, x, '')
            
            y_gap_from_x = X[0][j]
            if y_gap_from_x and y_gap_from_x.score > MINIMUM_FOR_GAP:
                new_score_y_x = y_gap_from_x.score + GAP_START + GAP_EXTEND
                if new_score_y_x > best_y[0]:
                    best_y = (new_score_y_x, y_gap_from_x, x, '')
            
            y_gap_from_y = Y[0][j]
            if y_gap_from_y and y_gap_from_y.score > MINIMUM_FOR_GAP_EXTEND:
                new_score_y_y = y_gap_from_y.score + GAP_EXTEND
                if new_score_y_y > best_y[0]:
                    best_y = (new_score_y_y, y_gap_from_y, x, '')
            
            if best_y[0] is 0:
                node_y = None
            else:
                node_y = Node(score=best_y[0], parent=best_y[1], a_value=best_y[2], b_value=best_y[3])
            Y[1].append(node_y)
            
            if node_y and node_y.score > best_score:
                best_score = node_y.score
                end_node = node_y
                
        # Finished processing this row
        # Remove the previous row, the current row becomes the previous
        M = M[1:]
        X = X[1:]
        Y = Y[1:]
        
        # Run the garbage collect to remove Nodes with no references
        gc.collect()
    
    # Backtrack from best score and build aligned strings
    local_a = ''
    local_b = ''
    while True:
        if end_node:
            local_a = end_node.a_value + local_a
            local_b = end_node.b_value + local_b
            end_node = end_node.parent
        else:
            break
            
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
    
    result = f'{best_score}\n{local_a}\n{local_b}'
    print(result)
    
    write_result(result)