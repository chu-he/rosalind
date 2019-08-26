nucleotides = ['A', 'C', 'G', 'T']

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

dict = {}

for i in range(len(data)):
    if data[i][0] == '>':
        strname = data[i][1:]
        dict[strname] = ''
    else:
        dict[strname] += data[i]
    
max = 0    
for k in dict.keys():
    percentage = float(dict[k].count('C') + dict[k].count('G'))/len(dict[k])
    if percentage > max:
        max_k = k
        max = percentage
        
result = str(max_k)
result += '\n'
result += str(round(max * 100, 2)) + '%'

print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()