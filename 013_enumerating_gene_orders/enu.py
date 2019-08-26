def GetAllCombinations(values, prefix = ''):
    if values == []:
        return [prefix]
        
    combinations = []
    
    for v in values:
        newList = list(values)
        newList.remove(v)
        
        if prefix == '':
            newPrefix = str(v)
        else:
            newPrefix = prefix + ' ' + str(v)
        combinations.extend(GetAllCombinations(newList, newPrefix))
        
    return combinations

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = int(data)

factorial = 1
for i in range(1, data+1):
    factorial *= i
    
result = str(factorial) + '\n'

values = [x for x in range(1, data+1)]

combinations = GetAllCombinations(values)

result += '\n'.join(combinations)

print result
    
# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()