from rnas import *

class Tests():
    def test_n_tiny():
        return
        for n in ['A', 'AU', 'AUU', 'AUUU']:
            assert(find_noncrossing_matchings(n) == 1)
            
    def test_n_medium():
        #assert(find_noncrossing_matchings('AUUUU') == 2)
        #assert(find_noncrossing_matchings('ACGGU') == 2)
        #assert(find_noncrossing_matchings('AAUCU') == 2)
        #assert(find_noncrossing_matchings('AGCUU') == 2)
        #assert(find_noncrossing_matchings('GUUUU') == 2)
        
        #assert(find_noncrossing_matchings('AUUUUG') == 3)
        
        assert(find_noncrossing_matchings('CAUUUUG') == 5)
            
    def test_n_big():
        assert(find_noncrossing_matchings('AUGCUAGUACGGAGCGAGUCUAGCGAGCGAUGUCGUGAGUACUAUAUAUGCGCAUAAGCCACGU') == 284850219977421)
        pass
        
def runTests():
    methods = [f for f in dir(Tests) if callable(getattr(Tests, f)) and f[0:2] != '__']
    for m in methods:
        getattr(Tests, m)()

if __name__=='__main__':
    runTests()