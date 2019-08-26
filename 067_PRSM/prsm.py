import operator

def get_masses():
    global masses
    masses = {}
    with open('masses.txt', 'r') as fp:
        data = fp.read().split('\n')
    for line in data:
        amino_acid, mass = line.split('   ')
        mass = float(mass)
        masses[amino_acid] = mass
    print(masses)
    
def get_spectrum(p):
    global masses
    spectrum = [0]
    for ch in p:
        spectrum.append( spectrum[-1] + masses[ch] )
    print(f'Spectrum of {p} = {spectrum}')
    return spectrum
    
def spectrum_difference(a, b):
    diff = {}
    for x in a:
        for y in b:
            d = format(x-y, ".5f")
            diff[d] = 1 + (diff[d] if d in diff else 0)
    return diff
    
def get_multiplicity(x):
    multiplicity = 0
    for i in range(len(x)-1):
        if abs(x[i+1] - x[i]) < 0.01: multiplicity += 1
    return multiplicity

if __name__=='__main__':
    get_masses()

    with open('dataset.txt', 'r') as fp:
        data = fp.read().split('\n')
        
    num_proteins = int(data[0])
    proteins = data[1:num_proteins+1]
    print(proteins)
    print()
    
    spectrum = [float(x) for x in data[num_proteins+1:]]
    print(spectrum)
    
    max_multiplicities = []
    for p in proteins:
        p_spectrum = get_spectrum(p)
        spec_diff = spectrum_difference(spectrum, p_spectrum)
        
        print(spec_diff)
        
        multiplicity = max(spec_diff.items(), key=operator.itemgetter(1))[1]
        max_multiplicities.append((p, multiplicity))
        
    print(max_multiplicities)
    max_protein, max_multiplicity = max(max_multiplicities, key=operator.itemgetter(1))
    
    result = f'{max_multiplicity}\n{max_protein}'
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)