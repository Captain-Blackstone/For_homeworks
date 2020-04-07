import numpy as np
import matplotlib.pyplot as plt
from collections.abc import Iterable
import dendropy as dp



def distance(p1, p2, datatype="points in space"):
    if datatype == "points in space":
        if not isinstance(p1, Iterable):
            p1 = np.array([p1, 0])
            p2 = np.array([p2, 0])
        else:
            p1 = np.array(p1)
            p2 = np.array(p2)
        return np.sqrt(sum((p1-p2)**2))


def clustering(data, datalabels=None, datatype="points in space"):
    if not datalabels:
        datalabels = list(range(len(data)))
    dist_matrix = np.zeros((len(data), len(data)))
    for i in range(len(data)):
        for j in range(len(data)):
            if i >= j:
                dist_matrix[i][j] = None
            else:
                dist_matrix[i][j] = distance(data[i], data[j], datatype)
    print(dist_matrix)
    print("-----")
    while len(datalabels) != 1:
        min_val = np.nanmin(dist_matrix)
        print(min_val)
        needed_point = np.argwhere(dist_matrix == min_val)
        i = needed_point[0][0]
        j = needed_point[0][1]
        print(i, j)
        new_point_label = f'({datalabels[i]},{datalabels[j]})'
        datalabels[i] = new_point_label
        datalabels.pop(j)
        new_dist_matrix = np.zeros([len(datalabels)+1, len(datalabels)+1])
        for x in range(dist_matrix.shape[0]):
            for y in range(dist_matrix.shape[1]):
                if j in (x, y):
                    continue
                if x == i:
                    new_dist_matrix[x][y] = (dist_matrix[i][y] + dist_matrix[i][y])/2
                elif y == i:
                    new_dist_matrix[x][y] = (dist_matrix[x][i] + dist_matrix[x][i])/2
                else:
                    new_dist_matrix[x][y] = dist_matrix[x][y]
        new_dist_matrix = np.delete(new_dist_matrix, j, 0)
        new_dist_matrix = np.delete(new_dist_matrix, j, 1)
        print(new_dist_matrix)
        print("----")
        dist_matrix = new_dist_matrix
    nwk=datalabels[0] + ";"
    tree = dp.Tree.get(data=nwk, schema="newick")
    tree.print_plot()


data = [[1, 2], [3, 5], [1, 3], [4, 5], [0, 0], [3, 1]]
xx = [el[0] for el in data]
yy = [el[1] for el in data]
clustering(data)



fig, ax = plt.subplots()
ax.scatter(xx, yy)
labels = list(range(len(data)))
for i, label in enumerate(labels):
    ax.annotate(label, (xx[i], yy[i]))
plt.grid()
plt.show()