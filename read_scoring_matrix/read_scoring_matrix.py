def read_scoring_matrix(filename):
    matrix = {}
    with open(filename) as fp:
        data = fp.read().split('\n')
        
    header = data[0].split()
    
    for line in data[1:]:
        line_split = line.split()
        x = line_split[0]
        line_split = line_split[1:]
        for i in range(len(line_split)):
            y = header[i]
            v = int(line_split[i])
            matrix[f'{x}{y}'] = v
            
    return matrix