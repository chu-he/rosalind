nucleotides = ['A', 'C', 'G', 'T']

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

profile = []

con_str = ''
for column in range(len(data[0])):
    # Build profile for this column
    dict = {}
    for n in nucleotides: dict[n] = 0
    
    for row in range(len(data)):
        dict[data[row][column]] += 1
        
    # Get the consensus char
    max = 0
    for k in nucleotides:
        if dict[k] > max:
            con = k
            max = dict[k]
            
    con_str += con
    
    profile.append(dict)

result = con_str
for n in nucleotides:
    result += '\n' + n + ':'
    for p in profile:
        result += ' ' + str(p[n])
        
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()