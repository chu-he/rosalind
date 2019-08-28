import laff3
import unittest

class MatrixTestCase(unittest.TestCase):
    def test_spot_check_matrix(self):
        scoring_matrix = laff3.read_scoring_matrix('BLOSUM62.txt')
        self.assertEqual( scoring_matrix['AA'], 4 )
        self.assertEqual( scoring_matrix['WC'], -2 )
        self.assertEqual( scoring_matrix['CW'], -2 )
        self.assertEqual( scoring_matrix['WW'], 11 )
        
    def test_align(self):
        scoring_matrix = laff3.read_scoring_matrix('BLOSUM62.txt')
        best_score, local_a, local_b = laff3.local_align('PLEASANTLY', 'MEANLY', scoring_matrix)
        self.assertEqual(best_score, 12)
        self.assertEqual(local_a, 'LEAS')
        self.assertEqual(local_b, 'MEAN')
        
if __name__=='__main__':
    unittest.main()