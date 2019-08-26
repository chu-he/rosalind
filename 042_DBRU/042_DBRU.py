reverse = {}
reverse['A'] = 'T'
reverse['T'] = 'A'
reverse['C'] = 'G'
reverse['G'] = 'C'

file = open('dataset.txt', 'r')
data = file.read()
file.close()

strings = data.split()

rcs = []
for s in strings:
    rc = ""
    for i in range(len(s)-1, -1, -1):
        rc += reverse[s[i]]
    if rc not in rcs: rcs.append(rc)
    
strings.extend(rcs)
strings.sort()

adj = []
for s in strings:
    edge = (s[:-1], s[1:])
    if edge not in adj: adj.append(edge)

result = '\n'.join(('(%s, %s)' % (a,b) for (a,b) in adj))


print result
outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()