import matplotlib.image as mpimg
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from math import log10


def plot(data, title):  # This function is for plot the image
    plt.imshow(data)
    plt.gray()
    plt.title(title)


def PSNR(original, compressed):  # This function for calculating PSNR value
    mse = np.mean((original - compressed) ** 2)
    maxl = 255.0
    psnr = 10 * log10(maxl ** 2 / mse)
    return psnr


img = mpimg.imread("Lena.gif")  # For reading the image
imgData = np.array(img, dtype=float)  # Convert to floating point

lowPass5x5filter = np.array([[1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
                             [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
                             [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
                             [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25],
                             [1 / 25, 1 / 25, 1 / 25, 1 / 25, 1 / 25]])

lowpass5x5 = ndimage.convolve(imgData, lowPass5x5filter, mode="nearest")
# If i use mode nearest, The input is extended by replicating the last pixel.

plot(lowpass5x5, 'Problem 2')
plt.show()

print(round(PSNR(imgData, lowpass5x5), 3))