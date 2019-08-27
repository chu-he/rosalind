import laff
import unittest

class MatrixTestCase(unittest.TestCase):
    def test_spot_check_matrix(self):
        scoring_matrix = laff.read_scoring_matrix('BLOSUM62.txt')
        self.assertEqual( scoring_matrix['AA'], 4 )
        self.assertEqual( scoring_matrix['WC'], -2 )
        self.assertEqual( scoring_matrix['CW'], -2 )
        self.assertEqual( scoring_matrix['WW'], 11 )
        
if __name__=='__main__':
    unittest.main()