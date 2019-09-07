from smgb import *
import unittest

class MatrixTestCase(unittest.TestCase):
        
    def test_align(self):
        print('test_align')
        best_score, local_a, local_b = semiglobal_align('CAGCACTTGGATTCTCGG', 'CAGCGTGG')
        self.assertEqual(best_score, 4)
        
if __name__=='__main__':
    unittest.main()