from DataGen import *
from PyIOUtils import *
from RandomProjection import *
from RecursLSH import *
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
    from scipy.cluster.vq import kmeans
    kmcents,_ = kmeans(array(X),k)

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
        subplot(330+((k-1)))
        plot([x[xcol] for x in X[::1]],[x[ycol] for x in X[::1]],',')
        for keyidx in xrange(len(estcents.keys())):
            key = estcents.keys()[keyidx]
            x = estcents[key]
            #s = ""
            #for key2 in estcents.keys():
            #    s += str(bin(key^key2).count('1'))+','

            plot(x[xcol],x[ycol],'o',color='gold',markersize=8)
            #annotate(str(keyidx), (x[xcol],x[ycol]))

        plot([x[xcol] for x in cents],[x[ycol] for x in cents],'*',color='red',markersize=7)
        #plot([x[xcol] for x in kmcents],[x[ycol] for x in kmcents],'v',color='green',markersize=7)

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
        l = 31
        k = 10
        d = 100

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
            run(d,n,i,noise=.75,variance=0.75,is3d=False)
        plt.show()
    else:
        infile = file(sys.argv[1],'r')
        X=readcsv(infile)
        k = int(sys.argv[2])
        estcents = findDensityModes(X,k,32)


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
