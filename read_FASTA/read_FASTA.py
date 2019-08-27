def read_fasta(filename):
    with open(filename, 'r') as fp:
        data = fp.read()
        
    data = data.split('\n')
    strings = {}
    strName = ''
    str = ''
    
    for line in data:
        if line[0] == '>':
            if strName != '':
                strings[strName] = str
            strName = line[1:]
            str = ''
        else:
            str += line
            
    if strName != '':
        strings[strName] = str
            
    return strings