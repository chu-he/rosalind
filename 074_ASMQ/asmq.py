if __name__=='__main__':
    with open('dataset.txt', 'r') as fp:
        lines = fp.read().split('\n')
        
    lengths = []
    total = 0
    max_length = 0
    for n in lines:
        l = len(n)
        lengths.append(l)
        total += l
        if l > max_length: max_length = l
        
    n75 = None
    n50 = None
    L = max_length
    while n75 is None:
        subset = [x for x in lengths if x >= L]
        L_sum = sum(subset)
        percentage = float(L_sum) / float(total)
        print(f'{L} - {percentage} - {subset}')
        
        if percentage >= 0.75 and n75 is None:
            n75 = L
            
        if percentage >= 0.50 and n50 is None:
            n50 = L
            
        L -= 1
        
    print(f'N75 = {n75}')
    print(f'N50 = {n50}')
    
    with open('result.txt', 'w') as fp2:
        fp2.write(f'{n50} {n75}')