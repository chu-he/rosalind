import operator

def get_masses():
    global masses
    masses = []
    with open('masses.txt', 'r') as fp:
        data = fp.read().split('\n')
    for line in data:
        amino_acid, mass = line.split('   ')
        mass = float(mass)
        masses.append( (amino_acid, mass) )
    print(masses)
    
def build_protein(spectrum):
    global masses
    
    protein = ''
    last_mass = spectrum[0]
    for i in range(1, len(spectrum)):
        mass = spectrum[i] - last_mass
        amino_acid, mass_diff = min([(mass_pair[0], abs(mass_pair[1]-mass)) for mass_pair in masses], key=operator.itemgetter(1))
        if mass_diff < 0.2:
            last_mass = spectrum[i]
            protein += amino_acid
            
    return protein
    
def multiplicity(a, b):
    print(f'Checking multiplicity {a} x {b}')
    b = sorted(list(b))
    multiplicity = 0
    for ch in a:
        if ch in b:
            print(f'  Remove {ch} from {b}')
            b.remove(ch)
            multiplicity += 1
    print(f'  Multiplicity = {multiplicity}')
    return multiplicity

if __name__=='__main__':
    get_masses()

    with open('dataset.txt', 'r') as fp:
        data = fp.read().split('\n')
        
    num_proteins = int(data[0])
    proteins = data[1:num_proteins+1]
    print(proteins)
    print()
    
    spectrum = sorted([float(x) for x in data[num_proteins+1:]])
    print(spectrum)
    
    new_protein = build_protein(spectrum)
    print(new_protein)
    
    best_match = max([(p, multiplicity(p, new_protein)) for p in proteins], key=operator.itemgetter(1))
    print(best_match)
    
    result = f'{best_match[1]}\n{best_match[0]}'
    print(result)
    
    with open('result.txt', 'w') as fp2:
        fp2.write(result)