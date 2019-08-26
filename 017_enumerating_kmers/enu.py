def GetAllStrings(alphabet, length, prefix):
    if length == 1:
        retList = [prefix+alphabet[i] for i in range(len(alphabet))]
        return retList
        
    else:
        retList = []
        for a in alphabet:
            retList.extend(GetAllStrings(alphabet, length-1, prefix+a))
        return retList

# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split('\n')
alphabet = data[0].split()
length = int(data[1])

strings = GetAllStrings(alphabet, length, '')

result = '\n'.join(strings)
print result
    
# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()