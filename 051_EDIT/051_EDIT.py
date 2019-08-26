 import string
from bisect import bisect_left

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

# Build ENUMERATED dicts so we don't have to run string.find so many times
ENUMERATED_T = {}
for x in enumerate(t):
    i, ch = x
    if ch not in ENUMERATED_T:
        ENUMERATED_T[ch] = [i]
    else:
        ENUMERATED_T[ch].append(i)
        
ENUMERATED_S = {}
for x in enumerate(s):
    i, ch = x
    if ch not in ENUMERATED_S:
        ENUMERATED_S[ch] = [i]
    else:
        ENUMERATED_S[ch].append(i)
    
def findNextIndex(i, ch, enumerated_str):
    # Binary search
    if ch in enumerated_str:
        next_i = bisect_left(enumerated_str[ch], i)
        if next_i != len(enumerated_str[ch]):
            return enumerated_str[ch][next_i]
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
            next_i = findNextIndex(i+1, ch, ENUMERATED_T)
            if next_i != -1:
                appendSubsequence(next_i, subseq+ch)
        
    # Find the first instance of ch in t, possible start of subsequence
    if ch in t:
        appendSubsequence(ENUMERATED_T[ch][0], ch)

# Sort by decreasing subsequence length
lcsq = sorted(T_SUBSEQUENCES.keys(), key=lambda x: len(x), reverse=True)[0]

print "LCSQ = {0}".format(lcsq)

# Find all the "gaps" and calculate edit distances for each
s_i = -1
t_i = -1
editDistance = 0
for ch in lcsq:
    p_s_i = s_i
    p_t_i = t_i
    
    s_i = findNextIndex(s_i+1, ch, ENUMERATED_S)
    t_i = findNextIndex(t_i+1, ch, ENUMERATED_T)
    
    gap_s = s[p_s_i+1:s_i]
    gap_t = t[p_t_i+1:t_i]
    
    l_s = len(gap_s)
    l_t = len(gap_t)
    ed = l_s if l_s > l_t else l_t
    
    print "{0} --> {1}: {2}".format(gap_s, gap_t, ed)
    
    editDistance += ed

result = editDistance
print result    

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()