'''
Created on Jan 9, 2014

@author: lee
'''

def readMatFile(name):
    f = file(name,"r")
    x = int(f.readline())
    y = int(f.readline())
    M = [[0.0]*y for a in xrange(x)]

    for i in xrange(len(M)):
        for j in xrange(len(M[i])):
            M[i][j] = float(f.readline())
    f.close()
    return M

def writeMatFile(M,name):
    f = file(name,"w")
    f.write(str(len(M))+'\n')
    f.write(str(len(M[0]))+'\n')
    for i in xrange(len(M)):
        for j in xrange(len(M[i])):
            f.write(str(M[i][j])+'\n')
    f.close()
    return name

def readVectorIterator(f):
    x = int(f.readline())
    y = int(f.readline())
    for i in xrange(x):
        vec = [0.0]*y
        for j in xrange(y):
            vec[j] = float(f.readline())
        yield vec
    f.close()


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

def readDBFriendProjections():
    mfile = file('M','r')
    M = []
    for l in mfile.readlines():
        M.append([int(st) for st in   l[:-2].split(',') ])
    mfile.close()
    pfile = file('P','r')
    P = []
    for l in pfile.readlines():
        P.append([int(st) for st in   l[:-2].split(',') ])
    pfile.close()
    return M,P

def writecents(estcents,outfile):
    outfile.write(str(len(estcents))+'\n')
    outfile.write(str(len(estcents[0]))+'\n')
    for vec in estcents:
        for val in vec:
            outfile.write(str(val)+'\n')
#import random
#k = 20
#n = 1000
#d = 500
#M = []
#for i in range(k):#
#	cent = [random.random()*2.0-1.0 for j in range(d)]
#	for l in range(n/k):
#		b = []
#		for j in range(d):
#			b.append(cent[j]+random.gauss(0.0,1.0))
#		M.append(b)
#writeMatFile(M,"outputs.mat")
