import matplotlib.pyplot as plt
import random
import numpy as np


def transform1(x,y):
    x1=0.85*x + 0.4*y
    y1=-0.04*x + 0.85*y + 1.6
    return x1,y1

def transform2(x,y):
    x1=0.2 * x - 0.26 * y
    y1=0.23 * x + 0.22 * y + 1.6
    return x1, y1

def transform3(x, y):
    x1 = -0.15*x + 0.28*y
    y1 = 0.26*x + 0.24*y + 0.44
    return x1, y1

def transform4(x, y):
    x1 = 0
    y1 = 0.16*y
    return x1, y1

def transform(x, y):
    outcomes = [transform1, transform2, transform3, transform4]
    probabilities = [0.85, 0.07, 0.07, 0.01]
    sample = np.random.choice(outcomes, size=1, p=probabilities)[0]
    x1, y1 = sample(x, y)
    return x1, y1

xs, ys = [], []
x,y=0,0
points = 10000
for i in range(points):
    xs.append(x)
    ys.append(y)
    x, y = transform(x, y)
plt.plot(xs, ys, 'o')
plt.show()

