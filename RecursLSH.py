from Project import *
class RecLSH():

    def __init__(self,projector=None):
        #our counter, replace with mincount hash
        self.IDAndCount = {}
        self.IDAndCent = {}
        self.projector = projector

    def getProjector(self):
        return self.projector


    def hashvec(self,x):
        '''
            super simple hash algorithm, reminiscient of pstable lsh
        '''
        s = 0
        for i in xrange(len(x)):
            s<<=1
            if x[i]> 0:s+=1
        return s

    def addtocounter(self,x,l):
        '''
            x          - input vector
            IDAndCount - ID->count map
            IDAndCent  - ID->centroid vector map
            hash the projected vector x and update
            the hash to centroid and counts maps
        '''
        xt = self.projector.proj(x)
        s = self.hashvec(xt)
        for i in xrange(0,l):
            partialhash = s>>i
            if self.IDAndCount.has_key(partialhash):
                self.IDAndCount[partialhash] = self.IDAndCount[partialhash]+1
                self.IDAndCent[partialhash].append(x)
            else:
                self.IDAndCount[partialhash] = 1
                self.IDAndCent[partialhash] = [x]

    def medoid(self,X):
        '''
            X - set of vectors
            compute the medoid of a vector set
        '''
        ret = X[0]
        for i in xrange(1,len(X)):
            for j in xrange(len(X[i])): ret[j]+=X[i][j]
        for j in  xrange(len(ret)):ret[j]= ret[j]/float(len(X))
        return ret

    def isPowerOfTwo (self,x):
      return ((x != 0) and not(x & (x - 1)))

    def findDensityModes(self,X,k,l):
        '''
            X - data set
            k - canonical k in k-means
            l - clustering sub-space
            Compute density mode via iterative deepening hash counting
        '''

        if self.projector == None:
            self.projector = Project(len(X[0]),l,projtype='dbf')

        #process data by adding to the counter
        for x in X:
            self.addtocounter(x,l)

        densityAndID = []
        for h in sort(self.IDAndCount.keys()):
            densityAndID.append((self.IDAndCount[h],h))
            #remove parents
            h>>=1
            if densityAndID.__contains__((self.IDAndCount[h],h)):
                densityAndID.remove((self.IDAndCount[h],h))
        # sort
        densityAndID.sort(reverse=True)

        # compute medoids
        estcentsmap = {}
        for d in densityAndID[:int(k*2)]:
            idcent = d[1]
            estcentsmap[idcent] = self.medoid(self.IDAndCent[idcent])

        mergelist = []
        for i in xrange(len(estcentsmap.keys())):
            d =estcentsmap.keys()[i]
            for ii in xrange(i+1,len(estcentsmap.keys())):
                dd = estcentsmap.keys()[ii]
                if self.isPowerOfTwo(d^dd):
                    mergelist.append([d^dd,[d,dd]])

        mergelist.sort(reverse=True)

        for mergers in mergelist:
            if len(estcentsmap) == k:
                return estcentsmap
            if estcentsmap.has_key(mergers[1][1]) and estcentsmap.has_key(mergers[1][0]):
                estcentsmap[mergers[1][1]] = self.medoid(vstack((estcentsmap[mergers[1][0]],estcentsmap[ mergers[1][1] ])))
            estcentsmap.pop(mergers[1][0],None)
        return estcentsmap
