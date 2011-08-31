import numpy as np
import matplotlib.pyplot as plt

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

    
f = open('birdtime.txt', 'r')
times = []
x = f.readline()
while x != "":
    t = []
    if x != "\n":
        x = x.split()
        for i,j in enumerate(x):
            if j != '0':
                t.append(int(j))
        times.append(t)
    x = f.readline()    
f.close()
alltimes = []
for i,j in enumerate(times):
    median = np.median(j)
    alltimes.append(np.log10(median))
    
plt.scatter(alltimes, pcntcorrect)
plt.xlabel('Median time (ms log scale)')
plt.ylabel('Accuracy')
plt.title('Annotator median time spent vs. accuracy')
plt.axvline(x=np.mean(alltimes), linestyle='--')
plt.axhline(y=np.mean(pcntcorrect), linestyle='--')
plt.savefig('timevsacc-bird.png')