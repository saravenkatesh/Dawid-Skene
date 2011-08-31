import numpy as np
import random
import matplotlib.pyplot as plt
import numpy as np

class DawidandSkene():
    
    def __init__(self, annotators, labels, truth, ests):
        
        self. a = annotators
        self.l = labels
        self.t = truth
        self.e = ests
        
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
        
        labels = [ [ 0.0 for i in range(len(self.l)) ] for j in range(len(self.t)) ]
        likely = [ ]
        for i in range(len(self.t)):
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
            
if __name__ == '__main__':
    
    labels = [1,2]
    
    annmats = [ [[.8, .2],[.2, .8]], [[.8, .2],[.2, .8]], [[.8, .2],[.2, .8]] ]

    def Labeling(lst):
	n = random.random()
	for item, weight in lst:
	    if n < weight:
		break
	    n -= weight
	return item
    
    fullannotators = []
    g = open('annlabels.txt', 'r')
    z = g.readline()
    while z != "":
        if z != '\n':
            given = []
            z = z.strip()
            for i in z:
                given.append(int(i))
            fullannotators.append(given)
        z = g.readline()
    g.close()
    
    initialtruth = []
    g1 = open('Truth.txt', 'r')
    y = g1.readline()
    for i in y:
        initialtruth.append(int(i))
    g1.close()
    
    averages = []

    for n in range(5,31,5):
        
        avg = 0.0
        
        for m in range(1000):
	    
	    rand = random.sample(range(31), n)
	    truth = []
	    for r in rand:
		truth.append(initialtruth[r])
	    annotators = []
	    for ann in fullannotators:
		a = []
		for r in rand:
		    a.append(ann[r])
		annotators.append(a)
    
            ests = [ [ 0.0 for i in range(len(labels)) ] for j in range(len(truth)) ]
            for i in range(len(truth)):
                for ann in annotators:
                    if ann[i] != 0:
                        ests[i][ann[i]-1] += 1
                ests[i] = [k/sum(x for x in ests[i]) for k in ests[i]]
        
            oldlikely = 2
            counter = 0
            conv = 1
    
            while conv > 0.0001 and counter < 100:

                x = DawidandSkene(annotators, labels, truth, ests)
        
                matrices = []
                for a in annotators:
                    matrices.append(x.createMatrix(a))
            
                probs = x.Probabilities()
        
                ests, likely = x.Labels(probs, matrices)
        
                conv = abs(likely - oldlikely)
                counter += 1
            
            avg += x.getPercents(ests)
        averages.append(avg/1000)
        
    plt.plot(averages)
    plt.show()
        