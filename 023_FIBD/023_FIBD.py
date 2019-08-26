import sys

(n, m) = [int(x) for x in sys.argv[1:3]]

age = [0 for x in range(m)]
dead = 0
age[0] = 1

ageIndexes = range(m)
ageIndexes.remove(0)
ageIndexes.reverse()
print ageIndexes

print 'Month 0 :', sum(age), 'rabbits'
for month in [x+1 for x in range(n-1)]:
    dead += age[-1]
    
    babies = 0
    for i in ageIndexes:
        babies += age[i]
        age[i] = age[i-1]
        
    age[0] = babies
    
    print 'Month', month, ':', sum(age), 'rabbits'
    
print sum(age)