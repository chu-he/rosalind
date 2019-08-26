from suff import *

if __name__=='__main__':
    assert( get_longest_common_prefix('test', 'tim') == 't' )
    assert( get_longest_common_prefix('alpha', 'beta') == '' )
    assert( get_longest_common_prefix('fly', 'flying') == 'fly' )