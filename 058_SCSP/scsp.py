lcs_map = {}

def longest_common_subsequence(a, b):
    global lcs_map
    
    # If either string is blank, the lcs is blank
    if a == '' or b == '':
        return ''
    
    # Return cached if available
    if (a,b) in lcs_map:
        return lcs_map[(a,b)]
        
    lcs = ''
    
    if a[0] == b[0]:
        # If first element is common, it's part of the lcs
        # Find the lcs of the remainder
        lcs = a[0] + longest_common_subsequence(a[1:],b[1:])
        
    else:
        # Otherwise, find the longer lcs of the two possibilities where the first char is removed from each string
        lcs = max( longest_common_subsequence(a    ,b[1:]), \
                   longest_common_subsequence(a[1:],b    ), \
                   key=len )
        
    # Cache the lcs for next time
    lcs_map[(a,b)] = lcs
    lcs_map[(b,a)] = lcs
    
    return lcs
    
    
def shortest_common_supersequence(a, b, lcs):
    super = ''
    
    while lcs:
        # Remove bits from beginning of both strings until the first char matches lcs
        while a[0] != lcs[0]:
            super += a[0]
            a = a[1:]
        
        while b[0] != lcs[0]:
            super += b[0]
            b = b[1:]
            
        # Add the first char of the lcs, and update both strings
        super += lcs[0]
        lcs = lcs[1:]
        a = a[1:]
        b = b[1:]
        
    # Add the remainder
    super += a
    super += b
    
    return super
        

if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        a, b = fp.read().split('\n')
    
    # Find longest common subsequence
    lcs = longest_common_subsequence(a, b)
    
    # Use subsequence to construct supersequence by interspersing the non-common bits
    super = shortest_common_supersequence(a, b, lcs)
    
    
    with open('result.txt', 'w') as fp2:
        fp2.write(super)