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
    
def findDist(a, b):
    diff = 0.0
    for i in range(len(a)):
        if a[i] != b[i]:
            diff += 1.0
    return diff / len(a)

file = open('dataset.txt', 'r')
data = file.read()
file.close()

strings = readFASTA(data)

results = []    
for a in range(len(strings)):
    dists = []
    for b in range(len(strings)):
        dists.append(findDist(strings[a][1], strings[b][1]))
    results.append(dists)

result = ''
for r in results:
    result += ' '.join(['%.5f' % x for x in r]) + '\n'
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()