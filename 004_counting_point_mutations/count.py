#import string

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

str1 = data[0]
str2 = data[1]

diff = 0
for i in range(len(str1)):
    if str1[i] != str2[i]:
        diff += 1
        
result = str(diff)
        
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()