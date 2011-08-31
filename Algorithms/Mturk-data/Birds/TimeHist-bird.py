import matplotlib.pyplot as plt
import numpy as np
import pylab

'''g = open('/Users/saraswathivenkatesh/svenkate-surf-2011-mturk/data/birdscale/\
image-ids.yaml', 'r')
names = []
Ids = []
x = g.readline()
while x != "":
    x = x.split()
    for i, j in enumerate(x):
        if i%2 == 0:
            if j[0] == '{':
                j = j[1:]
            names.append(int(j[14:-5]))
        else:
            Ids.append(j[:-1])
    x = g.readline()
g.close()
Idssort = [0 for i in range(256)]
for i in range(256):
    indx = names.index(i)
    Idssort[i] = Ids[indx]

h = open('birdimageIds.txt', 'r')
Idsordered = []
x = h.readline()
while x != "":
    x = x.split()
    Idsordered.append(x[1])
    x = h.readline()
h.close()'''

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

'''avgT = []
for t in range(len(times[0])):
    sm = 0
    div = 0
    for ann in times:
        if ann[t] != 0:
            sm += float(ann[t])
            div += 1
    avgT.append(sm/div)'''
    
'''avgTsort = [0 for i in range(len(avgT))]
for i, j in enumerate(avgT):
    label = Idsordered[i]
    indx = Idssort.index(label)
    avgTsort[indx] = int(j)'''
           
#x = range(len(avgT))
avgmedian = 0
avgmean = 0
alltimes = []

for i,j in enumerate(times):
    fig, ax = plt.subplots(1)
    bins = [float(k)/5 for k in range(0,21)]
    n, b = np.histogram(np.log10(j), bins)
    bincenters = [10**(k+.1) for k in bins[:-1]]
    plt.semilogx(bincenters, n)
    plt.xlabel('Time spent (ms)')
    plt.ylabel('Count')
    plt.title('Histogram of time spent by Annotator '+str(i))
    plt.ylim(ymax=110)
    median = np.median(j)
    avgmedian += median
    mu = np.mean(j)
    avgmean += mu
    textstr = '$\mu=%.2f$\n$\mathrm{median}=%.2f$' %(mu, median)
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.1, 0.95, textstr, transform=ax.transAxes, fontsize=14,\
        verticalalignment='top', bbox=props)
    plt.savefig('Ann'+str(i)+'-times-bird.png')
    alltimes.append(mu)
    
f = open('alltimes-bird.txt', 'w')
for i in alltimes:
    f.write(str(i)+' ')
f.close()
    
avgmedian = avgmedian/len(times)
avgmean = avgmean/len(times)
fig, ax = plt.subplots(1)
bins = [float(k)/5 for k in range(0,21)]
n, b = np.histogram(alltimes, bins)
bincenters = [10**(k+.1) for k in bins[:-1]]
plt.semilogx(bincenters, n)
plt.xlabel("Time Spent (ms)")
plt.ylabel("Count")
plt.title("Histogram of Time Spent by All Annotators")
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
textstr = '$\mu=%.2f$\n$\mathrm{median}=%.2f$' %(avgmean, avgmedian)
ax.text(0.1, 0.95, textstr, transform=ax.transAxes, fontsize=14, \
    verticalalignment='top', bbox=props)
plt.savefig('bird-avgtimes.png')