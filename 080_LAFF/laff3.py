# This implementation saves on memory by building the matrices on the fly
# It's still pretty slow and seems to get stuck around row 1391
# The hardest part of this problem is the huge size of the input strings

import operator
import sys

sys.path.append('../read_FASTA')
from read_FASTA import *

sys.path.append('../read_scoring_matrix')
from read_scoring_matrix import *

class Node():
    COUNT = 0
    def __init__(self, score=0, parent=None, a_value='', b_value=''):
        self.score = score
        self.parent = parent
        self.a_value = a_value
        self.b_value = b_value

# Algorithm: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf
# Modified to allow zeroes for local alignment
def local_align(a, b, scoring_matrix):
    print(f'String sizes: {len(a)} x {len(b)}')
    GAP_START = -10
    GAP_EXTEND = -1
    
    # Initialize alignment matrices
    # The strings being processed by this problem are much longer, so we cannot pre-create the Nodes due to memory issues
    # Only the first row is initialized
    print('Creating matrices')
    M = [[None for j in range(len(b)+1)]]
    X = [[None for j in range(len(b)+1)]]
    Y = [[None for j in range(len(b)+1)]]
    
    best_score = 0
    end_node = None
    
    # Fill in matrices
    for i in range(1,len(a)+1):
        print(f'Row {i}')
    
        # Initialize first column of this row 
        for arr in [M, X, Y]:
            arr.append([None])
            
        for j in range(1,len(b)+1):
            x = a[i-1]
            y = b[j-1]
            
            # List of possibilities for M
            m_possibilities = []
            match_score = scoring_matrix[f'{x}{y}']
            
            match_from_m = M[i-1][j-1]
            match_from_x = X[i-1][j-1]
            match_from_y = Y[i-1][j-1]
            for m in [match_from_m, match_from_x, match_from_y]:
                prev_score = m.score if m else 0
                new_score = prev_score + match_score
                if new_score > 0:
                    m_possibilities.append( (new_score, m, x, y) )
            m_possibilities.append( (0, None, '', '') )
            
            best_m = max(m_possibilities, key=operator.itemgetter(0))
            if best_m[0] is 0:
                node_m = None
            else:
                node_m = Node(score=best_m[0], parent=best_m[1], a_value=best_m[2], b_value=best_m[3])
            M[i].append(node_m)
            
            if node_m and node_m.score > best_score:
                best_score = node_m.score
                end_node = node_m
            
            # List of possibilities for X
            x_possibilities = []
            
            x_gap_from_m = M[i][j-1]
            new_score_x_m = (x_gap_from_m.score if x_gap_from_m else 0) + GAP_START + GAP_EXTEND
            if new_score_x_m > 0:
                x_possibilities.append( (new_score_x_m, x_gap_from_m, '', y) )
            
            x_gap_from_x = X[i][j-1]
            new_score_x_x = (x_gap_from_x.score if x_gap_from_x else 0) + GAP_EXTEND
            if new_score_x_x > 0:
                x_possibilities.append( (new_score_x_x, x_gap_from_x, '', y) )
            
            x_gap_from_y = Y[i][j-1]
            new_score_x_y = (x_gap_from_y.score if x_gap_from_y else 0) + GAP_START + GAP_EXTEND
            if new_score_x_y > 0:
                x_possibilities.append( (new_score_x_y, x_gap_from_y, '', y) )
            
            x_possibilities.append( (0, None, '', '') )
            
            best_x = max(x_possibilities, key=operator.itemgetter(0))
            if best_x[0] is 0:
                node_x = None
            else:
                node_x = Node(score=best_x[0], parent=best_x[1], a_value=best_x[2], b_value=best_x[3])
            X[i].append(node_x)
            
            if node_x and node_x.score > best_score:
                best_score = node_x.score
                end_node = node_x
                
            # List of possibilities for Y
            y_possibilities = []
            
            y_gap_from_m = M[i-1][j]
            new_score_y_m = (y_gap_from_m.score if y_gap_from_m else 0) + GAP_START + GAP_EXTEND
            if new_score_y_m > 0:
                y_possibilities.append( (new_score_y_m, y_gap_from_m, x, '') )
            
            y_gap_from_x = X[i-1][j]
            new_score_y_x = (y_gap_from_x.score if y_gap_from_x else 0) + GAP_START + GAP_EXTEND
            if new_score_y_x > 0:
                y_possibilities.append( (new_score_y_x, y_gap_from_x, x, '') )
            
            y_gap_from_y = Y[i-1][j]
            new_score_y_y = (y_gap_from_y.score if y_gap_from_y else 0) + GAP_EXTEND
            if new_score_y_y > 0:
                y_possibilities.append( (new_score_y_y, y_gap_from_y, x, '') )
            
            y_possibilities.append( (0, None, '', '') )
            
            best_y = max(y_possibilities, key=operator.itemgetter(0))
            if best_y[0] is 0:
                node_y = None
            else:
                node_y = Node(score=best_y[0], parent=best_y[1], a_value=best_y[2], b_value=best_y[3])
            Y[i].append(node_y)
            
            if node_y and node_y.score > best_score:
                best_score = node_y.score
                end_node = node_y
            
    display_alignment(a, b, M)
    display_alignment(a, b, X)
    display_alignment(a, b, Y)
    
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

def display_alignment(a, b, alignment):
    # Header (b)
    size = 3
    print(' '*2*size + ''.join([f'{x:>{size}}' for x in b]))
    
    # First row
    print(' '*size + ''.join([f'{n.score if n else 0:>{size}}' for n in alignment[0]]))
    
    # Other rows
    for i in range(len(a)):
        print(f'{a[i]:>{size}}' + ''.join([f'{n.score if n else 0:>{size}}' for n in alignment[i+1]]))

    print()
    
def write_result(result):
    with open('result.txt', 'w') as fp:
        fp.write(result)

if __name__=='__main__':
    scoring_matrix = read_scoring_matrix('BLOSUM62.txt')
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    best_score, local_a, local_b = local_align(a, b, scoring_matrix)

    result = f'{best_score}\n{local_a}\n{local_b}'
    print(result)
    
    write_result(result)