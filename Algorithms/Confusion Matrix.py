import sys
import csv

#labels == range(1, L)
#truth == list of length I, each entry is the true label of image #i+1
#given_k == list of length I, each entry is what ann k labeled image #i+1 or 0
#   if image wasn't annotated by ann k
#annotators == range(1, K)

class ConfusionMatrix():
    '''Returns the confusion matrix of a single annotator.'''

    def __init__(self, labels, truth, given):
        '''Creates a list of the labels and the proper dimension matrix.'''

        self.labels = list(labels)
        self.t = truth
        self.g = given
        self.matrix = [ [ 0.0 for i in range(len(labels)) ]
                        for j in range(len(labels)) ]

    def createMatrix(self):
        '''Creates the confusion matrix given the data, where truth is a
        list of each image's true label and given is a list of each image's
        given label.'''

        label_count = [ 0 for i in range(len(self.labels)) ]

        for i,j in enumerate(self.t):
            if self.g[i] != 0:
                label_count[j - 1] += 1
                self.matrix[j-1][self.g[i]-1] += 1

        for r,c in enumerate(self.matrix):
            if label_count[r] != 0:
                for k in range(len(c)):
                    self.matrix[r][k] = round(self.matrix[r][k]/label_count[r], 2)
            
        return self.matrix

    def prettyMatrix(self):
        '''Prints confusion matrix as a pretty table.'''

        writer = csv.writer(sys.stdout, dialect=csv.excel_tab)
        tab = [[' ']]
        for i, j in enumerate(self.labels):
            tab[0].append(j)
            row = []
            row.append(j)
            for k in range(len(self.labels)):
                row.append(self.matrix[i][k])
            tab.append(row)
        writer.writerows(tab)


class Posterior(ConfusionMatrix):
    '''Returns the predicted label of each image.'''

    def __init__(self, annotators, labels, truth):
        '''annotators is a nested list, each list being that respective
        annotator's labels.'''

        self.ann = annotators
        self.l = labels
        self.t = truth

    def allMatrices(self):
        '''Creates a list of all confusion matrices.'''

        allmatrices = []
        for i in self.ann:
            x = ConfusionMatrix(self.l, self.t, i)
            y = x.createMatrix()
            allmatrices.append(y)
        return allmatrices

    def getProbabilities(self):
        '''Returns a list of the probability that a random image i has label
        j.'''

        probs = [0.0 for l in range(len(self.l))]
        for t in self.t:
            probs[t - 1] += 1
        for p in range(len(probs)):
            probs[p] = probs[p]/len(self.t)
            print probs[p]
        return probs

    def getNumerators(self):
        '''List of the conditional probabilities of each image.'''

        nums = []

        probs = [0.0 for l in range(len(self.l))]
        for t in self.t:
            probs[t - 1] += 1
        for p in range(len(probs)):
            probs[p] = probs[p]/len(self.t)

        allmatrices = []
        for i in self.ann:
            x = ConfusionMatrix(self.l, self.t, i)
            y = x.createMatrix()
            allmatrices.append(y)
        
        for i in range(len(self.t)):
            lst = []
            for j in range(len(self.l)):
                pr = 1
                for a in range(len(self.ann)):
                    if self.ann[a][i] != 0:
                        label = self.ann[a][i]
                        pi = allmatrices[a][j][label-1]
                        pr = pr*pi
                lst.append(pr*probs[j])
            nums.append(lst)
        return nums
        
    def getPosterior(self, numerators):
        '''Returns posteriors for every image and every label in a nested
        list.'''

        posteriors = []
        for i in numerators:
            imageposts = []
            total = sum(x for x in i)
            for j in i:
                imageposts.append(j/total)
            posteriors.append(imageposts)
        return posteriors
    
    def getAverage(self):
        '''Returns majority rule labeling of each image.'''
        
        def most_common(lst):
            return max(set(lst), key=lst.count)
        
        averages = []
        for i in range(len(self.t)):
            labels = []
            for j in self.ann:
                if j[i] != 0:
                    labels.append(j[i])
            averages.append(most_common(labels))
        return averages
    
    def getPercents(self, avg, matrix):
        
        avgperc = 0.0
        for i in range(len(self.t)):
            if avg[i] == self.t[i]:
                avgperc += 1
        avgperc = avgperc/len(self.t)
        
        matrixperc = 0.0
        for i in range(len(self.t)):
            if matrix[i] == self.t[i]:
                matrixperc += 1
        matrixperc = matrixperc/len(self.t)
        
        return matrixperc, avgperc

if __name__ == '__main__':
    
    labels = [1,2,3,4,5,6]
    
    truth = []
    f = open('Bird/birdtruth.txt', 'r')
    y = f.readline()
    for i in y:
        truth.append(int(i))
    f.close()
    
    annotators = []
    g = open('Bird/birdannlabels.txt', 'r')
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
    y = x.getNumerators()
    z = x.getPosterior(y)
    w = x.getAverage()
    
    matrixlabels = []                    
    h = open('birdposteriors.txt', 'w')
    for i,j in enumerate(z):
        imgmax = max(j)
        label = j.index(imgmax) + 1
        matrixlabels.append(label)
        h.write(str(i) + '. ' + str(label) + ' ' + str(w[i]) + ' ' + str(truth[i]) + '\n')
    h.write(str(x.getPercents(w, matrixlabels)))
    h.close()
            
