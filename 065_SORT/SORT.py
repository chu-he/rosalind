import operator

# Reference: https://www.cs.helsinki.fi/u/lmsalmel/algbio12/AfB_lecture3_13092012.pdf
# A breakpoint is a position where the elements very by more than 1.
#
# Ex: 1 2|8 7
#        ^- Breakpoint here
#
# A strip is any contiguous sequence of elements that belong together. It can be increasing or decreasing.
#
# Ex: 9 1 2 3 7
#       -----   <- Increasing strip
#
# Ex: 3 7 6 5 1
#       -----   <- Decreasing strip
#
# Algorithm:
# while breakpoints > 0:
#     if there is a decreasing strip:
#         Find the swap that clears the most breakpoints
#     else:
#         Swap any increasing strip
#

# Read from dataset and parse into pairs of sequences
def get_sequences():
    file = open("dataset.txt", 'r')
    text = file.read().split('\n')
    file.close()
    
    pairs = []
    pairFirstItem = None
    
    for i, line in enumerate(text):
        if line:
            if pairFirstItem:
                pair = (pairFirstItem, line.split(' '))
                pairs.append(pair)
                pairFirstItem = None
            else:
                pairFirstItem = line.split(' ')

    return pairs
    
# Align a pair of sequences such that the first sequence is 1, 2, 3, ...
# and the second sequence has item mapped onto the first
def align_pair(pair):
    itemMap = {}
    for i, item in enumerate(pair[0]):
        itemMap[item] = i
        
    left = []
    right = []
    for i in range(len(pair[0])):
        left.append(i)
        right.append(itemMap[pair[1][i]])
        
    return (left, right)
    
# Find all breakpoints in a sequence
# A breakpoint is a position where the elements very by more than 1.
#
# Ex: 1 2|8 7
#        ^- Breakpoint here
#
# If a breakpoint exists between two items N and N+1, the breakpoint will be labelled N+0.5
def find_breakpoints(list):
    breakpoints = []
    
    if list[0] != 0:
        breakpoints.append(-0.5)
        
    for i in range(len(list)-1):
        if abs(list[i+1] - list[i]) != 1:
            breakpoints.append(i+0.5)
        
    if list[-1] != len(list)-1:
        breakpoints.append(len(list)-0.5)
        
    return breakpoints

# Return the input list, with indexFrom <--> indexTo (inclusive) swapped    
def swap(list, indexFrom, indexTo):
    result = []
    #result.extend(list[:indexFrom])
    #result.extend(list[indexFrom:indexTo+1][::-1])
    #result.extend(list[indexTo+1:])
    return list[:indexFrom] + list[indexFrom:indexTo+1][::-1] + list[indexTo+1:]
    
# Determine if the list has any decreasing strip
# Can be easily verified by finding any element N where the next element is N+1
# Strips of length 1 count as decreasing
def has_decreasing_strip(list):
    for i in range(len(list)-1):
    
        # Check for decreasing strip of length 1+
        if list[i+1] - list[i] == -1:
            return True
            
        # Check for decreasing strip of length 1
        if i == 0:
            if list[0] != 0:
                return True
        elif i == len(list)-1:
            if list[-1] != len(list)-1:
                return True
        else:
            if abs(list[i+1] - list[i]) != 1 and \
               abs(list[i-1] - list[i]) != 1:
                return True
            
    return False
    
# Determine if the list has any increasing strip
# Can be easily verified by finding any element N where the next element is N-1
# Strips of length 1 DO NOT count as increasing
def has_increasing_strip(list):
    for i in range(len(list)-1):
        # Check for increasing strip of length 1+
        if list[i+1] - list[i] == 1:
            return True
    return False
    
# Find the first increasing strip and swap it
def swap_any_increasing_strip(list):
    strip_start = None
    strip_end   = None
    for i in range(len(list)-1):
        if strip_start == None:
            if list[i+1] - list[i] == 1:
                strip_start = i
        else:
            if list[i+1] - list[i] != 1:
                strip_end = i
                # Ignore the increasing strip if it's a placed 0 at 0 position
                if strip_start == 0 and list[0] == 0:
                    strip_start = None
                    strip_end   = None
                else:
                    return swap(list, strip_start, strip_end)

