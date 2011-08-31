import matplotlib.pyplot as plt
import numpy as np

ds = [.5201, .5979, .6783, .7464, .7895, .8219, .8501, .8756, .9034, .9503]
maj = [.6174, .4795, .6234, .6166, .6232, .6283, .6341, .6255, .6267, .6243]
lenient = [.6174, .7752, .6841, .6941, .701, .681, .673, .674, .658, .653]

p1, = plt.plot(ds)
p2, = plt.plot(maj)
p3, = plt.plot(lenient)
plt.legend([p1, p2, p3], ["D&S", "strict majority", "lenient majority"], loc=4)
plt.xlabel("Number of annotators per image (chosen randomly)")
plt.ylabel("Fraction of images labeled correctly")
plt.title("Annotating Accuracy Using Different Methods")
plt.savefig("Diff-models-birds.png")