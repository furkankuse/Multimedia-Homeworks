import numpy as np


def createBlock(topLeftCorner, data, blockRow, blockColumn):
    block = []
    for i in range(blockRow):
        newColumn = []
        for j in range(blockColumn):
            newColumn.append(data[i + topLeftCorner[0]][j + topLeftCorner[1]])
        block.append(newColumn)
    return np.array(block)


def MAEcalc(blockRow, blockColumn, region, block):
    bestOne = [0, 0]
    bestMAE = 255 * blockColumn * blockRow
    for x1 in range(len(region) - blockRow):
        for y1 in range(len(region[0]) - blockColumn):
            total = 0
            for x2 in range(blockRow):
                for y2 in range(blockColumn):
                    total += abs(region[x1 + x2][y1 + y2] - block[x2][y2])

            total /= (blockRow * blockColumn)
            if total < bestMAE:
                bestOne = [x1, y1]
                bestMAE = total
    return bestMAE, bestOne


class ExhaustiveSearch:

    def regionStart(self, blockTopLeftCorner, blockRow, blockColumn, regionRow, regionColumn):
        if blockTopLeftCorner[0] - (regionRow - blockRow) / 2 < 0:
            x = 0
        else:
            x = blockTopLeftCorner[0] - (regionRow - blockRow) / 2

        if blockTopLeftCorner[1] - (regionColumn - blockColumn) / 2 < 0:
            y = 0
        else:
            y = blockTopLeftCorner[1] - (regionColumn - blockColumn) / 2
        return int(x), int(y)

    def regionLength(self, regionTopLeftCorner, blockTopLeftCorner, blockRow, blockColumn, regionRow, regionColumn):
        x = blockTopLeftCorner[0] - regionTopLeftCorner[0]
        y = blockTopLeftCorner[1] - regionTopLeftCorner[1]

        if blockTopLeftCorner[0] + blockRow + (regionRow - blockRow) / 2 > len(self._I1):
            x += len(self._I1) - blockTopLeftCorner[0]
        else:
            x += blockRow + (regionRow - blockRow) / 2

        if blockTopLeftCorner[1] + blockColumn + (regionColumn - blockColumn) / 2 > len(self._I1[0]):
            y += len(self._I1[0]) - blockTopLeftCorner[1]
        else:
            y += blockColumn + (regionColumn - blockColumn) / 2
        return int(x), int(y)

    def createRegion(self, blockTopLeftCorner, blockRow, blockColumn, regionRow, regionColumn, data):
        regionX, regionY = self.regionStart(blockTopLeftCorner, blockRow, blockColumn, regionRow, regionColumn)
        regionXLen, regionYLen = self.regionLength([regionX, regionY], blockTopLeftCorner, blockRow, blockColumn,
                                                   regionRow,
                                                   regionColumn)

        region = []
        for x1 in range(regionXLen):
            newColumn = []
            for y1 in range(regionYLen):
                newColumn.append(data[regionX + x1][regionY + y1])
            region.append(newColumn)

        return np.array(region), [regionX, regionY]

    def blockedDFD(self, blockRow, blockColumn, regionRow, regionColumn):
        vectors = []
        for i in range(int(len(self._I2) / blockRow)):
            vectorsRow = []
            for j in range(int(len(self._I2[0]) / blockColumn)):
                region = []
                # We are creating the block
                block = createBlock([i * blockRow, j * blockColumn], self._I2, blockRow, blockColumn)

                # We are creating the Research region

                region, regionAxis = self.createRegion([i * blockRow, j * blockColumn], blockRow, blockColumn,
                                                       regionRow,
                                                       regionColumn, self._I1)

                # For calculating MAE values
                bestMAE, bestOne = MAEcalc(blockRow, blockColumn, region, block)
                vectorsRow.append(
                    [bestOne[0] + regionAxis[0], bestOne[1] + regionAxis[1], i * blockRow, j * blockColumn])
            vectors.append(vectorsRow)
        return vectors

    def __init__(self, I1, I2):
        self._I1 = I1
        self._I2 = I2
