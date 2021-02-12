import matplotlib.image as mpimg
import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
from math import log10

def PSNR(original, compressed):  # This function for calculating PSNR value
    mse = np.mean((original - compressed) ** 2)
    maxl = 255.0
    psnr = 10 * log10(maxl ** 2 / mse)
    return psnr

img = mpimg.imread("noisy.jpg")  # For reading the image
noisy = np.array(img, dtype=float)  # Convert to floating point

img = mpimg.imread("original.jpg")  # For reading the image
original = np.array(img, dtype=float)  # Convert to floating point

# We use constant mode with 0 because default value of median filter on matlab is zeros as padding option
result = ndimage.median_filter(noisy, size=3, mode='constant', cval=0)
result2 = ndimage.median_filter(result, size=3, mode='constant', cval=0)

plt.gray()
fig, axs = plt.subplots(2, 2)
axs[0, 0].imshow(original)
axs[0, 0].set_title("Original Image")
axs[0, 1].imshow(noisy)
axs[0, 1].set_title("Noisy Image")
axs[1, 0].imshow(result)
axs[1, 0].set_title("After first filter")
axs[1, 1].imshow(result2)
axs[1, 1].set_title("After second filter")
plt.show()


print("PSNR value between original and noisy image : ", end="")
print(round(PSNR(original, noisy), 2))
print("PSNR value between original and median filtered for once image: ", end="")
print(round(PSNR(original, result), 2))
print("PSNR value between original and median filtered for twice image: ", end="")
print(round(PSNR(original, result2), 2))


