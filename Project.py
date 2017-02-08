from numpy.random import *
from numpy import *


class Project():
    def __init__(self, m,l, projtype=None, X=None):
        self.M = None
        self.P = None
        self.l = l
        if projtype=='dbf':
            self.M,self.P = self.genDBFriendly(m,l)
            self.projtype = 'data base friendly '+str(m)+'x'+str(l)
        elif projtype=='svd':
            if X == None:
                print "Error must specify X, using gaussian RP instead"
                self.P = randn(m,l)
                self.projtype = 'random matrix '+str(m)+'x'+str(l)
            else:
                print "warning running svd on "+str(len(X))+'x'+str(len(X[0]))+" matrix"
                U,s,Vt = linalg.svd(X,full_matrices=False)
                self.P =  ((Vt.T)*((1/s**.5)))[:,:l]
                self.projtype = 'svd projection '+str(m)+'x'+str(l)
        else:
            self.P = randn(m,l)
            self.projtype = 'random matrix '+str(m)+'x'+str(l)

    def genDBFriendly(self,n,t):
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

    def proj(self,v):
        '''
            project a vector based on a M(inuses) and P(luses)
            set of column ids, generated from Achlioptas modified
            random and svd projection
            x - high dimensional vector
            P - len(x) * n matrix of GNV elements
            this is a naive and slow random projection,
            but it's compact and to the point.
        '''
        if self.M==None:
            return dot(v,self.P)
        if self.M!=None and self.P!=None:
            r = [0]*self.l
            sums = 0.0
            scale = (3.0/self.l)**.5
            for i in xrange(self.l):
                sums = 0.0
                for col in self.M[i]:
                    sums -= v[col]
                for col in self.P[i]:
                    sums += v[col]
                r[i] = sums * scale
            return r



if __name__ == "__main__":
    print "nothing in main"
    from pylab import *
    from numpy import *
    from random import *
    num_clusters = 5
    dim = 100
    l = 2
    n = 10000
    X = []
    clu = []
    labels = []
    colors = [',r',',g',',b',',k',',y']
    for i in range(num_clusters):
        clu.append(rand(dim))
    for i in xrange(n):
        labels.append(randint(0,num_clusters-1))
        X.append(clu[labels[-1]]+randn(dim)*.05)
    #u,d,v = linalg.svd(X)
    #proj = (v[:,:l]*d[:l])
    proj = randn(dim,l)
    Xp = []
    for x in X:
        Xp.append(dot(proj.T,x))
    Xp=array(Xp)
    for i in xrange(len(labels)):
        plot(Xp[i,0],Xp[i,1],colors[labels[i]%len(colors)])
    #print d[:10]
    show()

