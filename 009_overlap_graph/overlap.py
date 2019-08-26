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
    
def CheckOverlap(left, right, overlapLength):
    return (left[-overlapLength:] == right[:overlapLength])

# Start program execution -------------------------------------
# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

dict = ReadFASTA(data)
keys = dict.keys()
numkeys = len(dict.keys())

result = ''
for k1 in range(numkeys):
    for k2 in range(k1, numkeys):
        if k1 != k2:
            if CheckOverlap(dict[keys[k1]], dict[keys[k2]], 3):
                result += keys[k1] + ' ' + keys[k2] + '\n'
            if CheckOverlap(dict[keys[k2]], dict[keys[k1]], 3):
                result += keys[k2] + ' ' + keys[k1] + '\n'

print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()