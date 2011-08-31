import matplotlib.pyplot as plt
import numpy as np

f = open("colannorg.txt")
labels = []
x = f.readline()
while x != "":
    lst = []
    x = x.split()
    for i in range(1,11):
        y = x[i]
        lst.append(int(y[0]))
    labels.append(lst)
    x = f.readline()
f.close()

f2 = open('colposteriors.txt', 'r')
x = f2.readline()
dands= []
while '(' not in x:
    x = x.split()
    dands.append(int(x[1]))
    x = f2.readline()

g = open('/Users/saraswathivenkatesh/svenkate-surf-2011-mturk/data/Colors/\
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
            names.append(j[14:-5])
        else:
            Ids.append(j[:-1])
    x = g.readline()
g.close()

h = open('colimageIds.txt', 'r')
ordlabels = [0 for k in range(200)]
x = h.readline()
orddands = [0 for k in range(200)]
c = 0
while x != "":
    x = x.split()
    Id = x[1]
    col = names[int(Ids.index(Id))]
    ordlabels[int(col)] = labels[c]
    orddands[int(col)] = dands[c]
    x = h.readline()
    c += 1
   
fig = plt.figure(figsize=(16,5))
plt.ylim(0,7)
plt.xlim(0, 200)
plt.axvline(33.3, linewidth=1, color="black")
plt.axvline(66.7, linewidth=1, color="black")
plt.axvline(100, linewidth=1, color="black")
plt.axvline(133.3, linewidth=1, color="black")
plt.axvline(166.7,linewidth=1, color="black")
plt.xlabel("Image")
plt.ylabel("Labels given to image")
plt.title("Individual image labels")
labels = ['Magenta', 'Blue', 'Cyan', 'Green', 'Yellow', 'Red']
xloc = [16.65, 50, 83.25, 116.55, 149.85, 183.15]
xloc.reverse()
yloc = [1, 2, 3, 4, 5, 6]
plt.xticks(xloc, labels, size=10)
plt.yticks(yloc, labels, size=10)
labs = [1,2,3,4,5,6]
for i, j in enumerate(ordlabels):
    for l in labs:
        heat = float(j.count(l))
        color = (1-heat/10, 1-heat/10, 1-heat/10)
        if color == (0,0,0):
            p1 = plt.plot((i+16)%200,l, 'x', color=color)
        else:
            plt.plot((i+16)%200,l, 'x', color=color)
plt.savefig("allLabels-col.png")
