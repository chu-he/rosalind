def readFASTA(data):
    data = data.split('\n')
    strings = []
    strName = ''
    str = ''
    
    for line in data:
        if line[0] == '>':
            if strName != '':
                strings.append((strName, str))
            strName = line[1:]
            str = ''
        else:
            str += line
            
    if strName != '':
        strings.append((strName, str))
            
    return strings

file = open('dataset.txt', 'r')
data = file.read()
file.close()

s = readFASTA(data)[0][1]
alphabet = ['A', 'C', 'G', 'T']

kmers = []
count = {}
for ch1 in alphabet:
    for ch2 in alphabet:
        for ch3 in alphabet:
            for ch4 in alphabet:
                kmer = ch1 + ch2 + ch3 + ch4
                kmers.append(kmer)
                count[kmer] = 0
                
for i in range(len(s)-3):
    count[s[i:i+4]] += 1
    
result = ''
for kmer in kmers:
    result += str(count[kmer]) + ' '
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()