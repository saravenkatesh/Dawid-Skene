import random
import matplotlib.pyplot as plt
import numpy as np

class DawidandSkene():
    
    def __init__(self, annotators, labels, truth, ests, known):
        
        self. a = annotators
        self.l = labels
        self.t = truth
        self.e = ests
	self.k = known
        
    def createMatrix(self, worker):
        
        matrix = [ [ 0.0 for i in range(len(self.l)) ] for j in range(len(self.l)) ]
        
        for j in range(len(self.l)):
            for i in range(len(self.e)):
                if worker[i] != 0:
                    l = worker[i]-1
                    matrix[j][l] += self.e[i][j]
            add = sum(x for x in matrix[j])
            if add != 0:
                matrix[j] = [ k/add for k in matrix[j] ]
                
        return matrix
    
    def Probabilities(self):
        
        probs = [ 0.0 for i in range(len(self.l)) ]
        
        for j in range(len(self.l)):
            for i in range(len(self.t)):
                probs[j] += self.e[i][j]
            probs[j] = probs[j]/len(self.t)
            
        return probs
            
    def Labels(self, probs, matrices):
        
        labels = self.e
        likely = [ ]
        for i in range(len(self.t)):
	    if i not in self.k:
		for j in range(len(self.l)):
		    T = probs[j]
		    for k in range(len(self.a)):
			l = self.a[k][i]
			if l != 0:
			    T = T*matrices[k][j][l-1]
		    labels[i][j] = T
		likely.append(sum(x for x in labels[i]))
		labels[i] = [ k/sum(x for x in labels[i]) for k in labels[i] ]

        likely = sum( np.log10(x) for x in likely)
        return labels, likely
    
    def getPercents(self, ests):
        '''Returns the percent of images that the matrix model accurately
        predicted.'''
        #avg = majority ruling labels
        #matrix = matrix ruling labels
        
        matrixperc = 0.0
        for i in range(len(ests)):
            if ests[i].index(max(ests[i]))+1 == self.t[i]:
                matrixperc += 1
        matrixperc = matrixperc/len(ests)
        
        return matrixperc
            
def Run(p, known):

    labels = [1,2,3,4,5]
    
    annotators = []
    g = open('annlabels.txt', 'r')
    z = g.readline()
    while z != "":
        if z != '\n':
            given = []
            z = z.strip()
            for i in z:
                given.append(int(i))
            annotators.append(given[0:p])
        z = g.readline()
    g.close()

    truth = []
    g1 = open('Truth.txt', 'r')
    y = g1.readline()
    for i in y:
        truth.append(int(i))
    g1.close()
    truth = truth[0:p]

    ests = [ [ 0.0 for i in range(len(labels)) ] for j in range(len(truth)) ]
    for i in range(len(truth)):
	if i not in known:
	    for ann in annotators:
		if ann[i] != 0:
		    ests[i][ann[i]-1] += 1
	    ests[i] = [k/sum(x for x in ests[i]) for k in ests[i]]
	else:
	    ests[i][truth[i]-1] = 1

    oldlikely = 2
    counter = 0
    conv = 1
    
    while conv > 0.001 and counter < 100:
        
        x = DawidandSkene(annotators, labels, truth, ests, known)
        
        matrices = []
        for a in annotators:
            matrices.append(x.createMatrix(a))
	    
        probs = x.Probabilities()

	ests, likely = x.Labels(probs, matrices)
	
        conv = abs(likely - oldlikely)
        counter += 1
	
    counter = 0.0
    for i in range(len(truth)):
        a = []
        for ann in annotators:
	    if ann[i] != 0:
		a.append(ann[i])
        if max(set(a), key=a.count) == truth[i]:
            counter += 1
    print ests
    return x.getPercents(ests), counter/len(truth)
