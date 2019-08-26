#import string

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

super = data[0]
sub = data[1]
sub_len = len(sub)

result = ''
for i in range(len(super)-sub_len+1):
    if super[i:i+sub_len] == sub:
        result += str(i+1) + ' '
        
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()