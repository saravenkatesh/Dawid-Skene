import matplotlib.pyplot as plt

f1 = open("coltruth.txt")
x = f1.readline()
truth = list(x)
f1.close()

accuracy = []
f2 = open("colannlabels.txt", 'r')
x = f2.readline()
while x != "":
    x = x.strip()
    labels = list(x)
    correct = 0.0
    total = 0
    for i, j in enumerate(labels):
        if j != '0':
            total += 1
            if j == truth[i]:
                correct += 1
    accuracy.append(correct/total)
    x = f2.readline()
    x = f2.readline()
f2.close()

num = []
f3 = open('numimages.txt', 'r')
x = f3.readline()
while x != "":
    x = x.strip()
    x = x.split()
    num.append(int(x[1]))
    x = f3.readline()
f3.close()

plt.scatter(num, accuracy)
plt.xlabel("Number of images annotated")
plt.ylabel("Accuracy")
plt.savefig("accuracy-vs-num-col.png")