"""Todays machine learning lesson inspired me to code this algorithm. Here it is =)"""
import numpy as np
import math
import matplotlib.pyplot as plt


def distance(point1, point2):
    l = math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)
    return l

def kmeans(datapoints, number_of_clusters):
    dataxx = [point[0] for point in datapoints]
    datayy = [point[1] for point in datapoints]
    xx = np.random.uniform(low=min(dataxx), high=max(dataxx), size=number_of_clusters)
    yy = np.random.uniform(low=min(datayy), high=max(datayy), size=number_of_clusters)
    centers = [tuple((xx[i], yy[i])) for i in range(number_of_clusters)]
    Npoints = len(datapoints)
    delta = 0.002
    while delta > 0.001:
        distances = tuple((tuple((distance(point, center) for center in centers)) for point in datapoints))
        closest = tuple(tuple((element.index(min(element))) for element in distances))
        deltas = []
        for i in range(len(centers)):
            indexes = []
            for index, element in enumerate(closest):
                if element == i:
                    indexes.append(index)
            center_points = [point for point in datapoints if datapoints.index(point) in indexes]
            pointsxx = [point[0] for point in center_points]
            pointsyy = [point[1] for point in center_points]
            new_x = sum(pointsxx)/len(pointsxx)
            new_y = sum(pointsyy)/len(pointsyy)
            deltas.append(distance(centers[i], [new_x, new_y]))
            centers[i] = (new_x, new_y)
        delta = max(deltas)
        print(centers)
        plt.scatter(dataxx, datayy, c=closest)
        plt.scatter([center[0] for center in centers], [center[1] for center in centers], marker="*", s=100,  c=range(len(centers)),)
        print(delta)
        plt.show()
    plt.scatter(dataxx, datayy, c=closest)
    plt.scatter([center[0] for center in centers], [center[1] for center in centers], marker="*", s=100,
                c=range(len(centers)), )
    plt.title("Final")
    print(delta)
    plt.show()


points = [(np.random.uniform(low=-10, high=-5), np.random.uniform(low =-10, high=-5)) for _ in range(100)]
points += [(np.random.uniform(low=0, high=5), np.random.uniform(low = 5, high=10)) for _ in range(100)]
points += [(np.random.uniform(low= 5, high=10), np.random.uniform(low =0, high=5)) for _ in range(100)]

print(points)

kmeans(points, 3)