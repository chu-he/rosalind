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
	return best_match

if __name__=='__main__':
	fp = open('masses.txt', 'r')
	masses = parse_masses(fp.read().split('\n'))
	fp.close()
	
	fp2 = open('dataset.txt', 'r')
	prefix_spectrum = fp2.read().split('\n')
	fp2.close()
	
	protein_string = ""
	
	prev_mass = prefix_spectrum[0]
	for index in range(1,len(prefix_spectrum)):
		mass = prefix_spectrum[index]
		mass_diff = float(mass) - float(prev_mass)
		amino_acid = find_best_match(mass_diff, masses)
		
		protein_string += amino_acid
		prev_mass = mass
		
	print(protein_string)
	
	fp3 = open('result.txt', 'w')
	fp3.write(protein_string)
	fp3.close()