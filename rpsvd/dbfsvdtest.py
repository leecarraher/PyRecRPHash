import sys
sys.path.append("../")
import DataGen
from numpy import *
import Project
from pylab import *
import time
import fjlt
from sklearn.decomposition import TruncatedSVD



def spectralProj(X,l):
    X = array(X)
    svd = TruncatedSVD(n_components=l)
    pX = svd.fit(X).components_
    return dot(pX,X.T).T
    #d = len(X[0])
    #p = Project.Project(d,2,projtype="svd",X=X)
    #return array([p.proj(x) for x in X])

def dbfspectralProj(X,l):
    X = array(X)
    p1X = fjlt.fjlt_usp(X, l)
    Xldot = dot(p1X,X.T).T
    svd = TruncatedSVD(n_components=2)
    pdbfsvd = svd.fit(Xldot).components_
    #Project.Project(l,2,projtype="svd",X = Xldot)
    return dot(pdbfsvd,Xldot.T).T#   array([pdbfsvd .proj(x) for x in Xldot])


#for i in range(1000,30000,5000):
print "generating data"
colors = ['red','blue','green','orange','purple','brown','black','yellow','pink','magenta','cyan']
cents,X,labels = DataGen.makeData(10000,10000,20,noise = .5,errorperc=0, variance=1,sparseness = .99)
print "dbfspectralproj"
starttime = time.time()
Xdbfsvd = dbfspectralProj(X,100)
print "processing took: ",time.time()-starttime,"s"
print "full spectral proj"
starttime = time.time()
Xsvd = spectralProj(X,2)
print "processing took: ",time.time()-starttime,"s"

subplot(2,1,1)
for i in xrange(len(Xdbfsvd)):
    plot(Xdbfsvd[i][0],Xdbfsvd[i][1],',',color=colors[labels[i]%len(colors)])
subplot(2,1,2)
for i in xrange(len(Xdbfsvd)):
    plot(Xsvd[i][0],Xsvd[i][1],',',color=colors[labels[i]%len(colors)])
show()

