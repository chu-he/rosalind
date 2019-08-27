import loca
import unittest

class MatrixTestCase(unittest.TestCase):
    def test_spot_check_matrix(self):
        scoring_matrix = loca.read_scoring_matrix('pam250.txt')
        self.assertEqual( scoring_matrix['AA'], 2 )
        self.assertEqual( scoring_matrix['WC'], -8 )
        self.assertEqual( scoring_matrix['CW'], -8 )
        self.assertEqual( scoring_matrix['WW'], 17 )
        
if __name__=='__main__':
    unittest.main()