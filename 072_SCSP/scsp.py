if __name__=='__main__':
    fp = open('dataset.txt', 'r')
    a, b = fp.read().split('\n')
    fp.close()
    
    # Find longest common subsequence
    sub = find_longest_common_subsequence(a, b)
    # Build a map of the "pieces" between the longest common subsequence
    # Build the supersequence by interleaving the in-between pieces with the subsequence