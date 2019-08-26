from decimal import Decimal

def parse_sets(data):
	s1 = [Decimal(x) for x in data[0].split(' ')]
	s2 = [Decimal(x) for x in data[1].split(' ')]
	return (s1, s2)

if __name__=='__main__':
	fp = open('dataset.txt', 'r')
	s1, s2 = parse_sets(fp.read().split('\n'))
	fp.close()
	
	max_occurrences_value = 0
	max_occurrences_item  = None
	
	difference_map = {}
	for s1_item in s1:
		for s2_item in s2:
			difference = s1_item - s2_item
			difference_map[difference] = difference_map.get(difference, 0) + 1
			if difference_map[difference] > max_occurrences_value:
				max_occurrences_value = difference_map[difference]
				max_occurrences_item = difference
	
	#print(difference_map)
	print(max_occurrences_value)
	print(max_occurrences_item)
	
	fp2 = open('result.txt', 'w')
	fp2.write(str(max_occurrences_value) + '\n' + str(max_occurrences_item))
	fp2.close()