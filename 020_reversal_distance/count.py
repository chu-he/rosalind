def Flip(list, left, right):
    leftSide = list[:left]
    rightSide = list[right+1:]
    middle = list[left:right+1]
    middle.reverse()
    
    leftSide.extend(middle)
    leftSide.extend(rightSide)
    return leftSide

def ReversalDistance(fromList, toList):
    reversals = 0
    for index in range(len(toList)):
        if fromList[index] != toList[index]:
            target = fromList.index(toList[index])
            fromList = Flip(fromList, index, target)
            reversals += 1
            
    return reversals

# Start program execution -------------------------------------
# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')

results = []
index = 0
while index < len(data):
    results.append(str(ReversalDistance(data[index].split(), data[index+1].split())))
    index += 3
    
result = ' '.join(results)
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()