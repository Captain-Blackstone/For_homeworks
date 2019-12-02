"""
I watched this video explaining linear regression algorithm:
https://www.youtube.com/watch?v=wYPUhge9w5c
And it encouraged me to actually code it. Which I did. And succedeed)
"""

import numpy as np
import matplotlib.pyplot as plt

f = lambda x, slope, intersect: slope*x + intersect

k_real = 4
b_real = 7
# generate data
xx = list(np.random.uniform(-10, 10, 100))
xx.sort()
yy = [f(x, k_real, b_real) for x in xx]
yy = [y + float(np.random.normal(0, 1)) for y in yy]

# Set parameters
number_of_epochs = 1000000
learning_rate = 0.0001

# random initialization
k = float(np.random.uniform(-10, 10))
b = float(np.random.uniform(-10, 10))
k_s = []
b_s = []

# Machine Learning happens
for epoch in range(number_of_epochs):
    k_s.append(k)
    b_s.append(b)
    pos = np.random.choice(range(100))
    point = tuple((xx[pos], yy[pos]))
    regr_point = tuple((xx[pos], f(xx[pos], k, b)))
    x_dist = point[0]
    y_dist = point[1] - regr_point[1]
    k += x_dist*y_dist*learning_rate
    b += y_dist*learning_rate
    # plt.plot(xx, [f(x, k, b) for x in xx], color=str(1-epoch/number_of_epochs), zorder = -1)


# plt.scatter(xx, yy, color="red", zorder=1)
# plt.plot(xx, [f(x, k, b) for x in xx], color="blue", zorder=1)
# plt.grid()
# plt.show()
print(k_real, k)
print(b_real, b)
plt.plot(range(number_of_epochs), k_s)
plt.plot([0, number_of_epochs], [k_real, k_real])
plt.grid()
plt.show()
plt.plot(range(number_of_epochs), b_s)
plt.plot([0, number_of_epochs], [b_real, b_real])
plt.grid()
plt.show()
