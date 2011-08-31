import matplotlib.pyplot as plt
import numpy as np

ds = [.6943, .7497, .7634, .7705, .8162, .8168, .8627, .8625, .8938, .93]
maj = [.6971, .6205, .741, .714, .7284, .7284, .7504, .7395, .7493, .735]
lenient = [ .6971, .7903, .7542, .7713, .7667, .759, .897, .764, .7563, .765625]

p1, = plt.plot(ds)
p2, = plt.plot(maj)
p3, = plt.plot(lenient)
plt.legend([p1, p2, p3], ["D&S", "strict majority", "lenient majority"], loc=4)
plt.xlabel("Number of annotators per image (chosen randomly)")
plt.ylabel("Fraction of images labeled correctly")
plt.title("Annotating Accuracy Using Different Methods")
plt.savefig("Diff-models-col.png")