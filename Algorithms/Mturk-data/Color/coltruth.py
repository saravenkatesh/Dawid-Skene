f = open('colimageIds.txt', 'r')
g = open('/Users/saraswathivenkatesh/svenkate-surf-2011-mturk/data/Colors/\
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
            names.append(j[:-5])
        else:
            Ids.append(j[:-1])
    x = g.readline()
    
Idsordered = []
y = f.readline().strip()
while y != "":
    y = y.split()
    Idsordered.append(y[1])
    y = f.readline().strip()

for k in Idsordered:
    indx = Ids.index(k)
    img = names[indx]
    #specific for data set:
    val = int(img[14:])
    if 16 <= val < 49:
        label = 5
    elif 49 <= val < 83:
        label = 4
    elif 83 <= val < 116:
        label = 3
    elif 116 <= val < 150:
        label = 2
    elif 150 <= val < 183:
        label = 1
    else:
        label = 6
    truth.append(label)
    
print len(truth)
f.close()
g.close()
h = open("coltruth.txt", 'w')
for i in truth:
    h.write(str(i))
h.close()