# Return a list of all possible increasing strip swaps
def swap_increasing_strip(list):
    strip_start = None
    strip_end   = None
    swaps = []
    for i in range(len(list)-1):
        if strip_start == None:
            if list[i+1] - list[i] == 1:
                strip_start = i
        else:
            if list[i+1] - list[i] != 1:
                # Ignore the increasing strip if it's a placed 0 at 0 position
                if strip_start == 0 and list[0] == 0:
                    pass
                else:
                    strip_end = i
                    swaps.append(swap(list, strip_start, strip_end))            
                strip_start = None
                strip_end   = None
    return swaps
                    
def display_sequence(list):
    breakpoints = find_breakpoints(list)
    display = ''
    display += '|' if -0.5 in breakpoints else ' '
    for n, item in enumerate(list):
        display += str(item)
        display += '|' if (n+0.5) in breakpoints else ' '
    print(display)
    
# Find the minimum reversal distance
# Algorithm:
# if breakpoints == 0:
#     return 0
# else:
#     build a swap map of all possible swap scores to swap results
#     return 1 + min( reversal distance of all possible swaps of the highest score )
# If all swaps do not reduce the score, swap any increasing strip
cache = {}
def find_reversal_distance(list, level=0):
    #print(level*' ' + f'Level {level} --> {display_sequence(list)}')
    
    cache_key = ''.join([str(x) for x in list])
    global cache
    if cache_key in cache:
        return cache[cache_key].copy()
    
    breakpoints = find_breakpoints(list)
    num_breakpoints = len(breakpoints)
    
    if num_breakpoints == 0:
        return [0, []]
        
    swap_map = { 2: [], 1: [], 0: [] }
    best_swap_score = 0
    
    for i in range(num_breakpoints):
        for j in range(i+1, num_breakpoints):
            swapPoint1 = int(breakpoints[i]+0.5)
            swapPoint2 = int(breakpoints[j]-0.5)
            swapped = swap(list, swapPoint1, swapPoint2)
            
            # Score:
            #     2 - Removes 2 breakpoints [best score, return immediately]
            #     1.5 - Removes 1 breakpoint and flips an increasing strip
            #     1 - Removes 1 breakpoint and does not flip an increasing strip
            swap_score = num_breakpoints - len(find_breakpoints(swapped))
            swap_strip = list[swapPoint1:swapPoint2+1]
            
            if swap_score >= best_swap_score:
                best_swap_score = swap_score
                swap_map[swap_score].append([swapped, swapPoint1, swapPoint2, -1, []])
                
    if level == 0:
        #print(swap_map)
        pass
    
    swap_possibilities = swap_map[best_swap_score]
    for s in swap_possibilities:
        x = find_reversal_distance(s[0], level=level+1)
        distance, path = x
        s[3] = distance
        s[4] = path.copy()
        s[4].insert(0,(s[1], s[2]))
    best_swap = min(swap_possibilities, key=operator.itemgetter(0))
    #print(best_swap)
    result = 1 + best_swap[3]
    cache_entry = [result, s[4].copy()]
    cache[cache_key] = cache_entry
    return [result, s[4]]
    

if __name__=="__main__":
    pairs = get_sequences()
    print(pairs)
    
    for pair in pairs:
        # Flip the pair - we are going the opposite direction
        pair = (pair[1], pair[0])
        #print(pair)
        pair = align_pair(pair)
        #print(pair)
        reversals = find_reversal_distance(pair[1])
        
    #print(reversals)
    result = str(reversals[0])
    for swap_pair in reversals[1]:
        result += '\n' + ' '.join([str(s+1) for s in swap_pair])
        
    print(result)
    
    with open('result.txt', 'w') as fp:
        fp.write(result)