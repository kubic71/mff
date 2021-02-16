import matplotlib.pyplot as plt

f = open("score", "r")
x = [float(n) for n in f.read().strip().split()]
plt.hist(x, bins = 15)
plt.show()
