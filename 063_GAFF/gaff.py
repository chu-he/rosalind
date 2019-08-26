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

    def __init__(self, a_index, b_index, a_char, b_char):
        self.score = 0
        self.parent = None
        self.is_a_gap = False
        self.is_b_gap = False
        self.align_type = ''
        self.a_index = a_index-1
        self.b_index = b_index-1
        self.a_char = a_char
        self.b_char = b_char

def print_alignment_matrix(alignment, a, b):
    width = 3
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
    alignment = [[Node(i, j, a[i-1], b[j-1]) for j in range(len(b)+1)] for i in range(len(a)+1)]

    # Initialize
    alignment[0][0].score = 0
    for a_index in range(1,len(a)+1):
        node = alignment[a_index][0]
        node.parent = alignment[a_index-1][0]
        node.score = node.parent.score + (Node.GAP_EXTEND if node.parent.is_b_gap else Node.GAP_OPEN)
        node.is_b_gap = True
        node.align_type = 'GAP_B'
        node.a_index = a_index
        node.b_index = -1
    for b_index in range(1,len(b)+1):
        node = alignment[0][b_index]
        node.parent = alignment[0][b_index-1]
        node.score = node.parent.score + (Node.GAP_EXTEND if node.parent.is_a_gap else Node.GAP_OPEN)
        node.is_a_gap = True
        node.align_type = 'GAP_A'
        node.a_index = -1
        node.b_index = b_index

    # Fill in rest of the table
    for a_index in range(1,len(a)+1):
        for b_index in range(1, len(b)+1):
            a_ch = a[a_index-1]
            b_ch = b[b_index-1]
            current_node = alignment[a_index][b_index]
            
            # Build the 3 possibilities - score, parent, is_a_gap, is_b_gap, align_type

            # Character match
            match_parent = alignment[a_index-1][b_index-1]
            match_score  = match_parent.score + BLOSUM62[a_ch][b_ch]
            match_pair = (match_score, match_parent, False, False, 'MATCH')

            # Gap on B string
            gap_b_parent = alignment[a_index-1][b_index]
            gap_b_score = gap_b_parent.score + (Node.GAP_EXTEND if gap_b_parent.is_b_gap else Node.GAP_OPEN)
            gap_b = (gap_b_score, gap_b_parent, False, True, 'GAP_B')
            
            # Gap on A string
            gap_a_parent = alignment[a_index][b_index-1]
            gap_a_score = gap_a_parent.score + (Node.GAP_EXTEND if gap_a_parent.is_a_gap else Node.GAP_OPEN)
            gap_a = (gap_a_score, gap_a_parent, True, False, 'GAP_A')
            
            result = max([match_pair, gap_a, gap_b], key=operator.itemgetter(0))
            current_node.score, current_node.parent, current_node.is_a_gap, current_node.is_b_gap, current_node.align_type = result

    print_alignment_matrix(alignment, a, b)
    
    # Construct the aligned strings - start at the end and follow the parent back
    current_node = alignment[-1][-1]
    aligned_a = ''
    aligned_b = ''
    while current_node != alignment[0][0]:
        if current_node.align_type == 'MATCH':
            aligned_a = current_node.a_char + aligned_a
            aligned_b = current_node.b_char + aligned_b
        elif current_node.align_type == 'GAP_A':
            aligned_a = '-' + aligned_a
            aligned_b = current_node.b_char + aligned_b
        elif current_node.align_type == 'GAP_B':
            aligned_a = current_node.a_char + aligned_a
            aligned_b = '-' + aligned_b
        else:
            print(f'{current_node.a_index} {current_node.b_index}')
            
        current_node = current_node.parent

    return (alignment[-1][-1].score, aligned_a, aligned_b)

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