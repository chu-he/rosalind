from gasm import *

assert( reverse_complement('ATATCGCG') == 'CGCGATAT' )

assert( align('CGATT', 'ATTGG') == (3, 'CGATTGG') )

assert( try_alignment('CGATT', 'ATTGG') == (3, 'CGATTGG', 'CGATT', 'ATTGG') )

l = ['CGATT', 'ATTGG']
assert( consolidate(l) == 'CGATTGG' )

l = ['CGATT', 'ATTGG', 'TGGAC']
assert( consolidate(l) == 'CGATTGGAC' )

assert( find_loop('TAATCTGTAA') == 'TCTGTAA' )