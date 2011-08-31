import numpy as np
import random

initialize = [[0 for i in range(3)] for j in range(3)]
annotators = []

for i in range(2):
    ann = np.random.rand(2, 2)
    for i, row in enumerate(ann):
        ann[i] = [ k/sum(x for x in row) for k in row ]
    annotators.append(ann)

annotators = [ [[.6, .4],[.4, .6]], [[.7, .3],[.3, .7]],[[.8, .2],[.2, .8]] ]

def Labeling(lst):
    n = random.random()
    for item, weight in lst:
	if n < weight:
	    break
	n -= weight
    return item

f = open('Truth.txt', 'r')
x = f.readline()
truth = [ int(k) for k in list(x) ]
f.close()

anns = []
g = open('annlabels.txt', 'w')
for ann in annotators:
    annlst = []
    for img in truth:
	lst = []
	for i in range(2):
	    lst.append((i+1, ann[img-1][i]))
	g.write(str(Labeling(lst)))
	annlst.append(Labeling(lst))
    anns.append(annlst)
    g.write('\n')
    g.write('\n')
g.close()