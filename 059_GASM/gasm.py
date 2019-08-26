from operator import itemgetter

complement = { 'A': 'T',
               'T': 'A',
               'C': 'G',
               'G': 'C' }

def reverse_complement(s):
    global complement
    return ''.join([complement[ch] for ch in s[::-1]])

# Return a tuple with:
#  0: alignment size
#  1: alignment result
def align(left, right):
    #print(f'Aligning {left} with {right}')
    for i in range(min(len(left), len(right)), 0, -1):
        left_sub  = left[len(left)-i:]
        right_sub = right[:i]
        #print(f'{left_sub} <--> {right_sub}')
        if left_sub == right_sub:
            return (i, left + right[i:])
    # No alignment found
    return (0, '')
        
# Return a tuple with:
#  0: alignment size
#  1: alignment result
#  2: aligned item a
#  3: aligned item b
def try_alignment(a, b):
    #print(f'try_alignment {a} {b}')
    results = []
    
    # Get reverse complement of b --> c
    c = reverse_complement(b)
    
    # Check for perfect contains
    if a in b:
        print('<< PERFECT CONTAINS >>')
        return (len(a), b, a, b)
    if b in a:
        print('<< PERFECT CONTAINS >>')
        return (len(b), a, a, b)
    if a in c:
        print('<< PERFECT CONTAINS >>')
        return (len(a), b, a, b)
    if c in a:
        print('<< PERFECT CONTAINS >>')
        return (len(c), a, a, b)
    
    # Try to align every combination 
    results.append(align(a, b))
    results.append(align(b, a))
    results.append(align(a, c))
    results.append(align(c, a))
    
    # Find the maximal alignment
    best_alignment = max(results, key=itemgetter(0))
    #(f'Best alignment = {best_alignment}')
    
    return (best_alignment[0], best_alignment[1], a, b)
    
def get_alignment_set(lines):
    results = []
    for i in range(len(lines)):
        for j in range(i+1,len(lines)):
            a = lines[i]
            b = lines[j]
            # Try to align the two strings, get the best alignment score and result
            alignment = try_alignment(a, b)
            results.append(alignment)
            
            # We are VERY confident these two strings are aligned if 80% of the string matches
            if alignment[0] >= (max(len(a), len(b)) * 0.8):
                return [alignment]
                
    # If nothing is so confident, then result all possible alignments and scores
    return results

def consolidate(lines):
    
    # Consolidate the entire dataset into a single line
    while len(lines) > 1:
        print(f'List size = {len(lines)}')
        alignment_set = get_alignment_set(lines)
                    
        # For the best alignment score, remove the two components and replace with the result
        best_alignment = max(alignment_set, key=itemgetter(0))
        print(f'Best alignment out of set is {best_alignment}')
        _, result, x, y = best_alignment
        lines.remove(x)
        lines.remove(y)
        lines.append(result)
        
    return lines[0]
    
# If the string is looping, return the string with the loop removed
def find_loop(s):
    for i in range(len(s)-1,0,-1):
        if s[:i] == s[len(s)-i:]:
            return s[i:]
    return s

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        lines = fp.read().split('\n')
        
    consolidated = consolidate(lines)
    
    result = find_loop(consolidated)
    
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)