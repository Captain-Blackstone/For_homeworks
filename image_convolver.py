import matplotlib.pyplot as plt
import numpy as np
from math import ceil, floor
import argparse
from pathlib import Path
import ast
import imageio


def convolve(image, kernel):
    if kernel.shape[0] != kernel.shape[1] or not kernel.shape % 2:
        print("Wrong kernel size! Exiting")
        return None
    n = kernel.shape[0]
    modified = np.zeros_like(image)
    border = ceil(n/2)
    p1 = floor(n / 2)
    p2 = border
    for row in range(border, image.shape[0]-border):
        for column in range(border, image.shape[1]-border):
            modified[row, column] = (image[row-p1:row+p2, column-p1:column+p2] * kernel).sum()
    mx = modified.max()
    if modified.min() < 0:
        for row in range(modified.shape[0]):
            for column in range(modified.shape[1]):
                y = modified[row][column]
                modified[row][column] = np.exp(y)/(1+np.exp(y))
    else:
        for row in range(modified.shape[0]):
            for column in range(modified.shape[1]):
                y = modified[row][column]
                modified[row][column] = y / mx
    print(modified)
    return modified

def parse_kernel_file(file):
    file = Path(file)
    with file.open("r") as fl:
        raw_kernel = fl.read()
    str_kernel = raw_kernel.replace("\n", " ")
    kernel = ast.literal_eval(str_kernel)
    kernel = np.array([np.array(element) for element in kernel])
    return kernel

def initiate_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--image",
                        required=True,
                        type=str,
                        help="Image you want to convolve")
    parser.add_argument("-k", "--kernel",
                        required=True,
                        type=str,
                        help="Name of file with a kernel. Kernel should be written in a form you would write in in python file - with square brackerts and commas. Newline characters are allowed.")
    args = parser.parse_args()
    image = plt.imread(args.image).mean(2)
    kernel = parse_kernel_file(args.kernel)
    print(kernel)
    image = convolve(image, kernel)
    if image is None:
        return None
    img_name = f"convolved_{args.image}"
    imageio.imwrite(img_name, image)
    print(f"Your image is saved as {img_name}")

initiate_parser()
