file = open('dataset.txt', 'r')
data = file.read()
file.close()

lines = data.split('\n')
seq = ''.join(lines[1:])
print seq

FAILURE_ARRAY = ['0']

FAILURE_POSSIBILITIES = {}
# Build the failure possibilities set
prefix = ''
for i in range(0, len(seq)):
    if i % 1000 == 0:
        print i
    prefix += seq[i]
    FAILURE_POSSIBILITIES[prefix] = i+1
    #print "{0} --> {1}".format(prefix, i)

print "Done constructing possibilities"
    
# For each index, check each possible subsequence starting from the longest if it is in FAILURE_POSSIBILITIES
# Check subsequence lengths from prev_k+1 to 1
prevK = 0
for i in range(1, len(seq)):
    if i % 1000 == 0:
        print i
    
    k = 0
    for tryK in range(prevK+1, 0, -1):
        subseq = seq[i-tryK+1:i+1]
        if subseq in FAILURE_POSSIBILITIES:
            k = len(subseq)
            break
    FAILURE_ARRAY.append(str(k))
    prevK = k
    

result = ' '.join(FAILURE_ARRAY)
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()