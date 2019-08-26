def swap(seq, start, end):
    newSeq = []
    for i in range(0, start):
        newSeq.append(seq[i])
    for i in range(end, start-1, -1):
        newSeq.append(seq[i])
    for i in range(end+1, len(seq)):
        newSeq.append(seq[i])
    print('Swap {0} from {1} to {2} --> {3}'.format(seq, start, end, newSeq))
    return newSeq
   
   
def countMatch(x, y):
    score = 0
    for i in range(0, len(x)):
        if x[i] == y[i]:
            score += 1
        else:
            break
    for i in range(len(x)-1, -1, -1):
        if x[i] == y[i]:
            score += 1
        else:
            break
    print('Score {0} vs {1} --> {2}'.format(x, y, score))
    return score


def reversal_distance(p, s):
    # Initialize pointers for beginning and end
    frontPtr = 0
    endPtr = len(p) - 1
    dist = 0
    
    # Repeat until the pointers meet
    while frontPtr != endPtr:
        # Advance the front pointer until the front numbers no longer match
        while p[frontPtr] == s[frontPtr] and frontPtr != endPtr:
            frontPtr += 1
            
        # Advance the end pointer until the end numbers no longer match
        while p[endPtr] == s[endPtr] and frontPtr != endPtr:
            endPtr -= 1
            
        # If the pointers match, both sequences fully match
        if frontPtr == endPtr:
            None
            
        else:
            # Swaps are needed
            dist += 1
            
            # Try swapping to match the front, and count how many elements match for the result
            sFront = s[frontPtr]
            pSwapFrontIdx = p.index(sFront)
            pSwappedFront = swap(p, frontPtr, pSwapFrontIdx)
            frontSwapScore = countMatch(pSwappedFront, s)
            
            # Try swapping to match the end, and count how many elements match for the result
            sEnd = s[endPtr]
            pSwapEndIdx = p.index(sEnd)
            pSwappedEnd = swap(p, pSwapEndIdx, endPtr)
            endSwapScore = countMatch(pSwappedEnd, s)
            
            # Choose the higher score to replace p (equal scores don't matter)
            if frontSwapScore > endSwapScore:
                p = pSwappedFront
            else:
                p = pSwappedEnd
            print ''
            
    return dist
        

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

pi    = [int(x) for x in data[0].split(' ')]
sigma = [int(x) for x in data[1].split(' ')]
print 'pi    = {0}'.format(pi)
print 'sigma = {0}'.format(sigma)

result = reversal_distance(pi, sigma)
print 'dist  = {0}'.format(result)

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()