from DandSmodel import DawidandSkene
import matplotlib.pyplot as plt
import numpy as np
import random
from pylab import show

labels = [1,2,3,4,5,6]

truth = []
f = open('birdtruth.txt', 'r')
y = f.readline()
for i in y:
    truth.append(int(i))
f.close()

annotators = []
g = open('birdannlabels.txt', 'r')
z = g.readline()
while z != "":
    if z != '\n':
        given = []
        z = z.strip()
        for i in z:
            given.append(int(i))
        annotators.append(given)
    z = g.readline()
g.close()

ests = [ [ 0.0 for i in range(len(labels)) ] for j in range(len(truth)) ]
for i in range(len(truth)): #Initialize using ground truth
    for j in range(len(ests[i])):
	if truth[i] == j+1:
	    ests[i][j]= 1
	else:
	    ests[i][j] = 0
	    
x = DawidandSkene(annotators, labels, truth, ests)
allmats = []
for i in annotators:
    allmats.append(x.createMatrix(i))

for i in range(len(allmats)):
    name = 'birdheat-'+str(i)+'.png'
    data = allmats[i]
    data = np.array(data)
    data.shape = (6,6)
    fig = plt.figure(figsize=(4,4))
    plt.gray()
    plt.pcolormesh(data)
    labels = [1, 2, 3, 4, 5, 6]
    loc = [.5, 1.5, 2.5, 3.5, 4.5, 5.5]
    plt.xticks(loc, labels, size=10) 
    plt.yticks(loc, labels, size=10)
    plt.xlabel("Given")
    plt.ylabel("Truth")
    plt.savefig(name)