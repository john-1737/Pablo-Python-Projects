import matplotlib.pyplot as plt
import random

def transform1(x,y):
    x1=0.5*x
    y1=0.5*y
    return x1,y1

def transform2(x,y):
    x1=0.5*x + 0.5
    y1=0.5*y + 0.5    
    return x1, y1

def transform3(x, y):
    x1 = 0.5*x +1
    y1 = 0.5*y
    return x1, y1

def transform(x, y):
    sample=random.choice([transform1, transform2, transform3])
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

