from laff6 import *
import unittest
from Bio.SubsMat.MatrixInfo import blosum62

class MatrixTestCase(unittest.TestCase):
    def test_spot_check_matrix(self):
        print('test_spot_check_matrix')
        self.assertEqual( get_blosum62_value('A', 'A'), 4 )
        self.assertEqual( get_blosum62_value('W', 'C'), -2 )
        self.assertEqual( get_blosum62_value('C', 'W'), -2 )
        self.assertEqual( get_blosum62_value('W', 'W'), 11 )
        
    def test_align(self):
        print('test_align')
        best_score, local_a, local_b = local_align('PLEASANTLY', 'MEANLY')
        self.assertEqual(best_score, 12)
        self.assertEqual(local_a, 'LEAS')
        self.assertEqual(local_b, 'MEAN')
        
    def test_align_2(self):
        print('test_align_2')
        a = 'LLLLLWWWWWCCCCCCCCWWWWWWWWWWLLLLL'
        b = 'DDDDDWWWWWWWWWWQQQQQQQQWWWWWDDDDD'
        best_score, local_a, local_b = local_align(a, b)
        self.assertEqual(best_score, (11*5*3)-(18*2))
        self.assertEqual(local_a, 'WWWWWCCCCCCCCWWWWWWWWWW')
        self.assertEqual(local_b, 'WWWWWWWWWWQQQQQQQQWWWWW')
        
if __name__=='__main__':
    unittest.main()