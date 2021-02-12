import matplotlib.image as mpimg
import numpy as np
from scipy import ndimage
import matplotlib.pyplot as plt
from math import ceil, log10, floor

def plot(data, title):  # This function is for plot the image
    plt.imshow(data)
    plt.gray()
    plt.title(title)


def PSNR(original, compressed):  # This function for calculating PSNR value
    mse = np.mean((original - compressed) ** 2)
    maxl = 255.0
    psnr = 10 * log10(maxl ** 2 / mse)
    return psnr


def downSample(data):  # For taking the downs sample
    lenheight = ceil(len(data) / 2)
    lenwidth = ceil(len(data[0]) / 2)

    newSample = []
    for i in range(0, lenheight):
        newRow = []

        for j in range(0, lenwidth):
            newRow.append(data[i * 2][j * 2])
        newSample.append(newRow)
    return np.array(newSample)

def allZero(lenheight, lenwidth, data):
    # For creating All zero array  and, changing odd indexed values with values from down sampled array
    newSample = []
    for i in range(lenheight):
        newRow = []
        for j in range(lenwidth):
            if (i % 2 == 1) or (j % 2 == 1):
                newRow.append(0)
            else:
                newRow.append(data[floor((i + 1) / 2)][floor((j + 1) / 2)])

        newSample.append(newRow)
    return np.array(newSample)


img = mpimg.imread("original.jpg")  # For reading the image
imgData = np.array(img, dtype=float)  # Convert to floating point

lowPass3x3filter = np.array([[1 / 9, 1 / 9, 1 / 9],
                             [1 / 9, 1 / 9, 1 / 9],
                             [1 / 9, 1 / 9, 1 / 9]])

lowpass3x3 = ndimage.convolve(imgData, lowPass3x3filter, mode="nearest")
# If i use mode nearest, The input is extended by replicating the last pixel.


downSampled = downSample(lowpass3x3)

allZero = allZero(359, 479, downSampled)

newFilter = np.array([[.25, .5, .25],  # Filter for 5th part
                      [.5, 1, .5],
                      [.25, .5, .25]])

final = ndimage.convolve(allZero, newFilter, mode="constant", cval=0)
# I use constant mode and 0 value for it,
# becuase in matlab default mode of imfilter is constant value 0 for edges

plot(final, "Problem 3")
plt.show()
print(round(PSNR(imgData, final), 3))
############################
