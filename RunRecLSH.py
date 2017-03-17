from PyIOUtils import *
from Project import *
from RecursLSH import *
import numpy as np
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

    #different densities
    k3 = int((k/3.0)+.5)
    cents, X, labels = makeData(d,n,k,noise,errorperc,2*variance,sparseness)
    #cents2, X2 = makeData(d,n/3,k3,noise,errorperc,variance,sparseness)
    #cents = np.append(cents,cents2, axis=0)
    #X = np.append(X,X2, axis=0)
    #cents3, X3 = makeData(d,n/3,k3,noise,errorperc,.2*variance,sparseness)
    #cents = np.append(cents,cents3, axis=0)
    #X = np.append(X,X3, axis=0)

    projector = Project(len(X[0]),l,projtype='dbf')
    clusterer = RecLSH(projector=projector)

    estcents = clusterer.findDensityModes(X,k,l)

    #randomly pick the axis to plot
    xcol , ycol , zcol = 0,1,2#randint(d),randint(d),randint(d)
    while xcol == ycol: ycol = randint(d)
    while zcol == ycol or zcol == xcol: zcol = randint(d)

    if is3d:
        ax = fig.add_subplot(330+(k-1), projection='3d')
        ax.scatter([x[xcol] for x in X[::6]],[x[ycol] for x in X[::6]],[x[zcol] for x in X[::6]],',b',s=1)
        ax.scatter([x[xcol] for x in estcents],[x[ycol] for x in estcents],[x[zcol] for x in estcents],'o',color='gold',marker='o',s=20)
        ax.scatter([x[xcol] for x in pcents],[x[ycol] for x in pcents],[x[zcol] for x in pcents],color='red',marker='*',s=20)

    else:
        subplot(330+((k-1)))
        for x in X[::2]:
            x =projector.proj(x)
            plot(x[0],x[1] ,',g')
        for x in estcents:
            x =projector.proj(x)
            plot(x[0],x[1] ,'o',color='gold',markersize=8)
        for x in cents:
            x =projector.proj(x)
            plot(x[0],x[1] ,'*',color='red',markersize=7)

            #for keyidx in xrange(len(estcents.keys())):
            #    key = estcents.keys()[keyidx]
            #    x = pestcents[key]
                #s = ""
                #for key2 in estcents.keys():
                #    s += str(bin(key^key2).count('1'))+','

             #   plot(x[xcol],x[ycol],'o',color='gold',markersize=8)
                #annotate(str(keyidx), (x[xcol],x[ycol]))


            #plot([x[xcol] for x in kmcents],[x[ycol] for x in kmcents],'v',color='green',markersize=7)

if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1 :
        from DataGen import *
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
        d = 1000

        #make plots
        n = 2000
        fig = plt.figure()

        for i in range(2,11):
            run(d,n,i,noise=0,variance=.3,sparseness = 0,errorperc =0, is3d=False)
        plt.show()
    else:
        X=readMatFile(sys.argv[1])
        k = int(sys.argv[2])
        l = 30

        if len(sys.argv)>4:
            l = sys.argv[4]

        projector = Project(len(X[0]),l,projtype='dbf')
        clusterer = RecLSH(projector=projector)
        estcents = clusterer.findDensityModes(X,k,l)

        #from scipy.cluster.vq import *
        #kmcent,_ = kmeans(array(estcents),k)

        if len(sys.argv)>3 and sys.argv[3]=='plot=true':
            from pylab import *
            import matplotlib.pyplot as plt
            fig = plt.figure()

            P = randn(len(X[0]),2)

            for i in xrange(len(X)):
                X[i] = array(X[i]).dot(P)*(1/float(len(P[0])))**.5

            for i in xrange(len(estcents)):
                estcents[i] = array(estcents[i]).dot(P)*(1/float(len(P[0])))**.5

            projector = clusterer.getProjector()

            for i in xrange(len(X)):
                X[i] = projector.proj(X[i])
            for i in xrange(len(estcents)):
                estcents[i] = projector.proj(estcents[i])

            for b in range(25):
                xcol = b*2
                ycol = b*2+1
                subplot(5,5,(b+1))
                plot([x[xcol] for x in X[::1]],[x[ycol] for x in X[::1]],',')
                #plot([x[xcol] for x in kmcent],[x[ycol] for x in kmcent],'v',color='green',markersize=9)
                plot([x[xcol] for x in estcents],[x[ycol] for x in estcents],'*',color='red',markersize=6)

            plt.show()

        outfile = file(sys.argv[1]+'_output','w')
        writecents(estcents,outfile)
