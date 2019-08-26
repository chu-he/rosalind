
file = open('dataset.txt', 'r')
data = file.read()
file.close()

sequences = []
seq = ''
for line in data.split('\n'):
    if line != '' and line[0] == '>':
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

file = open('PAM250.txt')
data = file.read()
file.close()

SCORE_MATRIX = {}
from_aa = []
for line in data.split('\n'):
    if from_aa == []:
        from_aa = line.split()
    else:
        line = line.split()
        to_aa = line[0]
        for i in range(1,len(line)):
            score = int(line[i])
            SCORE_MATRIX[from_aa[i-1] + "/" + to_aa] = score
            SCORE_MATRIX[to_aa + "/" + from_aa[i-1]] = score
            
debugFile = open('debug.txt', 'w')
debugFile.write(str(SCORE_MATRIX))
debugFile.close()

GAP_PENALTY = 5

#EDIT_DISTANCE[i][j] where i in range(x) and j in range(y)
EDIT_DISTANCE = []
PREV = []
j = 0
for i in range(len(x)+1):
    inner = ([0]*(len(y)+1)) if i != 0 else [-GAP_PENALTY*k for k in range(len(y)+1)]
    inner[0] = -j*GAP_PENALTY
    j += 1
    EDIT_DISTANCE.append(inner)
    
    innerPrev = (['-'] + (['L'] * len(y))) if i == 0 else (['U'] + ['']*(len(y)))
    PREV.append(innerPrev)
    
for i in range(1, len(x)+1):
    for j in range(1, len(y)+1):
        up   = EDIT_DISTANCE[i-1][j] - GAP_PENALTY
        left = EDIT_DISTANCE[i][j-1] - GAP_PENALTY
        upLeft = EDIT_DISTANCE[i-1][j-1] + SCORE_MATRIX[x[i-1] + "/" + y[j-1]]
            
        ed = max(up, left, upLeft)
        EDIT_DISTANCE[i][j] = ed
        
        if ed == upLeft:
            PREV[i][j] += 'X'
        if ed == up:
            PREV[i][j] += 'U'
        if ed == left:
            PREV[i][j] += 'L'
   
DEBUG = False
if DEBUG:
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(EDIT_DISTANCE)):
        row = EDIT_DISTANCE[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(PREV)):
        row = PREV[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        
x_ptr = len(x)
y_ptr = len(y)
aligned_x = ''
aligned_y = ''

max_ed = EDIT_DISTANCE[x_ptr][y_ptr]
max_loc = (x_ptr, y_ptr)

min_ed = EDIT_DISTANCE[0][0]
min_loc = (0, 0)
while x_ptr > 0 or y_ptr > 0:
    print '({0}, {1}) - {2}'.format(x_ptr, y_ptr, EDIT_DISTANCE[x_ptr][y_ptr])
    if EDIT_DISTANCE[x_ptr][y_ptr] > max_ed:
        max_ed = EDIT_DISTANCE[x_ptr][y_ptr]
        max_loc = (x_ptr, y_ptr)
    if EDIT_DISTANCE[x_ptr][y_ptr] < min_ed:
        min_ed = EDIT_DISTANCE[x_ptr][y_ptr]
        min_loc = (x_ptr, y_ptr)
        
    if 'X' in PREV[x_ptr][y_ptr]:
        aligned_x = x[x_ptr-1] + aligned_x
        x_ptr -= 1
        
        aligned_y = y[y_ptr-1] + aligned_y
        y_ptr -= 1
        
    elif 'U' in PREV[x_ptr][y_ptr]:
        aligned_x = x[x_ptr-1] + aligned_x
        x_ptr -= 1
        
        aligned_y = '-' + aligned_y
        
    elif 'L' in PREV[x_ptr][y_ptr]:
        aligned_y = y[y_ptr-1] + aligned_y
        y_ptr -= 1
        
        aligned_x = '-' + aligned_x
        
print EDIT_DISTANCE[-1][-1]
print 'a_x = {0}'.format(aligned_x)
print 'a_y = {0}'.format(aligned_y)
print max_ed
print max_loc
print min_ed
print min_loc
# Go backwards on the PREV 2D array and rebuild the aligned strings
# While going backwards, find the MAX and MIN score along the range
# Find the substrings of each string using the MAX and MIN score as pointers

sub_x = x[min_loc[0]:max_loc[0]]
sub_y = y[min_loc[1]:max_loc[1]]
    
result = '{0}\n{1}\n{2}'.format(max_ed - min_ed, sub_x, sub_y)
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()