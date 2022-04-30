import matplotlib.pyplot as plt
from perlin_noise import PerlinNoise
from random import choice
from Tile import *
from AStar import AStar

class Archipelago():
    def __init__(self, xpix, ypix):
        self.width = ypix
        self.height = xpix
        noise = PerlinNoise(octaves=int(xpix/50))
        self.tileArray = [[0 for i in range(xpix)] for j in range(ypix)]
        for x in range(xpix):
            for y in range(ypix):
                elevation = noise([x/xpix, y/ypix])
                if elevation < 0.06:
                    newTile = Sea(x, y, self.tileArray, elevation=elevation)
                elif elevation < 0.17:
                    newTile = Beach(x, y, self.tileArray)
                elif elevation < 0.33:
                    newTile = Forest(x, y, self.tileArray)
                else:
                    newTile = Mountain(x, y, self.tileArray)
                self.tileArray[y][x] = newTile

    def __generatePicture(self):
        picture = []
        for tileRow in self.tileArray:
            row = []
            for tile in tileRow:
                row.append(tile.color)
            picture.append(row)
        return picture

    def randBeach(self):
        borders = []
        for y in range(len(self.tileArray)):
            for x in range(len(self.tileArray[0])):
                current = self.tileArray[y][x]
                if type(current).__name__ == "Beach" and current.isWet():
                    borders.append(current)
        return choice(borders)

    def show(self):
        pic = self.__generatePicture()
        plt.imshow(pic)
        plt.show()

if __name__ == "__main__":
    # instantiate map object
    islandMap = Archipelago(300, 300)

    # set start and end to random beach tiles
    start = islandMap.randBeach()
    end = islandMap.randBeach()
    # ensure path will be interesting
    while start.distanceTo(end) < islandMap.width / 3:
        end = islandMap.randBeach()

    # run AStar algorithm to determine best path
    path = AStar(islandMap.tileArray).aStar(start, end)
    # draw path
    for tile in path:
        tile.setColor(255, 0, 0)
    islandMap.show()
