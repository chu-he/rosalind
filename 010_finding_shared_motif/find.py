import string

nucleotides = ['A', 'C', 'G', 'T']

# in : data - Raw data containing FASTA format
# out: dict - Dictionary containing mapping from name -> sequence
def ReadFASTA(data):
    data = data.split('\n')
    dict = {}

    for i in range(len(data)):
        if data[i][0] == '>':
            strname = data[i][1:]
            dict[strname] = ''
        else:
            dict[strname] += data[i]
            
    return dict

# Start program execution -------------------------------------
# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

# Find the shortest string in the list
shortest = data[0]
for s in data:
    if len(s) < len(shortest):
        shortest = s
data.remove(shortest)

# Build the list of all substrings of the shortest string
shortest_subs = [shortest]
for length in range(len(shortest)-1, 0, -1):
    for start in range(len(shortest)-length+1):
        shortest_subs.append(shortest[start:start+length])
        
# Check each substring to see if the other strings contain it
for substr in shortest_subs:
    found = True
    for s in data:
        if string.find(s, substr) == -1:
            found = False
            break
            
    if found:
        result = substr
        break
    else:
        print 'Check ' + substr + ' failed.'
        
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()