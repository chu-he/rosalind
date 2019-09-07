from mgap import *
import unittest

class MatrixTestCase(unittest.TestCase):
        
    def test_num_gaps(self):
        gaps = get_max_gaps('AACGTA', 'ACACCTA')
        self.assertEqual(gaps, 3)
        
if __name__=='__main__':
    unittest.main()