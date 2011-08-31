import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

x21 = [.8274, .8532, .87, .8802, .9, .921, .931, .94, .94781, .9528]
x22 = [.8528, .8494, .853, .857, .863, .867, .8688, .869, .871, .873]
x23 = [.8422, .8484, .8507, .8528, .86274, .87041, .8741, .87698, .883075]
x24 = [.6668, .6583, .6466, .66475, .67796, .6896, .693, .69535, .6977, .6984]

x31 = [.90101, .90105, .9045, .90815, .9089, .92734, .94317, .95623, .96396, .97]
x32 = [.9158, .9091, .9043, .91065, .91236, .91432, .91422, .91672, .918395, .91924]
x33 = [.8336, .8261, .8241, .8215, .82316, .82976, .84214, .85136, .8544, .859116]

xr1 = [.956, .9638, .9638, .9705, .9762, .9764, .9756, .9764]
xr2 = [.8854, .8888, .8924, .8975, .8982, .9061, .90571]
xr3 = [.9282, .9363, .9332, .9417, .9448, .944, .9448]

y2 = [5, 10, 15, 20, 50, 75, 100, 150, 200, 250]
y23 = [5, 10, 15, 20, 50, 100, 150, 200, 250]
y3 = [5, 10, 15, 20, 25, 50, 100, 150, 200, 250]
yr = [5, 10, 15, 20, 50, 100, 150]


fontP = FontProperties()
fontP.set_size('small')
p1, = plt.plot(y2, x21)
p2, = plt.plot(y2, x22)
p3, = plt.plot(y23, x23)
p4, = plt.plot(y2, x24)
p5, = plt.plot(y3, x31)
p6, = plt.plot(y3, x32)
p7, = plt.plot(y3, x33)
plt.xlabel("Number of images per annotator")
plt.ylabel("Percent labeled correctly by model")
plt.title("D&S performance using set matrices")
plt.legend([p1, p2, p3, p4, p5, p6, p7], ["Set 1", "Set 2", "Set 3",\
                                                       "Set 4", "Set 5", "Set 6",\
                                                       "Set 7"], 'center right', prop=fontP)
plt.savefig("num-imgs-set.png")
plt.show()