import operator

def read_fasta(data):
    sequences = {}
    seq_name = ''
    seq = ''
    for line in data.split('\n'):
        if line[0] == '>':
            if seq != '':
                sequences[seq_name] = seq
                seq = ''
            seq_name = line[1:]
        else:
            seq += line
    sequences[seq_name] = seq

    return sequences

def read_blosum(data):
    BLOSUM62 = {}
    from_aa_list = []
    for line in data.split('\n'):
        if from_aa_list == []:
            from_aa_list = line.split()
        else:
            line = line.split()
            to_aa = line[0]
            for i in range(1,len(line)):
                score = int(line[i])

                from_aa = from_aa_list[i-1]

                if from_aa not in BLOSUM62: BLOSUM62[from_aa] = {}
                BLOSUM62[from_aa][to_aa] = score

                if to_aa not in BLOSUM62: BLOSUM62[to_aa] = {}
                BLOSUM62[to_aa][from_aa] = score
    return BLOSUM62
    
def get_blosum_matrix():
    global BLOSUM62
    with open('BLOSUM62.txt', 'r') as fp2:
        blosum_data = fp2.read()

    BLOSUM62 = read_blosum(blosum_data)

def print_blosum(BLOSUM62):
    amino_acids = sorted(BLOSUM62.keys())
    # Print header
    width = 4
    width_text = width*' '
    print(width_text + ''.join([f'{amino_acid:>{width}}' for amino_acid in amino_acids]))

    # Print each row
    for from_aa in amino_acids:
        print(f'{from_aa:>{width}}' + ''.join([f'{BLOSUM62[from_aa][to_aa]:>{width}}' for to_aa in amino_acids]))
    print()


class Node():
    GAP_OPEN   = -11
    GAP_EXTEND = -1

    def __init__(self, a_char, b_char, table):
        self.score = 0
        self.parent = None
        if table == 'M':
            self.a_char = a_char
            self.b_char = b_char
        elif table == 'X':
            self.a_char = '-'
            self.b_char = b_char
        elif table == 'Y':
            self.a_char = a_char
            self.b_char = '-'

def print_alignment_matrix(alignment, a, b):
    width = 4
    width_text = width*' '
    # Header
    print(width_text*2 + ''.join([f'{a_ch:>{width}}' for a_ch in a]))
    # First Row
    print(width_text + ''.join([f'{alignment[a_index][0].score:{width}}' for a_index,a_ch in enumerate(a+' ')]))
    # Other Rows
    for b_index, b_ch in enumerate(b):
        print(f'{b_ch:>{width}}' + ''.join([f'{alignment[a_index][b_index+1].score:>{width}}' for a_index,a_ch in enumerate(a+' ')]))

def align(a, b):
    get_blosum_matrix()
    global BLOSUM62

    # Create a 2D array 1-bigger in each dimension than the two strings
    M = [[Node(a[i-1], b[j-1], 'M') for j in range(len(b)+1)] for i in range(len(a)+1)]
    X = [[Node(a[i-1], b[j-1], 'X') for j in range(len(b)+1)] for i in range(len(a)+1)]
    Y = [[Node(a[i-1], b[j-1], 'Y') for j in range(len(b)+1)] for i in range(len(a)+1)]

    # Initialize
    M[0][0].score = X[0][0].score = Y[0][0].score = 0
    for a_index in range(1,len(a)+1):
        for arr in [M, X, Y]:
            node = arr[a_index][0]
            node.parent = arr[a_index-1][0]
            node.score = Node.GAP_OPEN if a_index == 1 else (Node.GAP_OPEN + Node.GAP_EXTEND*(a_index-1))
    for b_index in range(1,len(b)+1):
        for arr in [M, X, Y]:
            node = arr[0][b_index]
            node.parent = arr[0][b_index-1]
            node.score = Node.GAP_OPEN if b_index == 1 else (Node.GAP_OPEN + Node.GAP_EXTEND*(b_index-1))
            
    # Algorithm starts here
    # https://www.cs.cmu.edu/~ckingsf/bioinfo-lectures/gaps.pdf
    for a_index in range(1, len(a)+1):
        for b_index in range(1, len(b)+1):
            # Calculate M node
            a_char = a[a_index-1]
            b_char = b[b_index-1]
            M_prev = max([M[a_index-1][b_index-1], X[a_index-1][b_index-1], Y[a_index-1][b_index-1]], key=operator.attrgetter('score'))
            M[a_index][b_index].score = M_prev.score + BLOSUM62[a_char][b_char]
            M[a_index][b_index].parent = M_prev
            
            # Calculate X node
            X_score, X_prev = max([ (Node.GAP_OPEN + M[a_index][b_index-1].score,   M[a_index][b_index-1]),
                                    (Node.GAP_EXTEND + X[a_index][b_index-1].score, X[a_index][b_index-1]),
                                    (Node.GAP_OPEN + Y[a_index][b_index-1].score,   Y[a_index][b_index-1]) ], key=operator.itemgetter(0))
            X[a_index][b_index].score = X_score
            X[a_index][b_index].parent = X_prev
            
            # Calculate Y node
            Y_score, Y_prev = max([ (Node.GAP_OPEN + M[a_index-1][b_index].score, M[a_index-1][b_index]),
                                    (Node.GAP_OPEN + X[a_index-1][b_index].score, X[a_index-1][b_index]),
                                    (Node.GAP_EXTEND + Y[a_index-1][b_index].score, Y[a_index-1][b_index]) ], key=operator.itemgetter(0))
            Y[a_index][b_index].score = Y_score
            Y[a_index][b_index].parent = Y_prev
            
    print('--- M ---')
    print_alignment_matrix(M, a, b)
    print('--- X ---')
    print_alignment_matrix(X, a, b)
    print('--- Y ---')
    print_alignment_matrix(Y, a, b)
    
    # Get the best alignment
    node = max([M[-1][-1], X[-1][-1], Y[-1][-1]], key=operator.attrgetter('score'))
    best_score = node.score
    
    # Get aligned strings
    aligned_a = ''
    aligned_b = ''
    while node != M[0][0] and node != X[0][0] and node != Y[0][0]:
        aligned_a = node.a_char + aligned_a
        aligned_b = node.b_char + aligned_b
        node = node.parent
            
    return (best_score, aligned_a, aligned_b)

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        fasta_data = fp.read()

    fasta = read_fasta(fasta_data)
    a, b = fasta.values()
    print(a)
    print(b)

    alignment_score, aligned_a, aligned_b = align(a, b)

    result = f'{alignment_score}\n{aligned_a}\n{aligned_b}'
    print(result)

    with open('result.txt', 'w') as fp2:
        fp2.write(result)