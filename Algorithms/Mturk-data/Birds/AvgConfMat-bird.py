from Confusion_Matrix_bird import Posterior

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
    
x = Posterior(annotators, labels, truth)
allmats = x.allMatrices()

averagemat = [[0 for i in range(6)] for j in range(6)]

for i in range(6):
    for j in range(6):
        avg = 0
        for mat in allmats:
            avg += mat[i][j]
        avg = round(avg/len(allmats),2)
        averagemat[i][j] = avg

x.CreateImgs(averagemat, "avgconfusion.jpg")

import matplotlib.pyplot as plt
import numpy as np
import random
from pylab import show

data = averagemat
data = np.array(data)
data.shape = (6,6)

fig = plt.figure()
plt.xlabel('Given')
plt.ylabel('Truth')
plt.gray()
fig.subplots_adjust(bottom=0.2, left=.15)
plt.pcolormesh(data)
labels = ['Sage thrasher', 'Cactus wren', 'Waterthrush', 'Blue grosbeak', 'Indigo bunting', 'Lazuli bunting']
loc = [.5, 1.5, 2.5, 3.5, 4.5, 5.5]
plt.xticks(loc, labels, size=10, rotation=45) 
plt.yticks(loc, labels, size=10, rotation=45)
plt.colorbar() 
plt.savefig("avgconfusion-bird.png")
