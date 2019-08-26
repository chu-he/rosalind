# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

reverse = {}
reverse['A'] = 'T'
reverse['T'] = 'A'
reverse['C'] = 'G'
reverse['G'] = 'C'

result = ''
for c in reversed(data):
    result += reverse[c]
    
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()