#import string

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
    
result = ''
for i in range(len(data)/3):
    codon = data[i*3:(i+1)*3]
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