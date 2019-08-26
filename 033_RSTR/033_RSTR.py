def getStrChance(str, gc):
    at = (1-gc)/2
    gc /= 2
    
    chance = 1.0
    for ch in str:
        if ch == 'A' or ch == 'T':
            chance *= at
        else:
            chance *= gc
            
    return chance

file = open('dataset.txt', 'r')
data = file.read().split('\n')
file.close()

data[0] = data[0].split(' ')
N = int(data[0][0])
x = float(data[0][1])
s = data[1]

sChance = getStrChance(s, x)
# Calculate the probability that every string does NOT equal S
# then subtract that from 1.0
result = round(1-((1-sChance)**N),3)
print result

outfile = open('result.txt', 'w')
outfile.write(str(result))
outfile.close()