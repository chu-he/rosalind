def getExpected(n, s, gc):
    at = (1-gc)/2
    gc /= 2
    
    result = 1.0
    for ch in s:
        if ch == 'A' or ch == 'T':
            result *= at
        else:
            result *= gc
            
    return result*(n-len(s)+1)

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

n = int(data[0])
s = data[1]
A = [float(x) for x in data[2].split(' ')]

result = []
for a_i in A:
    result.append(getExpected(n, s, a_i))
    
result = ' '.join(['%.3f' % x for x in result])
print result


outfile = open('result.txt', 'w')
outfile.write(str(result))
outfile.close()
