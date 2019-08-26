# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

nucleotides = ['A', 'C', 'G', 'T']

dict = {}
for x in nucleotides:
    dict[x] = 0

for c in data:
    dict[c] = dict[c]+1
    
for n in nucleotides:
    print dict[n],