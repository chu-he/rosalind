from grep import *


if __name__=='__main__':
    a = 'string'
    b = 'ringbearer'
    c = find_overlap(a, b)
    print(f'Overlap {a} & {b} = {c}')
    assert( find_overlap(a, b) == 'ring' )
    
    a = ['string']
    b = 'rings'
    c = add_kmer(a, b)
    assert( a == ['string', 'strings'] )