from numpy.random import *
from numpy import *

def makeData(d,n,k,noise = 0,errorperc=0,variance=.1,sparseness = 0):
    '''
        d - dimensionality
        n - number of vectors to generate
        k - number of clusters to partition vectors in
        this method generates data from a heteroscedastic gaussian distribution
        and partitions it into k clusters. It then adds noise 1/4 from a uniform
        distribution -1.5 - +1.5.
    '''
    if noise>0: noise = int(noise*n)
    if errorperc>0: errorperc = int(errorperc*d)
    if sparseness>0: sparseness = int(sparseness*d)

    #generate some density modes
    cents = ((-1)**randint(2)*variance)*(rand(k,d)*2-1)
    for i in xrange(k):
        #add some random error bits
        for j in xrange(sparseness):
            cents[i][randint(d)]=0.0

    X = []
    for i in xrange(n):
        centid = int(randint(k))
        cent = cents[centid]
        x = array(cent+randn(d)*rand()*variance)
        for j in xrange(d):
            if cent[j]==0.0:x[j]=0.0

        X.append(x)
        #add some random error bits
        for j in xrange(errorperc):
            X[-1][randint(d)]=0.0

    #add some uniform noise
    X.extend( rand(noise,d)*3-1.5 )
    shuffle(X)
    return cents,X
