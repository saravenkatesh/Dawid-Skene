import matplotlib.pyplot as plt
import numpy as np

ds = [.6205, .8007, .8658, .8939, .9096, .9229, .9356, .9484, .9625, .9844]
maj = [.509, .5048, .754, .75, .8131, .8126, .8485, .8485, .8612, .8541]
lenient = [ .6971, .8966, .8784, .8774, .8806, .9031, .8971, .9199, .9084, .9111]

p1, = plt.plot(ds)
p2, = plt.plot(maj)
p3, = plt.plot(lenient)
plt.legend([p1, p2, p3], ["D&S", "strict majority", "lenient majority"], loc=4)
plt.xlabel("Number of annotators per image (chosen randomly)")
plt.ylabel("Fraction of images labeled correctly")
plt.title("Annotating Accuracy Using Different Methods")
plt.savefig("Diff-models-script.png")