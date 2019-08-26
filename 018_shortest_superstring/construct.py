nucleotides = ['A', 'C', 'G', 'T']

def CheckOverlap(left, right, overlapLength):
    return (left[-overlapLength:] == right[:overlapLength])
    
def Concatenate(left, right, overlapLength):
    return left + right[overlapLength:]

# Start program execution -------------------------------------
# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

strings = data.split('\n')
strLen = len(strings[0])

for overlap in range(strLen, strLen/2 - 1, -1):
    print 'Checking overlap length = ' + str(overlap)
    
    l = 0
    while l < len(strings):
        r = 0
        while r < len(strings):
            if l != r:
                left  = strings[l]
                right = strings[r]
                
                if CheckOverlap(left, right, overlap):
                    concatenated = Concatenate(left, right, overlap)
                    print 'Overlapping ' + left + ' and ' + right + ' = ' + concatenated
                    strings.remove(left)
                    strings.remove(right)
                    strings.append(concatenated)
                    l = 0
                    r = 0
                    
            r += 1
        l += 1
    
print strings
print

result = ' '.join(strings)
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()