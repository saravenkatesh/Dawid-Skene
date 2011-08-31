f = open('/Users/saraswathivenkatesh/svenkate-surf-2011-mturk/exps/Birds-0/\
pilot-hitlabels.yaml', 'r')

imageIds = []
annIds = []
annlabels = []
time = []

def perm(j):
    if j == '1':
        k = '1'
    elif j == '2':
        k = '4'
    elif j == '3':
        k = '6'
    elif j == '4':
        k = '5'
    elif j == '5':
        k = '3'
    else:
        k = '2'
    return k  

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
                annlabels.append([0 for i in range(181)])
                time.append([0 for i in range(181)])
        elif len(read) == 4 or read[1] == '-':
            Id = read[len(read)-1]
            if Id not in imageIds:
                imageIds.append(Id)
        elif read[0] == '!!python/unicode':
            value = read[2][0]
            annindex = annIds.index(ann)
            imageindex = imageIds.index(Id)
            annlabels[annindex][imageindex] = perm(value)
        else:
            annindex = annIds.index(ann)
            imageindex = imageIds.index(Id)
            spent = int(read[3][:-1]) - int(read[6][:-1])
            time[annindex][imageindex] = spent
    read = f.readline()

g1 = open('birdimageIds.txt', 'w')
for i,j in enumerate(imageIds):
    g1.write(str(i) + '. ' + j + '\n')
g1.close()
g2 = open('birdannIds.txt', 'w')
for i in annIds:
    g2.write(i + '\n')
g2.close()
g3 = open('birdannlabels.txt', 'w')
for i in annlabels:
    for j in i:
        g3.write(str(j))
    g3.write('\n'*2)
g3.close()
g4 = open('birdtime.txt', 'w')
for i in time:
    for j in i:
        g4.write(str(j)+' ')
    g4.write('\n'*2)
g4.close()
g5 = open('birdannorg.txt', 'w')
for i in range(len(imageIds)):
    g5.write(str(i)+'. ')
    for j,k in enumerate(annlabels):
        if k[i] != 0:
            g5.write(str(k[i])+', ')
    g5.write( '      ' )
    for j,k in enumerate(annlabels):
        if k[i] != 0:
            g5.write(str(j)+', ')
    g5.write('\n')
g5.close()
g6 = open('numimages.txt', 'w')
for i,j in enumerate(annlabels):
    num = 181 - j.count(0)
    g6.write(str(i)+'. '+str(num)+'\n')
g6.close()
