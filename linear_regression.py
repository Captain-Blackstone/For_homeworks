"""
I watched this video explaining linear regression algorithm:
https://www.youtube.com/watch?v=wYPUhge9w5c
And it encouraged me to actually code it. Which I did. And succedeed)
"""

import numpy as np
import matplotlib.pyplot as plt


def f(x, slope, intersect):
    """
    Just returns linear function of x with parameters k = slope, b = intersect
    :param x: x
    :param slope: k
    :param intersect: b
    :return: y
    """
    return slope*x + intersect


def Stochastic_gradient_descent(data, number_of_epochs, learning_rate, k, b):
    """
    Performs stochastic gradient descent. Just like in the video.
    :param data: tuple of 2 lists: xs and ys of points
    :param number_of_epochs: number of epochs =|
    :param learning_rate: learning rate =|
    :param k: initial k
    :param b: initial b
    :return: optimized k and b
    """
    xx = data[0]
    yy = data[1]
    k_s = []
    b_s = []
    for epoch in range(number_of_epochs):
        k_s.append(k)
        b_s.append(b)
        pos = np.random.choice(range(100))
        point = tuple((xx[pos], yy[pos]))
        regr_point = tuple((xx[pos], f(xx[pos], k, b)))
        x_dist = point[0]
        y_dist = point[1] - regr_point[1]
        k += x_dist * y_dist * learning_rate
        b += y_dist * learning_rate
        # plt.plot(xx, [f(x, k, b) for x in xx], color=str(1-epoch/number_of_epochs), zorder = -1)
    # plt.scatter(xx, yy, color="red", zorder=1)
    # plt.plot(xx, [f(x, k, b) for x in xx], color="blue", zorder=1)
    # plt.grid()
    # plt.show()
    plt.plot(range(number_of_epochs), k_s, label="k_stochastic")
    plt.plot(range(number_of_epochs), b_s, label="b_stochastic")
    return k, b


def dE_dk(k, b, xx, yy):
    n = len(xx)
    return (-2/n)*sum([xx[i]*(yy[i]-(k*xx[i]+b)) for i in range(len(xx))])


def dE_db(k, b, xx, yy):
    n = len(xx)
    return (-2/n)*sum([yy[i]-(k*xx[i]+b) for i in range(len(xx))])


def Gradient_descent(data, number_of_epochs, learning_rate, k, b):
    """
    Performs gradiend descent algorithm.
    :param data: tuple of 2 lists: xs and ys of points
    :param number_of_epochs: number of epochs =|
    :param learning_rate: learning rate =|
    :param k: initial k
    :param b: initial b
    :return: optimized k and b
    """
    xx = data[0]
    yy = data[1]
    k_s = []
    b_s = []
    for epoch in range(number_of_epochs):
        k_s.append(k)
        b_s.append(b)
        k -= learning_rate*dE_dk(k, b, xx, yy)
        b -= learning_rate*dE_db(k, b, xx, yy)
    plt.plot(range(number_of_epochs), k_s, label="k_normal")
    plt.plot(range(number_of_epochs), b_s, label="b_normal")
    return k, b


def main():
    # Now, let's do some linear regression!
    k_real = 4
    b_real = 7

    # generate data
    xx = list(np.random.uniform(-10, 10, 100))
    xx.sort()
    yy = [f(x, k_real, b_real) for x in xx]
    yy = [y + float(np.random.normal(0, 1)) for y in yy]

    # Set parameters
    number_of_epochs = 100000
    learning_rate = 0.0001

    # random initialization
    k_initial = float(np.random.uniform(-10, 10))
    b_initial = float(np.random.uniform(-10, 10))

    # Two ways of doing gradient descent
    k_stoch, b_stoch = Stochastic_gradient_descent((xx, yy), number_of_epochs, learning_rate, k_initial, b_initial)
    k_normal, b_normal = Gradient_descent((xx, yy), number_of_epochs, learning_rate, k_initial, b_initial)

    print(k_real, k_stoch, k_normal)
    print(b_real, b_stoch, b_normal)
    plt.legend()
    plt.grid()
    plt.show()

k_real = 4
b_real = 7
xx = list(np.random.uniform(-10, 10, 100))
xx.sort()
yy = [f(x, k_real, b_real) for x in xx]
yy = [y + float(np.random.normal(0, 1)) for y in yy]
X = np.array(xx)
Y = np.array(yy)
Y_pred = X*k_real + b_real
E = Y_pred-Y
print(np.mean(E**2))
# n = len(xx)
# return (-2/n)*sum([xx[i]*(yy[i]-(k*xx[i]+b)) for i in range(len(xx))])
