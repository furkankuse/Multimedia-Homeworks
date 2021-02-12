import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
from math import log10
from ExhaustiveSearch import MAEcalc
from ExhaustiveSearch import createBlock
from ExhaustiveSearch import ExhaustiveSearch
from LogarithmicSearch import LogarithmicSearch


def PSNR(original, compressed):  # This function for calculating PSNR value
    mse = np.mean((original - compressed) ** 2)
    maxl = 255.0
    psnr = 10 * log10(maxl ** 2 / mse)
    return psnr


def recreate(vectors, blockRow, blockColumn):  # For recreating images using backtrack vectors
    newI = np.zeros((len(I2), len(I2[0])))
    for i in range(len(vectors)):
        for j in range(len(vectors[0])):

            for x1 in range(blockRow):
                for y1 in range(blockColumn):
                    newI[i * blockRow + x1][j * blockColumn + y1] = I1[int(vectors[i][j][0]) + x1][int(vectors[i][j][1]) + y1]
    return newI

img = mpimg.imread("frame1.jpg")  # For reading the image
I1 = np.array(img, dtype=float)  # Convert to floating point

img = mpimg.imread("frame2.jpg")  # For reading the image
I2 = np.array(img, dtype=float)  # Convert to floating point


MAEval, vector = MAEcalc(32, 32, I1, createBlock([64, 80], I2, 32, 32))
print("Vector : ", end="")
vector = [vector, [64, 80]]
print(vector)
print("MAE value : ", end="")
print(round(MAEval, 2))

agent1 = ExhaustiveSearch(I1, I2)
vectors1 = agent1.blockedDFD(16, 16, 64, 64)
nI1 = recreate(vectors1, 16, 16)

agent2 = LogarithmicSearch(I1, I2)
vectors2 = agent2.start(16, 64)
nI2 = recreate(vectors2, 16, 16)


plt.gray()
fig, axs = plt.subplots(2, 2)
axs[0, 0].imshow(I1)
axs[0, 0].set_title("Frame 1")
axs[0, 1].imshow(I2)
axs[0, 1].set_title("Frame 2")
axs[1, 0].imshow(nI1)
axs[1, 0].set_title("From Exhaustive Search")
axs[1, 1].imshow(nI2)
axs[1, 1].set_title("From Logarithmic Search")
plt.show()

print("PSNR value of Exhaustive Search : ", end="")
print(round(PSNR(I2, nI1), 2))
print("PSNR value of Logarithmic Search : ", end="")
print(round(PSNR(I2, nI2), 2))