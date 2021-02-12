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

lowPass3x3filter = np.array([[1 / 9, 1 / 9, 1 / 9],
                             [1 / 9, 1 / 9, 1 / 9],
                             [1 / 9, 1 / 9, 1 / 9]])

lowpass3x3 = ndimage.convolve(imgData, lowPass3x3filter, mode="nearest")
# If i use mode nearest, The input is extended by replicating the last pixel.

plot(lowpass3x3, 'Problem1')
plt.show()

print(round(PSNR(imgData, lowpass3x3), 3))