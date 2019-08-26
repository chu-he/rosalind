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

strings = readFASTA(data)

result = ''
for s in strings:
    result += s[0] + '\n' + s[1] + '\n'
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()