"""
Hello, Sasha! Welcome to my 9-th homework. I'll make up an introduction while I do it. If you see that text, I
didn't come up with a nice one...
"""

import numpy as np
import time
import random
import matplotlib.pyplot as plt


def array_creation():
    """
    Creates 3 arrays in 3 different ways and prints them
    :return: None
    """
    array1 = np.array([1,2,3])
    lst = [1,2,3]
    array2 = np.array(lst)
    array3 = np.ones(3)
    print(array1, array2, array3)


def random_numpy_comparison():
    """
    Plots a graph of time consumed by numpy and ny random to generate x random numbers from standard normal distribution
    :return: None
    """
    random_time = []
    numpy_time = []
    for i in range(100):
        time1 = time.time()
        some_number = np.random.standard_normal(100)
        time2 = time.time()
        numpy_time.append(time2-time1)
        time1 = time.time()
        temp = []
        for j in range(i):
            some_number = random.normalvariate(0, 1)
            temp.append(some_number)
        time2 = time.time()
        random_time.append(time2-time1)
    plt.plot(range(100), random_time, color="red")
    plt.plot(range(100), numpy_time, color="blue")
    plt.show()


def random_walk():
    """
    Visualizes 2D random walk. Draws a trajectory.
    :return: None
    """
    x, y = 0, 0
    steps = [+1, -1]
    variables = ["x", "y"]
    xx = [0]
    yy = [0]
    for i in range(100):
        variable = np.random.choice(variables)
        step = np.random.choice(steps)
        if variable == "x":
            x += step
        else:
            y += step
        xx.append(x)
        yy.append(y)
    plt.plot(xx, yy)
    plt.show()


def Serpinsky_triangle(points=((100, 0), (0, 100), (-100, 0), (-50, -100), (50, -100))):
    """
    Draws Serpinsy triangle. You need to specify the points, on which triangle is built.
    :param points: a tuple(list) of tuples(lists) of point coordinates
    :return: None
    """
    xx = []
    yy = []
    x, y = 0, 0
    for i in range(100000):
        point = np.random.randint(0, len(points))
        x = (x+points[point][0])/2
        y = (y+points[point][1])/2
        xx.append(x)
        yy.append(y)
    plt.scatter(xx, yy, marker=".", s=0.05)
    plt.show()

def is_sorted(lst):
    """
    Determines whether the list is sorted or not
    :param lst: input list
    :return: True if list is sorted, else False
    """
    lst_sorted = True
    for i in range(len(lst) - 1):  # I feel like it could be written better with comprehensions. If so, tell me, please.
        if lst[i] > lst[i + 1]:
            lst_sorted = False
    return True if lst_sorted else False



def monkey_sort(lst):
    """
    Performs monkey sorting of a list
    :param lst: input list
    :return: number of shuffle events monkey sorting used
    """
    i = 0
    while not is_sorted(lst):
        np.random.shuffle(lst)
        i += 1
    return i

def monkey_sort_visualization():
    """
    Preforms monkey sorting of random lists of different lengths and draws a plot: x - number of elements in list, y -
    mean number of iterations monkey sorting needs to succeed. Error bars show standard error of mean.
    :return: None
    """
    xx = range(2, 9)
    yy_M = []
    yy_SE = []
    num_of_iterations = 100
    for i in range(2, 9): # for different list lengths
        print(i)
        speeds = []
        for _ in range(num_of_iterations): # we need to obtain some statistics
            lst = np.random.standard_normal(i)
            speeds.append(monkey_sort(lst))
        M = sum(speeds)/len(speeds) # mean
        SIGMA = np.sqrt(sum([(speed-M)**2 for speed in speeds])/len(speeds)) # standard deviation
        SE = SIGMA/np.sqrt(len(speeds)) # standard error of mean
        yy_M.append(M)
        yy_SE.append(SE)
    plt.errorbar(xx, yy_M, yy_SE)
    plt.show()


def Serpinsky_rectangle(points, num_of_iter, max_num_of_iter):
    ### This one doesn't work yet. Because I can't come up with an appropriate solution.
    def find_center_rectangle(points):
        p1_x = p3_x = (points[1][0] - points[0][0]) / 3 + points[0][0]
        p2_x = p4_x = (points[1][0] - points[0][0]) / 3 + 2 * points[0][0]
        p1_y = p2_y = (points[0][1] - points[3][1]) / 3 + 2 * points[3][1]
        p3_y = p4_y = (points[0][1] - points[3][1]) / 3 + points[3][1]
        return (p1_x, p1_y), (p2_x, p2_y), (p3_x, p3_y), (p4_x, p4_y)



def shaker(string):
    """
    This one takes a sentence as an input and returns it with all letters shuffled inside the words (only first and last
    letters remain on their positions)
    :param string: str - input sentence
    :return: shuffledd string
    """
    words = string.split()
    final = []
    for word in words:
        if len(word) < 4: # if the word consists of less than 4 letters, there's nothing to shuffle
            final.append(word)
            continue
        first = word[0]
        last = word[-1]
        word = list(word[1:-1])
        np.random.shuffle(word)
        word = first + "".join(word) + last
        final.append(word)
    return " ".join(final)


print(shaker("Напишите генератор, осуществляющий считывание фасты и возвращающий по 1-ой оттранслированной последовательности "))
# monkey_sort_visualization()
# array_creation()
# random_numpy_comparison()
# random_walk()
# Serpinsky_triangle()
