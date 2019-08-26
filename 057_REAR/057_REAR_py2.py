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

DEBUG = True


# Swaps the elements in the sequence between the start and end (inclusive) indices
def swap(seq, start, end):
    newSeq = []
    for i in range(0, start):
        newSeq.append(seq[i])
    for i in range(end, start-1, -1):
        newSeq.append(seq[i])
    for i in range(end+1, len(seq)):
        newSeq.append(seq[i])
    #print('Swap {0} from {1} to {2} --> {3}'.format(seq, start, end, newSeq))
    return newSeq


# Get a list of the breakpoints in the sequence
# Breakpoints are represented as halves and the list is guaranteed to be sorted
# The endpoints are breakpoints if they are not the minimal and maximal values
# Ex. A breakpoint of 1.5 denotes a breakpoint exists between 1 and 2
def get_breakpoints(x):
    bps = []

    if x[0] != 0:
        bps.append(-0.5)

    for i in range(0, len(x)-1):
        if abs(x[i] - x[i+1]) > 1:
            bps.append(i + 0.5)

    if x[-1] != 9:
        bps.append(len(x)-0.5)

    print '{0} has breakpoints at: {1}'.format(x, bps)
    
    if DEBUG:
        s = ''
        for i in range(len(x)):
            if (i - 0.5) in bps:
                s += '|'
            else:
                s += ' '
            s += str(x[i])
        if (len(x) - 0.5) in bps:
            s += '|'
        print s
        
        d = '|' if -0.5 in bps else ' '
        for i in range(len(x)):
            this = x[i]
            
            # Figure out relation to previous char
            if (i-1) >= 0:
                prev = x[i-1]
                diff = abs(this - prev)
                
                if diff >= 2:
                    d += '|'
                else:
                    if this - prev == 1:
                        d += '>>'
                    else:
                        d += '<<'
            
            # Figure out relation to next char
            if (i+1) < len(x):
                next = x[i+1]
                diff = abs(next - this)
                
                if diff >= 2:
                    if d[-1] == '|':
                        d += 'O|'
                    else:
                        d += '|'
                else:
                    if next - this == 1:
                        d += '>'
                    else:
                        d += '<'
            
        print d
    
    return bps


# Counts the number of breakpoints in a sequence
def count_breakpoints(x):
    b = len(get_breakpoints(x))
    print('{0} has {1} breakpoints'.format(x, b))
    return b


# Checks whether the sequence has any decreasing strips
# Strips of length 1 count as decreasing
def has_decreasing_strip(x):
    print 'Checking for decreasing strips'
    bps = get_breakpoints(x)
    
    for i in range(0, len(bps)-1):
        sub = x[int(bps[i]+0.5):int(bps[i+1]-0.5+1)]
        print ' Checking {0}'.format(sub)

        decreasing = True
        
        if len(sub) > 1:
            for j in range(0, len(sub)-1):
                if sub[j] - sub[j+1] != 1:
                    decreasing = False

        if decreasing:
            print ' * Decreasing strip found'
            return True

    print ' * Decreasing strip not found'
    return False
    
    
# Checks whether the sequence has any increasing strips
# Strips of length 1 do NOT count as increasing
def has_increasing_strip(x):
    print 'Checking for increasing strips'
    bps = get_breakpoints(x)
    
    for i in range(0, len(bps)-1):
        sub = x[int(bps[i]+0.5):int(bps[i+1]-0.5+1)]
        print ' Checking {0}'.format(sub)

        increasing = True
        
        if len(sub) > 1:
            for j in range(0, len(sub)-1):
                if sub[j+1] - sub[j] != 1:
                    increasing = False
        else:
            increasing = False

        if increasing:
            print ' * increasing strip found'
            return True

    print ' * increasing strip not found'
    return False


# Attempts all swaps between all breakpoints
# The best possible swap removes 2 breakpoints - there can be any number of "best swaps"
# When a 2-bp swap is found, return immediately
# Otherwise, return a 1-bp swap
# If there are only 0-bp swaps, something when horribly wrong
def find_best_swap(x):
    bp = count_breakpoints(x)
    bps = get_breakpoints(x)

    best_swap = []
    # Score:
    #     2 - Removes 2 breakpoints
    #     1.5 - Removes 1 breakpoint and flips an increasing strip
    #     1 - Removes 1 breakpoint and does not flip an increasing strip
    best_bp_diff = -99

    for i in range(0, len(bps)-1):
        for j in range(i+1, len(bps)):
            swap_from = int(bps[i]+0.5)
            swap_to = int(bps[j]-0.5)
            
            new_x = swap(x, swap_from, swap_to)
            new_bp = count_breakpoints(new_x)

            bp_diff = bp - new_bp
            print ' bp difference = {0}'.format(bp_diff)

            if bp_diff == 2:
                print ' Best swap found, returning immediately'
                print ' {0}'.format(x)
                print ' {0}'.format(new_x)
                return new_x
            elif bp_diff == 1:
                if has_increasing_strip(x[swap_from:swap_to+1]):
                    bp_diff += 0.5
                    
                if bp_diff > best_bp_diff:
                    best_bp_diff = bp_diff
                    best_swap = new_x

    print ' {0}-bp Swap found'.format(abs(best_bp_diff))
    print ' {0}'.format(x)
    print ' {0}'.format(best_swap)

    return best_swap


# Finds any increasing strip, and swaps it
def swap_increasing_strip(x):
    print 'Checking for longest increasing strip'
    bps = get_breakpoints(x)

    longest = 0
    longest_strip = (0, 0)

    for i in range(0, len(bps)-1):
        swap_from = int(bps[i]+0.5)
        swap_to   = int(bps[i+1]-0.5)
        sub = x[swap_from:swap_to+1]
        print ' Checking {0}'.format(sub)

        increasing = len(sub) > 1
        for j in range(0, len(sub)-1):
            if sub[j+1] - sub[j] != 1:
                increasing = False

        if increasing:
            len_swap = swap_to - swap_from
            if len_swap > longest:
                longest = len_swap
                longest_strip = (swap_from, swap_to)

    new_x = swap(x, longest_strip[0], longest_strip[1])
    print ' Swapped increasing strip'
    print ' {0}'.format(x)
    print ' {0}'.format(new_x)
    return new_x


def reversal_distance(p, s):
    print 'pi    = {0}'.format(p)
    print 'sigma = {0}'.format(s)
    
    # Replace p by the positions of p's elements in s, and s by the positions
    p = [s.index(x) for x in p]
    s = range(0, len(s))
    print 'p = {0}'.format(p)
    print 's = {0}'.format(s)

    dist = 0

    while count_breakpoints(p) > 0:
        #print ''

        dist += 1
        if has_decreasing_strip(p):
            p = find_best_swap(p)
        else:
            p = swap_increasing_strip(p)

        #print ''

    print 'dist  = {0}'.format(dist)
    return dist


file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

pairs = []
i = 0
while i+1 < len(data):
    p = [int(x) for x in data[i].split(' ')]
    s = [int(x) for x in data[i+1].split(' ')]
    pairs.append( (p, s) )
    i += 3
    
result = []
for pair in pairs:
    result.append(reversal_distance(pair[0], pair[1]))


outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()