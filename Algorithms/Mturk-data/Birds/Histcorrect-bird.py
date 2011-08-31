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

pcntcorrect = []
for ann in annotators:
    counter = 1.0
    correct = 1.0
    for i in range(len(ann)):
        if ann[i] == truth[i]:
            correct += 1
        if ann[i] != 0:
            counter += 1
    pcntcorrect.append(correct/counter)
    print correct/counter, annotators.index(ann)

import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(1)
mean = np.mean(pcntcorrect)
std = np.std(pcntcorrect)
textstr = '$\mu=%.2f$\n$\sigma=%.2f$' %(mean, std)
plt.hist(pcntcorrect,color=(0,.392,.314))
plt.xlabel("Fraction of images annotated correctly")
plt.ylabel("Number of annotators")
plt.title("How often an annotator labels an image correctly")
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text(0.05, 0.95, textstr, transform=ax.transAxes, fontsize=14,
    verticalalignment='top', bbox=props)
plt.savefig("Correcthist-bird.png")