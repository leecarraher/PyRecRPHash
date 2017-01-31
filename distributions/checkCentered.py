from numpy import *
from numpy.random import *
from scipy import stats, integrate
import matplotlib.pyplot as plt
import seaborn as sns

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

def dbfriendlyproj(v,M,P,l):
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
def proj(x,P):
    '''
        x - high dimensional vector
        P - len(x) * n matrix of GNV elements
        this is a naive and slow random projection,
        but it's compact and to the point.
    '''
    return x.dot(P)*(1/float(len(P)))**.5

def makeData(d,n,k):
    '''
        d - dimensionality
        n - number of vectors to generate
        k - number of clusters to partition vectors in
    '''
    #generate some density modes
    cents = rand(k,d)*2-1

    X = []
    for i in xrange(n):
        centid = int(randint(k))
        x = array(cents[centid]+randn(d)*1)
        X.append(x)

    return cents,X


from pyIOUtils import *
#cents,X = makeData(1000,100000,10)

X = []
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/HAR_clu6.txt")))
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/cora1_clu7.txt")))
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/webkb_clu5.txt")))

X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/cnae9_clu9.txt")))
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/citeseer1_clu6.txt")))
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/giset1_clu2.txt")))

X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/iad1_clu2.txt")))
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/inloc_clu3.txt")))
X.append( array(readMatFile("/home/lee/workspace/RPHash/datasets/iad1_clu3.txt")))

l=64
#create projector matrixs
#uncomment for db friendly
#M,P = genDBFriendly(len(X[0]),l)
P = randn(len(X[0]),l)


Xhat = []
for x in X:
    Xhat.append(proj(x,P))
    #uncomment for db friendly
    #Xhat.append(dbfriendlyproj(x,M,P,l))
Xhat = array(Xhat)


import matplotlib
for i in range(16):
    plt.subplot(4,4,i+1)

    avg = average(Xhat[:,i])
    std = var(Xhat[:,i])**.5
    plotobject = sns.distplot(Xhat[:,i],hist=True,norm_hist=True)

    #some matplotlib magic to turn all bars left and right of upper and lower
    #quartiles red
    children = plotobject.get_children()
    barlist=filter(lambda x: isinstance(x, matplotlib.patches.Rectangle), children)
    for bar in barlist[:-1]:
        if bar.get_x() < avg-std: bar.set_color('r')
        if bar.get_x() > avg+std: bar.set_color('r')

plt.show()











