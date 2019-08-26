import sys

def getSignedPermutations(set):
    if len(set) == 1:
        return [[set[0]], [-set[0]]]
        
    result = []
    for k in set:
        innerSet = set[:]
        innerSet.remove(k)
        innerResult = getSignedPermutations(innerSet)
        
        for r in innerResult:
            posList = r[:]
            posList.insert(0, k)
            negList = r[:]
            negList.insert(0, -k)
        
            result.append(posList)
            result.append(negList)
    return result

n = int(sys.argv[1])

set = range(1, n+1)
result = getSignedPermutations(set)
    
outstr = ''
outstr += str(len(result)) + '\n'
for r in result:
    outstr += ' '.join([str(x) for x in r]) + '\n'
    
outfile = open('032_SIGN.result', 'w')
outfile.write(outstr)
outfile.close()