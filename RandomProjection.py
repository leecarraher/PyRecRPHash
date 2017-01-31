from numpy.random import *
from numpy import *

def genDBFriendly(n,t):
    '''
        this is a modified version of achlioptas's db friendly projection
        scheme. It should have better cache utilizations, and avoids storing
        sparse matrices, floating point values, and is overall more computationally
        efficient.
    '''
    M = [ [] for i in xrange(t)]
    P = [ [] for i in xrange(t)]
    r = 0
    for i in xrange(t):
        #approx size
        orderedM = [] # plus columns
        orderedP = [] # minus columns
        for j in xrange(n):
            r = randint(6)
            if r == 0:
                orderedM.append(j)
            if r == 1:
                orderedP.append(j)

        orderedM.sort()#for better cache utilization
        M[i] = [0]*len(orderedM)
        j = 0
        for v in orderedM:
            M[i][j] = v
            j+=1
        orderedP.sort()
        P[i] = [0]*len(orderedP);
        j = 0
        for v in orderedP:
            P[i][j] = v
            j+=1
    return M,P

def proj2(v,M,P,l):
    '''
        project a vector based on a M(inuses) and P(luses)
        set of column ids, generated from Achlioptas modified
    '''
    r = [0]*l
    sums = 0.0
    scale = (3.0/l)**.5
    for i in xrange(l):
        sums = 0.0
        for col in M[i]:
            sums -= v[col]
        for col in P[i]:
            sums += v[col]
        r[i] = sums * scale
    return r


# faster since numpy uses c here, but db friendly will
# certainly beat this when optimized
def proj(x,M,P,l):
    '''
        x - high dimensional vector
        P - len(x) * n matrix of GNV elements
        this is a naive and slow random projection,
        but it's compact and to the point.
    '''
    return x.dot(P)*(1/float(len(P)))**.5

