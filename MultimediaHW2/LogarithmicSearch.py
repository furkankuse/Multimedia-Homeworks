import numpy as np
from math import log2


class LogarithmicSearch:

    def calcMae(self, blockSize, blockPoints, regionPoints):
        total = 0
        for x in range(blockSize):
            for y in range(blockSize):
                total += abs(
                    self._I1[int(regionPoints[0]) + x][int(regionPoints[1]) + y] - self._I2[blockPoints[0] + x][blockPoints[1] + y])

        return total / blockSize ** 2

    def logPoints(self, blockSize, regionSize,
                  regionTopLeftCorner):

        k = (regionSize / blockSize) / 4
        points = []
        for i in range(3):
            for j in range(3):
                points.append([(i + 1) * k * blockSize + regionTopLeftCorner[0] - blockSize / 2,
                            (j + 1) * k * blockSize + regionTopLeftCorner[1] - blockSize / 2])

        return points

    def regionStart(self, blockTopLeftCorner, blockSize, regionSize):
        points = []
        for i in range(2):
            if blockTopLeftCorner[i] - (regionSize - blockSize) / 2 < 0:
                points.append(0)
            elif blockTopLeftCorner[i] + (regionSize + blockSize) / 2 > len(self._I1):
                val = blockTopLeftCorner[i] - (regionSize - blockSize) / 2
                val += len(self._I1) - (blockTopLeftCorner[i] + (regionSize + blockSize) / 2)
                points.append(val)
            else:
                points.append(blockTopLeftCorner[i] - (regionSize - blockSize) / 2)

        return np.array(points)

    def start(self, blockSize, regionSize):
        vectors = []

        for i in range(int(len(self._I2) / blockSize)):
            vectorsRow = []
            for j in range(int(len(self._I2[0]) / blockSize)):
                regionPoints = self.regionStart([i * blockSize, j * blockSize], blockSize, regionSize)
                tempRegionSize = regionSize
                bestOne = [0, 0]
                bestMAE = 255 * blockSize * blockSize
                for k in range(int(log2(regionSize / blockSize))):
                    logPoints = self.logPoints(blockSize, tempRegionSize, regionPoints)
                    for p in range(len(logPoints)):
                        MAE = self.calcMae(blockSize, [i * blockSize, j * blockSize], logPoints[p])

                        if MAE < bestMAE:
                            bestMAE = MAE
                            bestOne = logPoints[p]

                    tempRegionSize /= 2

                vectorsRow.append([bestOne[0], bestOne[1], i * blockSize, j * blockSize])
            vectors.append(vectorsRow)

        return vectors

    def __init__(self, I1, I2):
        self._I1 = I1
        self._I2 = I2
