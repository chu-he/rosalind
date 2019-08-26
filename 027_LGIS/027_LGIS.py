def findSmallestGreaterThan(X, S, x):
    # Return the index of the smallest element k in S
    # such that k >= x
    # Given: S is sorted
    low = 0
    high = len(S)
    
    while low != high:
        mid = (low+high)/2
        check = X[S[mid]]
        
        if check == x:
            return mid
        if check > x:
            high = mid
        if check < x:
            low = mid+1
        
    mid = (low+high)/2
    if X[S[mid]] >= x:
        return mid
    else:
        return -1
        
def findLargestSmallerThan(X, S, x):
    # Return the index of the largest element k in S
    # such that k <= x
    # Given: S is sorted
    low = -1
    high = len(S)-1
    
    while low != high:
        mid = (low+high+1)/2
        check = X[S[mid]]
        
        if check == x:
            return mid
        if check > x:
            high = mid-1
        if check < x:
            low = mid
        
    mid = (low+high)/2
    if X[S[mid]] <= x:
        return mid
    else:
        return -1

def getLongestIncreasing(X):
    S = []
    p = {}
    
    for i_x in range(len(X)):
        
        x = X[i_x]
        print ''
        print i_x, '------------------'
        print ' x =', x
        if len(S) > 0:
            if x > X[S[-1]]:
                print ' (1)', x, '>', X[S[-1]]
                p[i_x] = S[len(S)-1]
                S.append(i_x)
            else:
                i_k = findSmallestGreaterThan(X, S, x)
                print ' (2)', x, i_k, X[S[i_k]]
                if i_k != -1:
                    if i_k != 0:
                        p[i_x] = S[i_k-1]
                    S[i_k] = i_x
        else:
            print ' (3)', x
            S = [i_x]
            
        print '  X =', X
        print '  S =', S
        print '  p =', p
            
    print ''
    print 'X =', X
    print 'S =', S
    print [X[k] for k in S]
    print p
    get = S[-1]
    
    ret = []
    while True:
        ret.append(X[get])
        if get in p:
            get = p[get]
        else:
            break
    
    ret.reverse()
    return ret

def getLongestDecreasing(X):
    S = []
    p = {}
    
    for i_x in range(len(X)):
        
        x = X[i_x]
        print ''
        print i_x, '------------------'
        print ' x =', x
        if len(S) > 0:
            if x < X[S[-1]]:
                print ' (1)', x, '<', X[S[-1]]
                p[i_x] = S[len(S)-1]
                S.append(i_x)
            else:
                i_k = findLargestSmallerThan(X, S, x)
                print ' (2)', x, i_k, X[S[i_k]]
                if i_k != -1:
                    if i_k != 0:
                        p[i_x] = S[i_k-1]
                    S[i_k] = i_x
        else:
            print ' (3)', x
            S = [i_x]
            
        print '  X =', X
        print '  S =', S
        print '  p =', p
            
    print ''
    print 'X =', X
    print 'S =', S
    print [X[k] for k in S]
    print p
    get = S[-1]
    
    ret = []
    while True:
        ret.append(X[get])
        if get in p:
            get = p[get]
        else:
            break
    
    ret.reverse()
    return ret


file = open('dataset.txt', 'r')
data = file.read().split()
file.close()

num = int(data[0])
data = [int(x) for x in data[1:]]
data = [int(x) for x in '10 2 1 6 3 4 9 5 8'.split()]
#print data

print getLongestIncreasing(data)
print getLongestDecreasing(data)



'''
X = [1, 5, 8, 23, 66, 192, 395, 682, 1039, 4928]
S = range(len(X))
print X[findSmallestGreaterThan(X, S, 23)]
print X[findSmallestGreaterThan(X, S, 50)]
print X[findSmallestGreaterThan(X, S, 100)]
print X[findSmallestGreaterThan(X, S, 200)]
print X[findSmallestGreaterThan(X, S, 400)]
print ''
print X[findLargestSmallerThan(X, S, 23)]
print X[findLargestSmallerThan(X, S, 50)]
print X[findLargestSmallerThan(X, S, 100)]
print X[findLargestSmallerThan(X, S, 200)]
print X[findLargestSmallerThan(X, S, 400)]
'''