

# in  - The GC content of the string
# out - The probability that two randomly chosen nucleotides will be the same
#
# G/C and A/T are assumed to have the same frequency, so we can calculate
# only for C and A and double the result
def CalculateProbTwoSame(gc):

    # For this given GC frequency:
    #  C has the frequency gc/2
    #  A has the frequency 0.5 - freq(C)
    c_freq = gc/2
    a_freq = 0.5 - c_freq
    
    # Square the frequencies to determine the odds of:
    #  * Picking the nucleotide as a first pick
    #  * Picking it again as a second pick
    result = (c_freq*c_freq + a_freq*a_freq)*2
    
    return result

# Start program execution -------------------------------------
# Read the dataset
file = open('dataset.txt', 'r')
data = file.read()
file.close()

data = data.split()
results = []
for gc in data:
    results.append(str(CalculateProbTwoSame(float(gc))))
    
result = ' '.join(results)
print result

# Write result to file
file = open('result.txt', 'w')
file.write(result)
file.close()