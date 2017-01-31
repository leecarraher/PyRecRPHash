from numpy import *
from numpy.random import *
#3.7x slower
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

def update_cent(centroid,x,n):
    centroid = [(x[i]+centroid[i]*n)/(n+1) for i in xrange(len(x))]
    return centroid

def proj(v,P,M,l):
    '''
        project a vector based on a M(inuses) and P(luses)
        set of column ids, generated from Achlioptas modified
    '''
    r = [0]*l
    sums = 0.0
    scale = 1#(3.0/l)**.5 #affinity matters, so who cares about scale
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
#def proj(x,M,P):
#    '''
#        x - high dimensional vector
#        P - len(x) * n matrix of GNV elements
#        this is a naive and slow random projection,
#        but it's compact and to the point.
#    '''
#    return x.dot(P)*(1/float(len(P)))**.5

def hashvec(x):
    '''
        super simple hash algorithm, reminiscient of pstable lsh
    '''
    s = 0
    for i in xrange(len(x)):
        s=s<<1
        if x[i]>0: s+=1
    return s

def addtocounter(x,M,P,IDAndCount,IDAndCent,l):
    '''
        x          - input vector
        IDAndCount - ID->count map
        IDAndCent  - ID->centroid vector map

        hash the projected vector x and update
        the hash to centroid and counts maps
    '''
    xt = proj(x,M,P,l)
    s = hashvec(xt)
    for i in xrange(0,l):
        partialhash = s>>i
        if IDAndCount.has_key(partialhash):
            update_cent(IDAndCent[partialhash],x,IDAndCount[partialhash])
            IDAndCount[partialhash] = IDAndCount[partialhash]+1
        else:
            IDAndCount[partialhash] = 1
            IDAndCent[partialhash] = x

def findDensityModes(X,k,l):
    '''
        X - data set
        k - canonical k in k-means
        l - clustering sub-space
        Compute density mode via iterative deepening hash counting
    '''
    d = len(X[0])

    #our counter, replace with mincount hash
    IDAndCount = {}
    IDAndCent = {}

    #create projector matrixs
    M,P = genDBFriendly(d,l)
    #P = randn(d,l)

    #process data by adding to the counter
    for x in X:
        addtocounter(x,M,P,IDAndCount,IDAndCent,l)

    #we are adding everything and sorting here, real implementation would
    #use a priority queue, heap, skiplist, redblack, and may be bounded
    densityAndID = []
    for h in sort(IDAndCount.keys()):
        if h>1  and 2*IDAndCount[h] > IDAndCount[h>>1]:
            densityAndID.append( (IDAndCount[h],h))
            #remove old
            if h>2 and densityAndID.__contains__((IDAndCount[h>>1],h>>1 )):
                densityAndID.remove((IDAndCount[h>>1],h>>1))

    # sort
    densityAndID.sort(reverse=True)

    # compute medoids
    estcents = []
    for d in densityAndID[0:int(k)]:
        idcent = d[1]
        estcents.append(IDAndCent[idcent])
    return estcents

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
    cents = rand(k,d)*2-1
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


def run(d,n,k,noise = 0, is3d = False,errorperc=0,variance=.1,sparseness = 0):
    '''
        d - dimensionality
        n - number of vectors to generate
        k - number of clusters to partition vectors in
        this method generates data from a heteroscedastic gaussian distribution
        and partitions it into k clusters. It then adds noise 1/4 from a uniform
        distribution -1.5 - +1.5. Then plots the results of iterative deepening
        hash count clustering and plots the data in a 3x3 subplot.
    '''

    cents, X = makeData(d,n,k,noise,errorperc,variance,sparseness)
    estcents = findDensityModes(X,k,l)
    #from scipy.cluster.vq import kmeans
    #kmcents,_ = kmeans(array(X),k)

    #randomly pick the axis to plot
    xcol , ycol , zcol = randint(d),randint(d),randint(d)
    while xcol == ycol: ycol = randint(d)

    while zcol == ycol or zcol == xcol: zcol = randint(d)

    if is3d:
        ax = fig.add_subplot(330+(k-1), projection='3d')
        ax.scatter([x[xcol] for x in X[::6]],[x[ycol] for x in X[::6]],[x[zcol] for x in X[::6]],',',s=1)
        ax.scatter([x[xcol] for x in estcents],[x[ycol] for x in estcents],[x[zcol] for x in estcents],'o',color='gold',marker='o',s=20)
        ax.scatter([x[xcol] for x in cents],[x[ycol] for x in cents],[x[zcol] for x in cents],color='red',marker='*',s=20)

    else:
        subplot(330+(k-1))
        plot([x[xcol] for x in X[::1]],[x[ycol] for x in X[::1]],',')
        plot([x[xcol] for x in estcents],[x[ycol] for x in estcents],'o',color='gold',markersize=8)
        plot([x[xcol] for x in cents],[x[ycol] for x in cents],'*',color='red',markersize=7)
        #plot([x[xcol] for x in kmcents],[x[ycol] for x in kmcents],'v',color='green',markersize=7)


def readcsv(filename):
    X = []
    line = filename.readline()[:-1]# no newline char
    while not line == "":
        vec = []
        cols = line.split(',')[:-1]#no cluster id
        for col in cols:
            vec.append(float(col))
        X.append(vec)
        line = filename.readline();
    return X


def writecents(estcents,outfile):
    outfile.write(str(len(estcents))+'\n')
    outfile.write(str(len(estcents[0]))+'\n')
    for vec in estcents:
        for val in vec:
            outfile.write(str(val)+'\n')


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1 :
        from pylab import *
        from mpl_toolkits.mplot3d import Axes3D
        import matplotlib.pyplot as plt
        '''
            Run some tests with different numbers of clusters
                b = file("somedata",'w+')
                b.write(str(len(X))+'\n')
                b.write(str(len(X[0]))+'\n')
                for x in X:
                    for xx in x:
                b.write(str(xx)+'\n')
        '''
        l = 24
        k = 10
        d = 500

        #from timeit import default_timer as timer
        #for r in range(8,20):
        #    n = int(10**(1+r/4.))
        #    cents, X = makeData(d,n,k)
        #    start = timer()
        #    estcents = findDensityModes(X,k,l)
        #    end = timer()
        #    print end - start

        #make plots

        n = 2000
        fig = plt.figure()
        for i in range(2,11):
            run(d,n,i,noise=.1,variance=.5,is3d=False)
        plt.show()
    else:
        infile = file(sys.argv[1],'r')
        X=(readcsv(infile))
        k = int(sys.argv[2])
        from timeit import default_timer as timer
        for i in range(10):
            start = timer()
            estcents = findDensityModes(X,k,32)
            end = timer()
            print end - start

        #from scipy.cluster.vq import *
        #kmcent,_ = kmeans(array(estcents),k)


        #from pylab import *
        #import matplotlib.pyplot as plt
        #fig = plt.figure()
        #for b in range(10):
        #    xcol = randint(len(X[0]))
        #    ycol = randint(len(X[0]))
        #    subplot(330+(b+1))
        #    plot([x[xcol] for x in X[::1]],[x[ycol] for x in X[::1]],',')
            #plot([x[xcol] for x in kmcent],[x[ycol] for x in kmcent],'v',color='green',markersize=9)
        #    plot([x[xcol] for x in estcents],[x[ycol] for x in estcents],'*',color='red',markersize=6)

        #plt.show()


        #outfile = file('output_'+sys.argv[1],'w')
        #writecents(estcents,outfile)



