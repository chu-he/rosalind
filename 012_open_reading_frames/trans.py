import string

start_protein = 'M' # AUG
stop_protein  = 'Stop'

def FindProteins(data):
    proteins = []
    currentProteins = []
    proteinStarted = False
    
    while len(data) >= 3:
        codon = data[:3]
        data = data[3:]
        
        amino = amino_lookup[codon]
        
        if amino == start_protein:
            if proteinStarted:
                currentProteins = [p+amino for p in currentProteins]
            currentProteins.append(amino)
            proteinStarted = True
            
        elif amino == stop_protein:
            if len(currentProteins) != 0:
                for p in currentProteins: proteins.append(p)
                currentProteins = []
                proteinStarted = False
                
        else:
            if proteinStarted:
                currentProteins = [p+amino for p in currentProteins]

    return proteins
    
def ReverseComplement(data):
    reverse = {}
    reverse['A'] = 'T'
    reverse['T'] = 'A'
    reverse['C'] = 'G'
    reverse['G'] = 'C'

    result = ''
    for c in reversed(data):
        result += reverse[c]
        
    return result

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

revcom = ReverseComplement(data)
data   = string.replace(data, 'T', 'U')
revcom = string.replace(revcom, 'T', 'U')

proteins = []
# Check original string for proteins
for p in FindProteins(data): proteins.append(p)

data = data[1:] # Shift reading frame 1 position
for p in FindProteins(data): proteins.append(p)
    
data = data[1:]
for p in FindProteins(data): proteins.append(p)

# Check reverse complement for proteins
for p in FindProteins(revcom): proteins.append(p)

revcom = revcom[1:]
for p in FindProteins(revcom): proteins.append(p)
    
revcom = revcom[1:]
for p in FindProteins(revcom): proteins.append(p)

# Uniquify the list of proteins
unique = []
for p in proteins:
    if p not in unique: unique.append(p)

result = '\n'.join(unique)
print result
    
# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()