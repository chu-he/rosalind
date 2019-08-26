
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

file = open('BLOSUM62.txt')
data = file.read()
file.close()

BLOSUM62 = {}
from_aa = []
for line in data.split('\n'):
    if from_aa == []:
        from_aa = line.split()
    else:
        line = line.split()
        to_aa = line[0]
        for i in range(1,len(line)):
            score = -1 * int(line[i])
            BLOSUM62[from_aa[i-1] + "/" + to_aa] = score
            BLOSUM62[to_aa + "/" + from_aa[i-1]] = score
            
debugFile = open('debug.txt', 'w')
debugFile.write(str(BLOSUM62))
debugFile.close()

GAP_PENALTY = 5

#EDIT_DISTANCE[i][j] where i in range(x) and j in range(y)
EDIT_DISTANCE = []
j = 0
for i in range(len(x)+1):
    inner = ([0]*(len(y)+1)) if i != 0 else [GAP_PENALTY*i for i in range(len(y)+1)]
    inner[0] = j*GAP_PENALTY
    j += 1
    EDIT_DISTANCE.append(inner)
    
for i in range(1, len(x)+1):
    for j in range(1, len(y)+1):
        up   = EDIT_DISTANCE[i-1][j] + GAP_PENALTY
        left = EDIT_DISTANCE[i][j-1] + GAP_PENALTY
        upLeft = EDIT_DISTANCE[i-1][j-1] + BLOSUM62[x[i-1] + "/" + y[j-1]]
            
        EDIT_DISTANCE[i][j] = min(up, left, upLeft)
   
DEBUG = False
if DEBUG:
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(EDIT_DISTANCE)):
        row = EDIT_DISTANCE[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
    
result = EDIT_DISTANCE[len(x)][len(y)] * -1
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()