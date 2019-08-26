def find_overlap(a, b):
    overlap = ''
    for i in range(1, min(len(a), len(b))):
        if a[-i:] == b[:i]:
            overlap = b[:i]
    confidence = float(len(overlap)) / float(len(b))
    return (overlap, confidence)

def add_kmers(strings, kmers):
    # Find all kmers that can be appended
    new_list = []
    used_kmers = []
    
    for list_item in strings:
        for kmer in kmers:
            overlap, confidence = find_overlap(list_item, kmer)
            if confidence >= 0.5:
                combined = list_item + kmer[len(overlap):]
                new_list.append(combined)
                used_kmers.append(kmer)
                
    new_list = list(dict.fromkeys(new_list))
    for x in used_kmers: kmers.remove(x)
    
    return (new_list, kmers)

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        kmers = fp.read().split('\n')
        
    first = kmers[0]
    kmers = kmers[1:]
    print('\n'.join(sorted(kmers)))
    
    strings = [first]
    
    while kmers:
        strings, kmers = add_kmers(strings, kmers)
        print('\n')
        print(strings)
        print(kmers)
        
    exit(0)
    results = []
    for s in strings:
        overlap, confidence = find_overlap(s, first)
        if confidence >= 0.5:
            # Remove overlap first
            s = s[:-len(overlap)]
            results.append(s)
            
    print('\n'.join(sorted(results, key=len)))