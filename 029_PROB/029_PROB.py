from math import log10

def getProb(str, gc):
    prob = 1.0
    at = (1.0 - gc)/2
    gc /= 2
    
    for ch in str:
        if ch == 'A' or ch == 'T':
            prob *= at
        else:
            prob *= gc
            
    return log10(prob)

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

str = data[0]
gc_list = [float(x) for x in data[1].split(' ')]

result = ''
for gc in gc_list:
    result += '%.3f ' % getProb(str, gc)
    
print result