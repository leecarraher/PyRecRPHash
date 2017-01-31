from RandomProjection import *

def hashvec(x):
    '''
        super simple hash algorithm, reminiscient of pstable lsh
    '''
    s = 0
    for i in xrange(len(x)):
        s<<=1
        if x[i]> 0:s+=1
    return s

def addtocounter(x,M,P,IDAndCount,IDAndCent,l):
    '''
        x          - input vector
        IDAndCount - ID->count map
        IDAndCent  - ID->centroid vector map
        hash the projected vector x and update
        the hash to centroid and counts maps
    '''
    xt = proj2(x,M,P,l)
    s = hashvec(xt)
    for i in xrange(0,l):
        partialhash = s>>i
        if IDAndCount.has_key(partialhash):
            IDAndCount[partialhash] = IDAndCount[partialhash]+1
            IDAndCent[partialhash].append(x)
        else:
            IDAndCount[partialhash] = 1
            IDAndCent[partialhash] = [x]

def medoid(X):
    '''
        X - set of vectors
        compute the medoid of a vector set
    '''
    ret = X[0]
    for i in xrange(1,len(X)):
        for j in xrange(len(X[i])): ret[j]+=X[i][j]
    for j in  xrange(len(ret)):ret[j]= ret[j]/float(len(X))
    return ret

def isPowerOfTwo (x):
  return ((x != 0) and not(x & (x - 1)))

def findDensityModes(X,k,l):
    '''
        X - data set
        k - canonical k in k-means
        l - clustering sub-space
        Compute density mode via iterative deepening hash counting
    '''
    #our counter, replace with mincount hash
    IDAndCount = {}
    IDAndCent = {}

    #create projector matrixs
    M,P = genDBFriendly(len(X[0]),l)
    #P = randn(len(X[0]),l)
    #M =[]

    #process data by adding to the counter
    for x in X:
        addtocounter(x,M,P,IDAndCount, IDAndCent,l)

    densityAndID = []
    for h in sort(IDAndCount.keys()):
        densityAndID.append((IDAndCount[h],h))
        #remove parents
        h>>=1
        if densityAndID.__contains__((IDAndCount[h],h)):
            densityAndID.remove((IDAndCount[h],h))
    # sort
    densityAndID.sort(reverse=True)

    # compute medoids
    estcentsmap = {}
    for d in densityAndID[:int(k*2)]:
        idcent = d[1]
        estcentsmap[idcent] = medoid(IDAndCent[idcent])

    mergelist = []
    for i in xrange(len(estcentsmap.keys())):
        d =estcentsmap.keys()[i]
        for ii in xrange(i+1,len(estcentsmap.keys())):
            dd = estcentsmap.keys()[ii]
            if isPowerOfTwo(d^dd):
                mergelist.append([d^dd,[d,dd]])

    mergelist.sort(reverse=True)

    for mergers in mergelist:
        if len(estcentsmap) == k:
            return estcentsmap
        if estcentsmap.has_key(mergers[1][1]) and estcentsmap.has_key(mergers[1][0]):
            estcentsmap[mergers[1][1]] = medoid(vstack((estcentsmap[mergers[1][0]],estcentsmap[ mergers[1][1] ])))
        estcentsmap.pop(mergers[1][0],None)
    return estcentsmap
