reverse = {}
reverse['A'] = 'T'
reverse['T'] = 'A'
reverse['C'] = 'G'
reverse['G'] = 'C'

file = open('dataset.txt', 'r')
data = file.read()
file.close()

strings = data.split()
first = strings[0]

rcs = []
for s in strings:
    rc = ""
    for i in range(len(s)-1, -1, -1):
        rc += reverse[s[i]]
    if rc not in rcs: rcs.append(rc)
    
strings.extend(rcs)
strings.sort()

debru = {}
for s in strings:
    a = s[:-1]
    b = s[1:]
    
    if a not in debru:
        debru[a] = [b]
    else:
        debru[a].append(b)
        
    if b not in debru:
        debru[b] = [a]
    else:
        debru[b].append(a)
        
node = first[1:]
prev = None
cycle = []
while node not in cycle:
    cycle.append(node)
    for next in debru[node]:
        if next != prev and next[:-1] == node[1:]:
            prev = node
            node = next
            break

while len(cycle) > 1:
    a = cycle.pop()
    b = cycle.pop()
    cycle.append(b[0] + a)

result = cycle[0][len(first)-2:]
print result

outfile = open('result.txt', 'w')
outfile.write(result)
outfile.close()