from REAR import *

def RunTests():
    p1 = ['A', 'B', 'C']
    p2 = ['C', 'A', 'B']
    ap1, ap2 = align_pair((p1, p2))
    assert ap1 == [0, 1, 2]
    assert ap2 == [2, 0, 1]
    
    bps = find_breakpoints([0, 5, 4, 1])
    assert bps == [0.5, 2.5, 3.5]
    
    assert has_decreasing_strip([0, 1, 2, 3, 9, 8, 7, 0, 1, 2]) == True
    assert has_decreasing_strip([0, 1, 2, 3, 4, 5, 6]) == False
    assert has_decreasing_strip([0, 1, 2, 3, 9, 0, 1, 2, 3]) == True
    
    assert has_increasing_strip([0, 1, 2, 3, 4, 5, 6, 7]) == True
    assert has_increasing_strip([7, 6, 5, 4, 3, 2, 1, 0]) == False
    assert has_increasing_strip([7, 6, 5, 0, 1, 4, 3, 2]) == True
    
    assert swap([1, 2, 3, 4], 1, 2) == [1, 3, 2, 4]
    assert swap([0, 1, 2, 3, 4, 5, 6, 7], 1, 6) == [0, 6, 5, 4, 3, 2, 1, 7]
    
    assert do_best_swap([0, 3, 2, 1, 4, 99, 9, 6, 7, 8, 20, 99, 5, 8, 7, 6, 20]) == \
                        [0, 1, 2, 3, 4, 99, 9, 6, 7, 8, 20, 99, 5, 8, 7, 6, 20]

    assert do_best_swap([9, 6, 7, 8, 20, 99, 15, 18, 17, 16, 20]) == \
                        [9, 8, 7, 6, 20, 99, 15, 18, 17, 16, 20]
                        
    assert do_best_swap([5, 8, 7, 6, 20]) == \
                        [5, 6, 7, 8, 20]
                        
    assert swap_any_increasing_strip([9, 8, 7, 1, 2, 3, 6, 5, 4]) == \
                                     [9, 8, 7, 3, 2, 1, 6, 5, 4]
                                     
    assert has_decreasing_strip([0, 3, 4, 5, 6, 7, 1, 2, 8, 9]) == False
                        
if __name__=="__main__":
    RunTests()
    print("All tests passed")