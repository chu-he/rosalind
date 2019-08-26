from decimal import *

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

file = open('table.txt', 'r')
table_text = file.read().split('\n')
file.close()

mass_table = {}
for line in table_text:
    line = line.split()
    mass_table[line[0]] = Decimal(line[1])
    
mass = Decimal(0)
for ch in data:
    mass += mass_table[ch]

mass = round(mass, 2)
    
result = str(mass)
print result
    
# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()