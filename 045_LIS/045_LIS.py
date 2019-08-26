file = open('dataset.txt', 'r')
#file = open('dataset_small.txt', 'r')
data = file.read()
file.close()

lines = data.split('\n')
perm = [int(x) for x in lines[1].split(' ')]

incSeqs = []
decSeqs = []

index = 0
for x in perm:
    # --- INCREASING ---
    # Append the new number onto all lists where it currently fits
    # If it doesn't fit anywhere, create a new list where it is the only entry
    appended = False
    for seq in incSeqs:
        if x > seq[-1]:
            newSeq = seq[:]
            newSeq.append(x)
            incSeqs.append(newSeq)
            appended = True
            
    if not appended:
        incSeqs.append([x])
        
    # Check all entries and put the list with the smallest end number of each length into the final list
    # Discard all other entries
    smallestOfLength = {}
    for seq in incSeqs:
        seqLen = len(seq)
        if seqLen not in smallestOfLength:
            smallestOfLength[seqLen] = seq
        else:
            if seq[-1] < smallestOfLength[seqLen][-1]:
                smallestOfLength[seqLen] = seq
            
    incSeqs = smallestOfLength.values()
        
    # --- DECREASING ---
    # Append the new number onto all lists where it currently fits
    # If it doesn't fit anywhere, create a new list where it is the only entry
    appended = False
    for seq in decSeqs:
        if x < seq[-1]:
            newSeq = seq[:]
            newSeq.append(x)
            decSeqs.append(newSeq)
            appended = True
            
    if not appended:
        decSeqs.append([x])
        
    # Check all entries and put the list with the largest end number of each length into the final list
    # Discard all other entries
    largestOfLength = {}
    for seq in decSeqs:
        seqLen = len(seq)
        if seqLen not in largestOfLength:
            largestOfLength[seqLen] = seq
        else:
            if seq[-1] > largestOfLength[seqLen][-1]:
                largestOfLength[seqLen] = seq
            
    decSeqs = largestOfLength.values()
    
    if index % 100 == 0:
        print index
    index += 1
    #print incSeqs
    #print '----'
    
if 0:
    for seq in incSeqs:
        print ' '.join([str(x) for x in seq])
    print '-----'
    for seq in decSeqs:
        print ' '.join([str(x) for x in seq])
    print '-----'    

result = ''
    
maxLenInc = 0
maxLenIncSeq = []
for seq in incSeqs:
    if len(seq) > maxLenInc:
        maxLenInc = len(seq)
        maxLenIncSeq = seq
result += ' '.join([str(x) for x in maxLenIncSeq]) + '\n'

maxLenDec = 0
maxLenDecSeq = []
for seq in decSeqs:
    if len(seq) > maxLenDec:
        maxLenDec = len(seq)
        maxLenDecSeq = seq
result += ' '.join([str(x) for x in maxLenDecSeq])

print result

outFile = open('result.txt', 'w')
outFile.write(result)
outFile.close()