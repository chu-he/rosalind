from motz import *

class Tests():
    def test_n_1():
        for n in ['A', 'U', 'C', 'G']:
            assert(find_noncrossing_matchings(n) == 1)
            
    def test_n_2():
        for n in ['AA', 'AC', 'AG', 'UU', 'UC', 'UG', 'CC', 'CA', 'CU', 'GG', 'GA', 'GU']:
            assert(find_noncrossing_matchings(n) == 1)
        for n in ['AU', 'UA', 'CG', 'GC']:
            assert(find_noncrossing_matchings(n) == 2)
            
    def test_n_4():
        assert(find_noncrossing_matchings('AUAU') == 7)
        
def runTests():
    methods = [f for f in dir(Tests) if callable(getattr(Tests, f)) and f[0:2] != '__']
    for m in methods:
        getattr(Tests, m)()

if __name__=='__main__':
    runTests()