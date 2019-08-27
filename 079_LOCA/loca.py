import operator
import sys
sys.path.append('../read_FASTA')
from read_FASTA import *

def read_scoring_matrix(filename):
    matrix = {}
    with open(filename) as fp:
        data = fp.read().split('\n')
        
    header = data[0].split()
    
    for line in data[1:]:
        line_split = line.split()
        x = line_split[0]
        line_split = line_split[1:]
        for i in range(len(line_split)):
            y = header[i]
            v = int(line_split[i])
            matrix[f'{x}{y}'] = v
            
    return matrix
    
class Node():
    def __init__(self, score=0, parent=None, action=''):
        self.score = score
        self.parent = parent
        self.action = action
    
# Algorithm: https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/local.pdf
def local_align(a, b, scoring_matrix):
    GAP_PENALTY = -5
    
    # Initialize alignment matrix
    alignment = [[Node() for j in range(len(b)+1)] for i in range(len(a)+1)]
    
    best_score = 0
    end_node = None
    
    # Fill in matrix
    for i in range(1,len(a)+1):
        for j in range(1,len(b)+1):
            x = a[i-1]
            y = b[j-1]
            
            # Build the list of possibilities
            # Each possibility is a tuple consisting of:
            #  * Score
            #  * Previous Node
            #  * Action (string)
            possibilities = []
            
            # Gap in a
            gap_a = alignment[i][j-1]
            possibilities.append( (gap_a.score + GAP_PENALTY, gap_a, 'GAP_A') )
            
            # Gap in b
            gap_b = alignment[i-1][j]
            possibilities.append( (gap_b.score + GAP_PENALTY, gap_b, 'GAP_B') )
            
            # Match
            match = alignment[i-1][j-1]
            possibilities.append( (match.score + scoring_matrix[f'{x}{y}'], match, 'MATCH') )
            
            # Restart
            possibilities.append( (0, None, 'START') )
            
            # Pick the best score
            best = max(possibilities, key=operator.itemgetter(0))
            
            n = alignment[i][j]
            n.score, n.parent, n.action = best
            
            if n.score > best_score:    
                best_score = n.score
                end_node = n
            
    display_alignment(a, b, alignment)
    
    print(f'Best score = {best_score}')
    
def display_alignment(a, b, alignment):
    # Header (b)
    size = 3
    print(' '*2*size + ''.join([f'{x:>{size}}' for x in b]))
    
    # First row
    print(' '*size + ''.join([f'{n.score:>{size}}' for n in alignment[0]]))
    
    # Other rows
    for i in range(len(a)):
        print(f'{a[i]:>{size}}' + ''.join([f'{n.score:>{size}}' for n in alignment[i+1]]))

if __name__=="__main__":
    scoring_matrix = read_scoring_matrix('pam250.txt')
    strings = read_fasta('dataset.txt')
    a, b = strings.values()
    
    local_align(a, b, scoring_matrix)