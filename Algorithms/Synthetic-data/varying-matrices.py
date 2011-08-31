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

        return labels, likely
    
    def getPercents(self, matrix):
        '''Returns the percent of images that the matrix model accurately
        predicted.'''
        #avg = majority ruling labels
        #matrix = matrix ruling labels
        
        matrixperc = 0.0
        for i in range(len(matrix)):
            if matrix[i] == self.t[i]:
                matrixperc += 1
        matrixperc = matrixperc/len(matrix)
        
        return matrixperc
            
if __name__ == '__main__':
    
    labels = [1,2]
    realmats = [ np.eye(2), np.eye(2), np.eye(2) ]
    averages = []
    for y in range(31):
	if y != 0:
	    i = y%3
	    realmats[i][0][0] -= .1
	    realmats[i][1][1] -= .1
	    realmats[i][1][0] += .1
	    realmats[i][0][1] += .1

	correctavg = []
	for z in range(50):
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

	    g = open('annlabels.txt', 'w')
	    for ann in realmats:
		for img in truth:
		    lst = []
		    for i in range(2):
			lst.append((i+1, ann[img-1][i]))
		    g.write(str(Labeling(lst)))
		g.write('\n')
		g.write('\n')
	    g.close()
    
	    annotators = []
	    g = open('annlabels.txt', 'r')
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
	    for i in range(len(truth)):
		for ann in annotators:
		    if ann[i] != 0:
			ests[i][ann[i]-1] += 1
		ests[i] = [k/sum(x for x in ests[i]) for k in ests[i]]
        
	    conv = 1
	    counter = 0
	    while conv > .0001 and counter < 100:
		if counter != 0:
		    oldlikely = likely
		x = DawidandSkene(annotators, labels, truth, ests)
		matrices = []
		for a in annotators:
		    matrices.append(x.createMatrix(a))
		probs = x.Probabilities()
		ests, likely = x.Labels(probs, matrices)
		likely = sum( np.log10(z) for z in likely )
		if counter != 0:
		    conv = abs(likely - oldlikely)
		counter += 1
		
		matrixlabels = []
		for i, j in enumerate(ests):
		    imgmax = max(j)
		    label = j.index(imgmax) + 1
		    matrixlabels.append(label)
		correctavg.append(x.getPercents(matrixlabels))
	    
	averages.append(np.mean(correctavg))
	    
plt.plot(averages, 'b.')
plt.savefig("Varying-matrices-correct.png")
            
        