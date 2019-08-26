#import string

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

file = open('table.txt', 'r')
table = file.read().split('\n')
file.close()

possible_rna = {}
for line in table:
    line = line.split(' ')
    protein = line[1]
    if protein in possible_rna.keys():
        possible_rna[protein] += 1
    else:
        possible_rna[protein] = 1
    
possible = 1
for ch in data:
    possible *= possible_rna[ch]
    
# Multiply by 3 for the Stop codon
possible *= 3
    
result = str(possible)
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()