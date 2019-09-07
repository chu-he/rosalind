# This implementation is the most straight-forward, but hits a MemoryError trying to initialize the matrices

import operator
import sys

sys.path.append('../read_FASTA')
from read_FASTA import *

sys.path.append('../read_scoring_matrix')
from read_scoring_matrix import *

class Node():
    def __init__(self, action=''):
        self.score = 0
        self.parent = None
        self.action = action
        self.a_value = ''
        self.b_value = ''

# Algorithm: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf
# Modified to allow zeroes for local alignment
def local_align(a, b, scoring_matrix):
    GAP_START = -10
    GAP_EXTEND = -1
    
    # Initialize alignment matrices
    M = [[Node(action='START') for j in range(len(b)+1)] for i in range(len(a)+1)]
    X = [[Node(action='START') for j in range(len(b)+1)] for i in range(len(a)+1)]
    Y = [[Node(action='START') for j in range(len(b)+1)] for i in range(len(a)+1)]
    
    best_score = 0
    end_node = None
    
    # Fill in matrices
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            x = a[i-1]
            y = b[j-1]
            
            # List of possibilities for M
            node_m = M[i][j]
            m_possibilities = []
            match_score = scoring_matrix[f'{x}{y}']
            
            match_from_m = M[i-1][j-1]
            match_from_x = X[i-1][j-1]
            match_from_y = Y[i-1][j-1]
            for m in [match_from_m, match_from_x, match_from_y]:
                m_possibilities.append( (m.score + match_score, m, x, y) )
            m_possibilities.append( (0, None, '', '') )
            
            best_m = max(m_possibilities, key=operator.itemgetter(0))
            node_m.score, node_m.parent, node_m.a_value, node_m.b_value = best_m
            
            if node_m.score > best_score:
                best_score = node_m.score
                end_node = node_m
            
            # List of possibilities for X
            node_x = X[i][j]
            x_possibilities = []
            
            x_gap_from_m = M[i][j-1]
            x_possibilities.append( (x_gap_from_m.score + GAP_START + GAP_EXTEND, x_gap_from_m, '', y) )
            
            x_gap_from_x = X[i][j-1]
            x_possibilities.append( (x_gap_from_x.score + GAP_EXTEND, x_gap_from_x, '', y) )
            
            x_gap_from_y = Y[i][j-1]
            x_possibilities.append( (x_gap_from_y.score + GAP_START + GAP_EXTEND, x_gap_from_y, '', y) )
            
            x_possibilities.append( (0, None, '', '') )
            
            best_x = max(x_possibilities, key=operator.itemgetter(0))
            node_x.score, node_x.parent, node_x.a_value, node_x.b_value = best_x
            
            if node_x.score > best_score:
                best_score = node_x.score
                end_node = node_x
            
            # List of possibilities for Y
            node_y = Y[i][j]
            y_possibilities = []
            
            y_gap_from_m = M[i-1][j]
            y_possibilities.append( (y_gap_from_m.score + GAP_START + GAP_EXTEND, y_gap_from_m, x, '') )
            
            y_gap_from_x = X[i-1][j]
            y_possibilities.append( (y_gap_from_x.score + GAP_START + GAP_EXTEND, y_gap_from_x, x, '') )
            
            y_gap_from_y = Y[i-1][j]
            y_possibilities.append( (y_gap_from_y.score + GAP_EXTEND, x_gap_from_y, x, '') )
            
            y_possibilities.append( (0, None, '', '') )
            
            best_y = max(y_possibilities, key=operator.itemgetter(0))
            node_y.score, node_y.parent, node_y.a_value, node_y.b_value = best_y
            
            if node_y.score > best_score:
                best_score = node_y.score
                end_node = node_y
            
    display_alignment(a, b, M)
    display_alignment(a, b, X)
    display_alignment(a, b, Y)
    
    # Backtrack from best score and build aligned strings
    local_a = ''
    local_b = ''
    while True:
        if end_node.score is not 0:
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
    print(' '*size + ''.join([f'{n.score:>{size}}' for n in alignment[0]]))
    
    # Other rows
    for i in range(len(a)):
        print(f'{a[i]:>{size}}' + ''.join([f'{n.score:>{size}}' for n in alignment[i+1]]))

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