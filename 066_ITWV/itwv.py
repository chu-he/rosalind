def can_interweave_helper(s, a, b):
    #print(f'  can_interweave_helper {s} : {a} x {b}')
    # Interweave successful!
    if a == '' and b == '': return True
    
    first_chars = []
    if a: first_chars.append(a[0])
    if b: first_chars.append(b[0])
    
    if s[0] in first_chars:
        if a and b and a[0] == b[0]:
            # If both first chars are the same, we must consider both cases
            return can_interweave_helper(s[1:], a[1:], b) or can_interweave_helper(s[1:], a, b[1:])
        else:
            # Only one first char matches
            if a and s[0] == a[0]:
                a = a[1:]
            else:
                b = b[1:]
            return can_interweave_helper(s[1:], a, b)
    else:
        # First char of s did not match first char of A or B
        # This interweaving didn't work
        return False

def can_interweave(s, a, b):
    #print(f'can_interweave {s} : {a} x {b}')
    # Get all substrings of s that are the same length as a+b
    combined_length = len(a)+len(b)
    subs = []
    for i in range(0, len(s)-combined_length+1):
        subs.append(s[i:i+combined_length])
        
    # Only consider substrings for which the first char matches
    valid_first_chars = (a[0], b[0])
    valid_subs = [s for s in subs if s[0] in valid_first_chars]
    
    # Check if each substring can be interweaved
    for valid_sub in valid_subs:
        if can_interweave_helper(valid_sub, a, b):
            return True
    return False

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        data = fp.read().split('\n')
        
    s = data[0]
    patterns = data[1:]
    
    matrix = [[0 for _ in patterns] for _ in patterns]
    #print(matrix)
    
    for a_index, a in enumerate(patterns):
        for b_index, b in enumerate(patterns):
            if can_interweave(s, a, b):
                matrix[a_index][b_index] = 1
        
    result = ''
    for row in matrix:
        result += ' '.join([str(x) for x in row]) + '\n'
        
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)