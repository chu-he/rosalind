import sys

debugFile = open('debug.txt', 'w')

file = open('dataset.txt', 'r')
data = file.read()
file.close()

lines = data.split('\n')
seq = ''.join(lines[1:])
print seq

# Lookup array so we don't need to recalculate number of crossing for ones we have done already
NUM_MATCHINGS = { '': 1 }

# Matching base lookup
MATCHING_BASE = { 'A': 'U',
                  'U': 'A',
                  'C': 'G',
                  'G': 'C' }
                  
BASES = ['A', 'U', 'C', 'G']

# Find all positions of ch in seq
# If an after argument is provided, only returns positions after that point
def findAllPositions( ch, seq, after=None ):
    return [pos for pos, char in enumerate(seq) if char == ch and (after == None or pos > after)]
    
def countChars(s):
    d = dict((char_, s.count(char_)) for char_ in set(s))
    for b in BASES:
        if b not in d: d[b] = 0
    #print d
    return d

def findNumCrossings( seq ):
    # If it was previously calculated, just return it
    if seq in NUM_MATCHINGS:
        return NUM_MATCHINGS[seq]
        
    if len(seq) % 2 == 1:
        return 0
        
    crossings = 0
    
    charCount = countChars(seq)
    if charCount['A'] == charCount['U'] and \
       charCount['C'] == charCount['G']:
    
        first_pos = 0
        first_ch = seq[first_pos]
        second_ch = MATCHING_BASE[first_ch]
        second_positions = findAllPositions(second_ch, seq, first_pos)
        
        for second_pos in second_positions:
            # At this point the first and second bases are "paired"
            # The number of possibilities for this are equal to the number of
            # pairs of the bases INSIDE this pair, multiplied by the number of
            # pairs of the bases OUTSIDE this pair
            
            inside = seq[first_pos+1:second_pos]
            outside = seq[:first_pos] + seq[second_pos+1:]
            #debugFile.write(seq + "\n" + first_ch + (second_pos-1)*"-" + second_ch + "\nInside:  " + inside + "\nOutside: " + outside + "\n\n")
            
            crossings += findNumCrossings(inside) * findNumCrossings(outside)
        
    NUM_MATCHINGS[seq] = crossings
    return crossings
        
result = findNumCrossings(seq) % 1000000
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()

debugFile.close()