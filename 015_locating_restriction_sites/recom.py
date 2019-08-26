reverse = {}
reverse['A'] = 'T'
reverse['T'] = 'A'
reverse['C'] = 'G'
reverse['G'] = 'C'

def ReverseComplement(string):
    revcom = ''
    for ch in reversed(string):
        revcom += reverse[ch]
        
    return revcom

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

result = ''

data_length = len(data)
for start in range(data_length-4):
    for end in range(start+4, start+9):
        if end <= data_length:
            substring = data[start:end]
            if substring == ReverseComplement(substring):
                result += str(start+1) + ' ' + str(end-start) + '\n'
                
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()