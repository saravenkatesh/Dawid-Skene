f = open('/Users/saraswathivenkatesh/svenkate-surf-2011-mturk/exps/Colors-0/\
pilot-hitlabels.yaml', 'r')

imageIds = []
annIds = []
annlabels = []
time = []

read = f.readline()

while read != "":
    if read[0] == '-':
        pass
    else:
        read = read.split()
        if len(read) == 2:
            ann = read[1]
            if ann not in annIds:
                annIds.append(ann)
                annlabels.append([0 for i in range(200)])
                time.append([0 for i in range(200)])
        elif len(read) == 4 or read[1] == '-':
            Id = read[len(read)-1]
            if Id not in imageIds:
                imageIds.append(Id)
        elif read[0] == '!!python/unicode':
            value = read[2][0]
            annindex = annIds.index(ann)
            imageindex = imageIds.index(Id)
            annlabels[annindex][imageindex] = value
        else:
            annindex = annIds.index(ann)
            imageindex = imageIds.index(Id)
            spent = int(read[3][:-1]) - int(read[6][:-1])
            time[annindex][imageindex] = spent
    read = f.readline()
    
g1 = open('colimageIds.txt', 'w')
for i,j in enumerate(imageIds):
        g1.write(str(i) +'. ' + j + '\n')
g1.close()
g2 = open('colannIds.txt', 'w')
for i in annIds:
    g2.write(i + '\n')
g2.close()
g3 = open('colannlabels.txt', 'w')
for i in annlabels:
    for j in i:
        g3.write(str(j))
    g3.write('\n'*2)
g3.close()
g4 = open('coltime.txt', 'w')
for i in time:
    for j in i:
        g4.write(str(j)+' ')
    g4.write('\n'*2)
g4.close()
g5 = open('colannorg.txt', 'w')
for i in range(len(imageIds)):
    g5.write(str(i)+'. ')
    for j,k in enumerate(annlabels):
        if k[i] != 0:
            g5.write(str(k[i])+', ')
    g5.write( '    ' )
    for j,k in enumerate(annlabels):
        if k[i] != 0:
            g5.write(str(j)+', ')
    g5.write('\n')
g5.close()
g6 = open('numimages.txt', 'w')
for i,j in enumerate(annlabels):
    num = 200 - j.count(0)
    g6.write(str(i)+'. '+str(num)+'\n')
g6.close()

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
h1 = open('orderofimgs.txt', 'w')
ordlabels = [0 for k in range(200)]
x = h.readline()
c = 0
while x != "":
    x = x.split()
    Id = x[1]
    col = names[int(Ids.index(Id))]
    h1.write(str(c) + ': ' + col +'\n')
    x = h.readline()
    c += 1
h.close()
h1.close()