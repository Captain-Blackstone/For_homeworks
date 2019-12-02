"""
Hello, Sasha! Welcome to my 8th homework. Also check out my linear regression file - my first steps in machine learning)
"""
import numpy as np
import matplotlib.pyplot as plt
from Bio import SeqIO

def generate_data(k, b):
    """
    Generates not very random data, because it can be approximated with line with slope = k and intersect = b
    :param k: slope
    :param b: intersect
    :return: xs and ys of points of data
    """
    # These I will take from my linear regression file)
    f = lambda x, slope, intersect: slope * x + intersect
    xx = list(np.random.uniform(-10, 10, 100))
    xx.sort()
    yy = [f(x, k, b) for x in xx]
    yy = [y + float(np.random.normal(0, 1)) for y in yy]
    return xx, yy

def line_plot(k, b):
    """
    draws a line plot, which could be better approximated by line with slope = k and intersect = b
    :param k: slope
    :param b: intersect
    :return: None
    """
    xx, yy = generate_data(k, b)
    plt.plot(xx, yy)
    plt.grid()
    plt.show()

def length_distribution(path_fo_fasta):
    """
    Takes path to fasta file and draws distribution of record lengths in this file.
    :param path_fo_fasta: fasta file
    :return: None
    """
    fasta = SeqIO.parse(path_fo_fasta, "fasta")
    lengths = [len(record.seq) for record in fasta]
    print(len(lengths))
    plt.hist(lengths, 20)
    plt.show()

def my_favourite_graph():
    """
    Draws some random graph. Since I don't have a favourite one =|
    :return: None
    """
    xx, yy = generate_data(5, 10)
    graphs = ("plot", "hist", "scatter")
    graph = np.random.choice(graphs)
    if graph == "plot":
        plt.plot(xx, yy)
    elif graph == "scatter":
        plt.scatter(xx, yy)
    else:
        plt.hist(yy)
    plt.show()

line_plot(6, -1)
length_distribution("seqs.fasta")
my_favourite_graph()