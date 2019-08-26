
file = open('dataset.txt', 'r')
data = file.read()
file.close()

sequences = []
seq = ''
for line in data.split('\n'):
    if line[0] == '>':
        if seq != '':
            sequences.append(seq)
            seq = ''
    else:
        seq += line
sequences.append(seq)

x = sequences[0]
y = sequences[1]
print 'x = {0}'.format(x)
print 'y = {0}'.format(y)

#EDIT_DISTANCE[i][j] where i in range(x) and j in range(y)
EDIT_DISTANCE = []
j = 0
for i in range(len(x)+1):
    inner = ([0]*(len(y)+1)) if i != 0 else range(len(y)+1)
    inner[0] = j
    j += 1
    EDIT_DISTANCE.append(inner)
    
for i in range(1, len(x)+1):
    for j in range(1, len(y)+1):
        up   = EDIT_DISTANCE[i-1][j] + 1
        left = EDIT_DISTANCE[i][j-1] + 1
        
        upLeft = EDIT_DISTANCE[i-1][j-1]
        if x[i-1] != y[j-1]:
            upLeft += 1
            
        EDIT_DISTANCE[i][j] = min(up, left, upLeft)
   
DEBUG = False
if DEBUG:
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(EDIT_DISTANCE)):
        row = EDIT_DISTANCE[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
    
result = EDIT_DISTANCE[len(x)][len(y)]
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()