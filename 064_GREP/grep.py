def find_overlap(a, b):
    overlap = ''
    for i in range(1, min(len(a), len(b))):
        if a[-i:] == b[:i]:
            overlap = b[:i]
    confidence = float(len(overlap)) / float(len(b))
    return (overlap, confidence)

def add_kmers(list, kmers):
    # Find all kmers that can be appended
    new_list = []
    used_kmers = []
    
    for list_item in list:
        for kmer in kmers:
            overlap, confidence = find_overlap(list_item, kmer)
            if confidence >= 0.5:
                combined = list_item + kmer[len(overlap):]
                new_list.append(combined)
                used_kmers.append(kmer)
                
    new_list = list(dict.fromkeys(new_list))
    kmers = [x for x in kmers if x not in used_kmers]
    
    return (new_list, kmers)
    
def find_complete_strings(s, kmers):
    # Used up all the kmers - the string is complete
    if kmers == []: return [s]
    
    # Find all kmers that can be appended to this string
    matches = []
    for kmer in kmers:
        match_length = len(kmer)-1
        if s[-match_length:] == kmer[:match_length]:
            matches.append(kmer)
            
    if matches:
        # Find the string associated with each append
        strings = []
        for kmer in matches:
            child_kmers = kmers.copy()
            child_kmers.remove(kmer)
            strings.extend(find_complete_strings(s+kmer[-1], child_kmers))
        
        return strings
    else:
        # No matching kmers found - we hit a dead end
        # This is not a valid path
        return []
    

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        kmers = fp.read().split('\n')
        
    first = kmers[0]
    kmers = kmers[1:]
    
    complete_strings = find_complete_strings(first, kmers)
    
    # Filter out duplicates
    complete_strings = list(dict.fromkeys(complete_strings))
    
    # Only consider those strings that loop back to the first kmer
    # Remove the loop as well
    results = []
    for s in complete_strings:
        match_length = len(first)-1
        if s[-match_length:] == first[:match_length]:
            results.append(s[:-match_length])
    
    result = '\n'.join(sorted(results))
    print(result)
    
    with open('result.txt', 'w') as fp:
        fp.write(result)