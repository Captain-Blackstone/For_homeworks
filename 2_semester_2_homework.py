"""Hello, Sasha!
Wow, seems like I need to learn a little python before starting this homework) I hope you don't mind if I'll do it
here. The homework itself starts a little bit further, you may scroll down."""

import numpy as np
import matplotlib.pyplot as plt


nums = np.arange(5, 15)
print(nums)
nums = nums.reshape(2, 5) # 2 raws, 5 columns
print("reshaped\n", nums)
nums = nums.reshape(5, 2) # 5 raws, 2 columns
print("reshaped again\n", nums)
nums = np.reshape(nums, (1, 10)) # 1 raw, 10 columns; another way to do the same thing
print("reshaped back\n", nums) # hm, interesting. It didn't reshape it back, actually. Now the array has two pairs of brackets
nums = np.reshape(nums, (2, 5))
nums1 = np.reshape(nums, (-1, 5)) # you can subtract dimentions.
# But you need to calculate the second number (5 in that case) anyways, so what's the point?

# About axes
print(nums)
n = nums.max(axis=0) # for raw
m = nums.max(axis=1) # for column
print(n, m) # WTF? The other way around?

# About out
empty_array = np.empty(nums.shape[1])
print("empty ", empty_array)
nums.max(axis=0, out=empty_array)
print("filled ", empty_array)

# About keepdims
n = nums.max(axis=0)
m = nums.max(axis=0, keepdims=True)
print("dimentions not keeped ", n)
print("dimentions keeped ", m) # Why would I need to keep dimentions?

# About different functions on arrays. Apart from min and max, though.

print("argmax ", nums.argmax(axis=1)) # same with argmin
print("var ", nums.var())
print("std ", nums.std())
print("std ", nums.std(ddof=1)) # if you want to estimate std of a population having a sample, you need to make ddof=1
# Number of observations is calcilated as N-ddof, 0 as default.

# About indexing

# Logical
xx = np.arange(20)
ligical_array = xx > 10
filtered = xx[ligical_array] # or xx[xx>5]
print(filtered)

# By index
print(xx[[0, -1]])
xx = np.arange(12).reshape(3,4)
print(xx)
print(xx[[0,1,2], [0,1,2]])

# Where - replace depending on the condition

modified = np.where(xx<5, "<5", ">=5")
print(modified)
print(np.where(xx<5)) # without condition - lists of indexes

# Concatenation of arrays

matrix1 = np.arange(5)
matrix2 = np.arange(5, 10)
print(matrix1)
print(matrix2)
concatenated = np.concatenate((matrix1, matrix2))
print(concatenated)
horizontally_stacked = np.hstack((matrix1, matrix2))
vertically_stacked = np.vstack((matrix1, matrix2))
deeply_stacked = np.dstack((matrix1, matrix2))
print("hstack ", horizontally_stacked)
print("vstack ", vertically_stacked)
print("dstack ", deeply_stacked)

# And now the pandas part begins
import pandas as pd

# Series
serie = pd.Series([1,2,3], index=["A", "B", "C"])
print(serie["A"], serie[0], serie.iloc[0], serie.loc["A"]) # Why would I need these fancy loc and iloc if i could just slice?
print(serie[::2])
print(serie[[1,2]])
print(serie[serie>2]) # Same as serie.loc[serie>2]
value_array = serie.values # array object
index_index = serie.index # index object
index_array = index_index.values
print(value_array)
print(index_index)
print(index_array)
print(value_array.sum(), serie.sum())

# Dataframes

# Creating from scratch
df = pd.DataFrame({"a":[1, 2, 3], "b": [101, 102, 103]})
print(df)

# Reading from file

df = pd.read_csv("https://github.com/Serfentum/bf_course/raw/master/14.pandas/train.csv")
# print(df.head())
# print(df.tail(3))
# print(df.values) # List of rows as arrays
print(df.shape, df.size)
# print(df.index) # Names of rows
# print(df.columns) # Names of columns
# col_types = df.dtypes # Series, indexes - column names, values - types
# print(col_types["pos"])
# print(df["pos"])
# print(df.pos)
# print(df[["pos", "matches"]])
# print(df.loc[12])
# print(df.iloc[1:10, 2:4])

""" HOMEWORK STARTS HERE """
""" (and is really short)"""

target_df = df[df.matches>sum(df.matches)/len(df.matches)][["pos", "reads_all", "mismatches", "deletions", "insertions"]]
# target_df.to_csv("train_part.csv")

def plot_bar():
    """
    Plots the histogram you requested.
    :return: None
    """
    df = pd.read_csv("https://github.com/Serfentum/bf_course/raw/master/14.pandas/train.csv")

    a = df.A.values
    t = df["T"].values
    g = df.G.values
    c = df.C.values

    N = df.shape[0]
    fig, ax = plt.subplots()
    ind = np.arange(0, 2*N, 2)
    width = 0.4
    ax.bar(ind, a, width, label="A")
    ax.bar(ind+width, t, width, label="T")
    ax.bar(ind+2*width, g, width, label="G")
    ax.bar(ind+3*width, c, width, label="C")
    ax.set_xticks(ind + 1.5*width)
    ax.set_xticklabels(df.pos.values)
    ax.tick_params(axis="x", labelsize=4, labelrotation=90)
    ax.legend()
    plt.show()
plot_bar()