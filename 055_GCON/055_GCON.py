DEBUG = False

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

MIN_UP = []
MIN_LEFT = []

for i in range(len(x)+1):
    if i == 0:
        inner = [0] + [GAP_PENALTY for i in range(len(y))]
    else:
        inner = [GAP_PENALTY] + ([0] * len(y))
    EDIT_DISTANCE.append(inner)
    MIN_UP.append(inner[:])
    MIN_LEFT.append(inner[:])
    
    
if DEBUG:
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(EDIT_DISTANCE)):
        row = EDIT_DISTANCE[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(MIN_UP)):
        row = MIN_UP[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        

    
for i in range(1, len(x)+1):
    for j in range(1, len(y)+1):
        up = MIN_UP[i-1][j] + GAP_PENALTY
        #up = EDIT_DISTANCE[0][j]
        #for i_ptr in range(1,i):
            #if EDIT_DISTANCE[i_ptr][j] < up: up = EDIT_DISTANCE[i_ptr][j]
        #up += GAP_PENALTY
        
        left = MIN_LEFT[i][j-1] + GAP_PENALTY
        #left = EDIT_DISTANCE[i][0]
        #for j_ptr in range(1,j):
            #if EDIT_DISTANCE[i][j_ptr] < up: up = EDIT_DISTANCE[i][j_ptr]
        #left += GAP_PENALTY
        
        upLeft = EDIT_DISTANCE[i-1][j-1] + BLOSUM62[x[i-1] + "/" + y[j-1]]
            
        ed = min(up, left, upLeft)
        EDIT_DISTANCE[i][j] = ed
        
        MIN_UP[i][j]   = min(ed, MIN_UP[i-1][j])
        MIN_LEFT[i][j] = min(ed, MIN_LEFT[i][j-1])
        
        #PREV_ACTION[i][j] = []
        #if ed == up:   PREV_ACTION[i][j].append("Up")
        #if ed == left: PREV_ACTION[i][j].append("Left")
   
   
if DEBUG:
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(EDIT_DISTANCE)):
        row = EDIT_DISTANCE[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        
    print 'MIN_UP'
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(MIN_UP)):
        row = MIN_UP[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        
    print 'MIN_LEFT'
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(MIN_LEFT)):
        row = MIN_LEFT[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
    
result = EDIT_DISTANCE[len(x)][len(y)] * -1
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()