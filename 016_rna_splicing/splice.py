import string

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

file = open('table.txt', 'r')
table = file.read().split('\n')
file.close()

amino_lookup = {}
for line in table:
    line = line.split(' ')
    amino_lookup[line[0]] = line[1]

data = data.split('\n')
sequence = data[0]
introns = data[1:]

for i in introns:
    sequence = string.replace(sequence, i, '')
    
sequence = string.replace(sequence, 'T', 'U')
    
result = ''
for i in range(len(sequence)/3):
    codon = sequence[i*3:(i+1)*3]
    amino = amino_lookup[codon]
    
    if amino == 'Stop':
        break
    else:
        result += amino
        
print result
    
# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()