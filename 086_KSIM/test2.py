from ksim2 import *
import unittest

class TestCases(unittest.TestCase):
        
    def test_small(self):
        substrings = motifs('AB', 'ABA', 0)
        self.assertIn((1, 2), substrings)
        
    def test_small2(self):
        substrings = motifs('ACB', 'AB', 1)
        self.assertIn((1, 2), substrings)
        
    def test_small3(self):
        substrings = motifs('CAB', 'AB', 1)
        self.assertIn((1, 2), substrings)
        
    def test_rosalind(self):
        substrings = motifs('ACGTAG', 'ACGGATCGGCATCGT', 2)
        expected = ((1, 4), (1, 5), (1, 6))
        for e in expected:
            self.assertIn(e, substrings)
        
    def test_extra1(self):
        substrings = motifs('ACGTAG', 'AGTAG', 1)
        self.assertIn((1, 5), substrings)
        
    def test_extra(self):
        substrings = motifs('ACGTAG', 'GGACGATAGGTAAAGTAGTAGCGACGTAGG', 1)
        expected = ((3, 7), (13, 6), (14, 5), (17, 5), (24, 5), (24, 6), (24, 7), (23, 7), (25, 5))
        for e in expected:
            self.assertIn(e, substrings)
        
if __name__=='__main__':
    unittest.main()