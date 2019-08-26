from math import factorial

file = open('dataset.txt', 'r')
data = file.read()
file.close()

lines = data.split('\n')
rstr = lines[1]

numA = 0
numC = 0
for ch in rstr:
    if ch == 'A':
        numA += 1
    if ch == 'C':
        numC += 1
        
result = str(factorial(numA) * factorial(numC))
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()