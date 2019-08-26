import string
from bisect import bisect_right

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

s = sequences[0]
t = sequences[1]
print s
print t

# A list of mappings (subseq --> i), where:
#   i is the index of the last character of subseq in t
#   subseq is the current subsequence
T_SUBSEQUENCES = {}

# A list of mappings ( STR(LEN(SUBSEQ)) + CH --> i), where:
#   i is the index of the last character of subseq
#   ch is the last character of subseq
EARLIEST = {}

# A list of mappings ( STR(i) + CH --> subseq ) that keeps track of the longest subsequence ending in CH that ends at t[i]
LONGEST_AT_INDEX = {}

# Build ENUMERATED dict so we don't have to run string.find so many times
ENUMERATED = {}
for x in enumerate(t):
    i, ch = x
    if ch not in ENUMERATED:
        ENUMERATED[ch] = [i]
    else:
        ENUMERATED[ch].append(i)
    
def findNextIndex(i, ch):
    # Binary search
    next_i = bisect_right(ENUMERATED[ch], i)
    if next_i != len(ENUMERATED[ch]):
        return ENUMERATED[ch][next_i]
    return -1

def appendSubsequence(i, subseq):
    global T_SUBSEQUENCES
    global EARLIEST
    
    append = False
    
    if subseq not in T_SUBSEQUENCES:
        lenCh = str(len(subseq)) + subseq[-1]
        
        # Check if we already have this same subsequence occurring earlier in t
        if lenCh not in EARLIEST:
            append = True
        else:
            prev_i = EARLIEST[lenCh]
            if i < prev_i:
                append = True
                
    if append:
        # Check if we already have a longer subsequence with the same tail ending at this index
        iCh = str(i) + subseq[-1]
        if iCh in LONGEST_AT_INDEX:
            other_subseq = LONGEST_AT_INDEX[iCh]
            if len(subseq) > len(other_subseq):
                LONGEST_AT_INDEX[iCh] = subseq
                del T_SUBSEQUENCES[other_subseq]
        else:
            LONGEST_AT_INDEX[iCh] = subseq
            
        EARLIEST[lenCh] = i
        T_SUBSEQUENCES[subseq] = i
        
for s_i in range(len(s)):
    print s_i
    #print T_SUBSEQUENCES
    #print ''
    ch = s[s_i]
    
    # For each subsequence of t, find the next instance of ch and append it onto the subseq
    keys = T_SUBSEQUENCES.keys()
    for subseq in keys:
        # Due to the del action, subseq may no longer be in T_SUBSEQUENCES
        if subseq in T_SUBSEQUENCES:
            i = T_SUBSEQUENCES[subseq]
            next_i = findNextIndex(i, ch)
            if next_i != -1:
                appendSubsequence(next_i, subseq+ch)
        
    # Find the first instance of ch in t, possible start of subsequence
    appendSubsequence(ENUMERATED[ch][0], ch)

# Sort by decreasing subsequence length
result = sorted(T_SUBSEQUENCES.keys(), key=lambda x: len(x), reverse=True)[0]

# Return the first one
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()