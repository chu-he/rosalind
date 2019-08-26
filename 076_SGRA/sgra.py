def parse_masses(masses_raw):
    masses_parsed = []
    for line in masses_raw:
        amino_acid, mass = line.split('   ')
        masses_parsed.append((amino_acid, mass))
    return masses_parsed
        
def find_best_match(mass, masses):
    best_diff = 9999
    best_match = None
    for pair in masses:
        amino_acid, amino_acid_mass = pair
        diff = abs(float(mass) - float(amino_acid_mass))
        if diff < best_diff:
            best_diff = diff
            best_match = amino_acid
            
    if best_diff < 0.01:
        return best_match
    else:
        return None
        
def build_protein_string(prefix_spectrum):
    first_index = None
    protein_string = ''
    
    prev_mass = prefix_spectrum[0]
    for index in range(1,len(prefix_spectrum)):
        mass = prefix_spectrum[index]
        mass_diff = float(mass) - float(prev_mass)
        amino_acid = find_best_match(mass_diff, masses)
        print(f'{mass} - {prev_mass} = {mass_diff} --> {amino_acid}')
        
        if amino_acid:
            protein_string += amino_acid
            prev_mass = mass
            
            if first_index is None:
                first_index = index
                
        if mass_diff > 200:
            return protein_string
                
    return protein_string

if __name__=='__main__':
    fp = open('masses.txt', 'r')
    masses = parse_masses(fp.read().split('\n'))
    fp.close()
    
    fp2 = open('dataset.txt', 'r')
    prefix_spectrum = fp2.read().split('\n')
    fp2.close()
    
    prefix_spectrum = [float(x) for x in prefix_spectrum]
    prefix_spectrum.sort()
    
    protein_strings = []
    
    for i in range(len(prefix_spectrum)):
        p_str = build_protein_string(prefix_spectrum[i:])
        if p_str:
            protein_strings.append(p_str)
        
    print('\n'.join(protein_strings))
    
    result = max(protein_strings, key=len)
    print(result)
    
    fp3 = open('result.txt', 'w')
    fp3.write(result)
    fp3.close()