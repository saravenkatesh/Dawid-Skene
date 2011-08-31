f = open('birdimageIds.txt', 'r')
g = open('/Users/saraswathivenkatesh/svenkate-surf-2011-mturk/data/Birds/\
image-ids.yaml', 'r')

names = []
Ids = []
truth = []

x = g.readline()

while x != "":
    x = x.split()
    for i, j in enumerate(x):
        if i%2 == 0:
            if j[0] == '{':
                j = j[1:]
            names.append(j[:-1])
        else:
            Ids.append(j[:-1])
    x = g.readline()
    
Idsordered = []
y = f.readline().strip()
while y != "":
    Idsordered.append(y)
    y = f.readline().strip()

for k in Idsordered:
    k = k.split()
    indx = Ids.index(k[1])
    img = names[indx]
    #specific for data set:
    val = img[0]
    if val == 'C':
        label = 2
    elif val == 'N':
        label = 3
    elif val == 'I':
        label = 5
    elif val == 'L':
        label = 6
    elif val == 'B':
        label = 4
    else:
        label = 1
    truth.append(label)

f.close()
g.close()
h = open("birdtruth.txt", 'w')
for i in truth:
    h.write(str(i))
h.close()