file = open('dataset.txt', 'r')
data = file.read()
file.close()

sequences = []
seq = ''
for line in data.split('\n'):
    if line[0] == '>':
        if seq != '':
            sequences.append(seq)
            seq = ''
    else:
        seq += line
sequences.append(seq)

MATCHING_BASE = { 'A': 'T',
                  'T': 'A',
                  'C': 'G',
                  'G': 'C' }
BASES = ['A', 'U', 'C', 'G']

def getReverseComplement(seq):
    global MATCHING_BASE
    return ''.join(MATCHING_BASE[b] for b in seq[::-1])
    
# Returns the hamming distance between two sequence
# Note: For performance reasons, returns immediately if Hamming distance hits 2, since we are only interested in distances of 1
def getHammingDistance(a, b):
    hd = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            hd += 1
            if hd >= 2:
                return 2
    return hd

# Set of sequences that are GOOD - these have been matched 2x (either as-is or reverse complement
GOOD = {}

# Set of sequences that are PENDING - these have not been matched yet
PENDING = {}

# Set of sequences that are ERROR, mapping to its corrected version
CORRECTIONS = {}

for seq in sequences:
    # If this sequence is GOOD, we can ignore it
    if seq in GOOD:
        continue
        
    rcSeq = getReverseComplement(seq)
    
    # If this sequence is PENDING, this means it has appeared twice. We can add it to GOOD
    # Note: This applies for both the sequence as-is AND its reverse complement
    if seq in PENDING or rcSeq in PENDING:
        PENDING.pop(seq, None)
        PENDING.pop(rcSeq, None)
        GOOD[seq] = None
        GOOD[rcSeq] = None
        continue
        
    # Not GOOD or PENDING - put this sequence into the PENDING set
    PENDING[seq] = None
    
# What is left in the PENDING should be the ERRORs - match these with the appropriate corrections from the GOOD set
for error in PENDING:
    for correction in GOOD:
        if getHammingDistance(error, correction) == 1:
            CORRECTIONS[error] = correction
            break

# Format the result
result = ''            
for error in CORRECTIONS:
    result += error + "->" + CORRECTIONS[error] + "\n"
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()