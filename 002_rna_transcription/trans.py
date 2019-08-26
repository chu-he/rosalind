import string

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = string.replace(data, 'T', 'U')

print data