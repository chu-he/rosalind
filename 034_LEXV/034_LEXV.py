def buildStrings(alpha, n, header):
    if n == 0: return []
    
    result = []
    for ch in alpha:
        result.append(header+ch)
        result.extend(buildStrings(alpha, n-1, header+ch))
    return result

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

alpha = data[0].split(' ')
n = int(data[1])

result = '\n'.join(buildStrings(alpha, n, ''))

outfile = open('result.txt', 'w')
outfile.write(str(result))
outfile.close()