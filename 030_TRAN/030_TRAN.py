def isTransition(a, b):
    if (a == 'A' and b == 'G') or \
       (a == 'G' and b == 'A') or \
       (a == 'C' and b == 'T') or \
       (a == 'T' and b == 'C'):
        return True
    return False

def getTransRatio(s1, s2):
    transitions   = 0.0
    transversions = 0.0
    for i in range(len(s1)):
        a = s1[i]
        b = s2[i]
        if a != b:
            if isTransition(a, b):
                transitions += 1.0
            else:
                transversions += 1.0
            
    print transitions
    print transversions
    return transitions / transversions

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

# Drop the first line, start from the second
# Append the strings until we run into a '>' character
# Then start the second string
state = 1
s1 = ''
s2 = ''
for line in data[1:]:
    if line[0] == '>':
        state = 2
    else:
        if state == 1:
            s1 += line
        else:
            s2 += line

print getTransRatio(s1, s2)