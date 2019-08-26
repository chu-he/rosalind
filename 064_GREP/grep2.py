def find_overlap(a, b):
    overlap = ''
    for i in range(1, min(len(a), len(b))):
        if a[-i:] == b[:i]:
            overlap = b[:i]
    confidence = float(len(overlap)) / float(len(b))
    return (overlap, confidence)

def add_kmer(list, item):
    new_items = []
    for list_item in list:
        overlap, confidence = find_overlap(list_item, item)
        if confidence >= 0.5:
            combined = list_item + item[len(overlap):]
            new_items.append(combined)
    list.extend(new_items)

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        kmers = fp.read().split('\n')
        
    first = kmers[0]
    kmers = kmers[1:]
    
    strings = [first]
    
    while kmers:
        add_kmer(strings, kmers.pop(0))
        
    print(strings)
    
    results = []
    for s in strings:
        overlap, confidence = find_overlap(s, first)
        if confidence >= 0.5:
            # Remove overlap first
            s = s[:-len(overlap)]
            results.append(s)
            
    print('\n'.join(sorted(results, key=len)))