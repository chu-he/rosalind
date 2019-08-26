
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

# Direction can be: UP, LEFT, or UPLEFT
DIRECTION = []
j = 0
for i in range(len(x)+1):
    inner = ([0]*(len(y)+1)) if i != 0 else range(len(y)+1)
    inner[0] = j
    j += 1
    EDIT_DISTANCE.append(inner)
    DIRECTION.append([""]*(len(y)+1))
    
for i in range(1, len(x)+1):
    for j in range(1, len(y)+1):
        up   = EDIT_DISTANCE[i-1][j] + 1
        left = EDIT_DISTANCE[i][j-1] + 1
        
        upLeft = EDIT_DISTANCE[i-1][j-1]
        if x[i-1] != y[j-1]:
            upLeft += 1
            
        m = min(up, left, upLeft)
        EDIT_DISTANCE[i][j] = m
        if m == up:
            DIRECTION[i][j] = "UP"
        elif m == left:
            DIRECTION[i][j] = "LEFT"
        else:
            DIRECTION[i][j] = "UPLEFT"
   
DEBUG = False
if DEBUG:
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(EDIT_DISTANCE)):
        row = EDIT_DISTANCE[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [str(e) for e in row])
        
        
    directional = { "UP": "^",
                    "LEFT": "<",
                    "UPLEFT": "*",
                    "": "" }
    print ''
    print '\t'.join([' ', '#'] + list(y))
    for i in range(len(DIRECTION)):
        row = DIRECTION[i]
        x_ch = '#' if i == 0 else x[i-1]
        print '\t'.join([x_ch] + [directional[e] for e in row])
    
# Travel backwards on the DIRECTION grid to find the alignment
x_p = len(x)
y_p = len(y)
aligned_x = ""
aligned_y = ""
while x_p != 0 and y_p != 0:
    direction = DIRECTION[x_p][y_p]
    
    if direction == "LEFT":
        aligned_x = "-"      + aligned_x
        aligned_y = y[y_p-1] + aligned_y
        y_p -= 1
        
    elif direction == "UP":
        aligned_x = x[x_p-1] + aligned_x
        aligned_y = "-" + aligned_y
        x_p -= 1
        
    # UPLEFT
    else:
        aligned_x = x[x_p-1] + aligned_x
        aligned_y = y[y_p-1] + aligned_y
        x_p -= 1
        y_p -= 1
        
while x_p != 0:
    aligned_x = x[x_p-1] + aligned_x
    aligned_y = "-" + aligned_y
    x_p -= 1
    
while y_p != 0:
    aligned_x = "-"      + aligned_x
    aligned_y = y[y_p-1] + aligned_y
    y_p -= 1
    
result = "{0}\n{1}\n{2}".format(EDIT_DISTANCE[len(x)][len(y)], aligned_x, aligned_y)
print result

outFile = open('result.txt', 'w')
outFile.write(str(result))
outFile.close()