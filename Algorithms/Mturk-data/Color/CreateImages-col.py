from Confusion_Matrix_col import Posterior

labels = [1,2,3,4,5,6]
    
truth = []
f = open('coltruth.txt', 'r')
y = f.readline()
for i in y:
    truth.append(int(i))
f.close()
    
annotators = []
g = open('colannlabels.txt', 'r')
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

for i,j in enumerate(allmats):
    x.CreateImgs(j, 'col-'+str(i)+'.jpg')