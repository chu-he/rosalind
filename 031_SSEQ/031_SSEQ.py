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

# ---------------------------------------------------

def getSubsequence(a, b):
    indexes = []
    for ch in b:
        if indexes == []:
            startIndex = 0
        else:
            startIndex = indexes[-1]+1
        i = a.find(ch, startIndex)
        indexes.append(i)
    return indexes

strings = readFASTA(data)

result = ' '.join(str(x+1) for x in getSubsequence(strings[0][1], strings[1][1]))
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()