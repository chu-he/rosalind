import math

file = open('dataset.txt', 'r')
data = file.read()
file.close()

lines = data.split('\n')
seq = ''.join(lines[1:])
print seq

count = { 'A': 0,
          'U': 0,
          'C': 0,
          'G': 0 }
for ch in seq:
    count[ch] += 1
    
print count

def findCombinations( base1, base2 ):
    if base1 > base2:
        a = base1
        b = base2
    else:
        a = base2
        b = base1
        
    return math.factorial(a) / math.factorial(a - b)
    
result = findCombinations( count['A'], count['U'] ) * \
         findCombinations( count['C'], count['G'] )
    
print result
outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()