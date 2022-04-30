from math import sqrt

def rgb(r, g, b):
    """Converts given RGB 0-255 values to 0.0-1.0 and returns as a tuple"""
    return (r / 255.0, g / 255.0, b / 255.0)

class Tile():
    def __init__(self, x, y, colorTuple, tileArray):
        """Primarily acts as a superclass for further Sea, Beach, Forest, and Mountain Tiles"""
        self.x = x
        self.y = y
        self.color = colorTuple
        self.tileArray = tileArray
        lasty = len(self.tileArray) - 1
        lastx = len(self.tileArray[0]) - 1
        if x == 0 or y == 0 or x == lastx or y == lasty:
            self.isBorder = True
        else:
            self.isBorder = False
        self.costMultiplier = 1

    def setColor(self, r, g, b):
        self.color = rgb(r, g, b)

    def isWet(self):
        """Checks whether any of the 8 adjacent Tiles are a Sea Tile and returns a boolean"""
        if type(self).__name__ == "Sea":
            return True
        
        for i in range(self.y - 1, self.y + 2):
            for j in range(self.x - 1, self.x + 2):
                try:
                    if type(self.tileArray[i][j]).__name__ == "Sea":
                        return True
                except IndexError:
                    pass
        return False

    def getCoordinateTuple(self):
        return (self.x, self.y)  

    def distanceTo(self, target):
        dx = (self.x - target.x)**2
        dy = (self.y - target.y)**2
        return sqrt(dx + dy)

class Sea(Tile):
    def __init__(self, x, y, tileArray, elevation=0):
        super().__init__(x, y, rgb(96, 154, 163), tileArray)

class Beach(Tile):
    def __init__(self, x, y, tileArray):
        super().__init__(x, y, rgb(255, 250, 179), tileArray)
        self.costMultiplier = 2

class Forest(Tile):
    def __init__(self, x, y, tileArray):
        super().__init__(x, y, rgb(0, 140, 56), tileArray)
        self.costMultiplier = 3

class Mountain(Tile):
    def __init__(self, x, y, tileArray):
        super().__init__(x, y, rgb(160, 160, 160), tileArray)
        self.costMultiplier = 4
