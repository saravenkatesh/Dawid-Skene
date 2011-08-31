import matplotlib.pyplot as plt
import numpy as np

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

hues = []
f = open('orderofimgs.txt', 'r')
z = f.readline()
while z != "":
    z = z.strip()
    z = z.split()
    hues.append(((float(z[1])+50.0/3)%200)/200)
    z = f.readline()
f.close()

values = []
h = open('datavalues.txt', 'r')
z = h.readline()
while z != "":
    values.append(float(z.strip()))
    z = h.readline()
h.close()

def getColor(number):
    
    if number == 1:
        color = 'm'
    elif number == 2:
        color = 'b'
    elif number == 3:
        color = 'c'
    elif number == 4:
        color = 'g'
    elif number == 5:
        color = 'y'
    else:
        color = 'r'
        
    return color

for i,ann in enumerate(annotators):
    fig, ax = plt.subplots(1)
    plt.title('Annotator '+str(i)+"'s Labels")
    ax.set_ylim(0, 1)
    ax.set_xlim(0, 1)
    plt.axvline(x=1.0/6, linestyle='--', color='black', linewidth=.5)
    plt.axvline(x=2.0/6, linestyle='--', color='black', linewidth=.5)
    plt.axvline(x=3.0/6, linestyle='--', color='black', linewidth=.5)
    plt.axvline(x=4.0/6, linestyle='--', color='black', linewidth=.5)
    plt.axvline(x=5.0/6, linestyle='--', color='black', linewidth=.5)
    for j,img in enumerate(ann):
        if img != 0:
            plt.plot(hues[j], values[j], getColor(img)+'o')
            plt.xlabel('Hue')
            plt.ylabel('Value')
    plt.savefig('annotator-'+str(i)+'labelvshv.png')
