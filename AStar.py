from Tile import *
from collections import deque

class AStar():
    """Based on https://github.com/vandersonmr/A_Star_Algorithm/blob/master/libs/python/AStar.py"""
    def __init__(self, tileArray, horizontalCost=10, diagonalCost=12):
        self.tileArray = tileArray
        self.horizontalCost = horizontalCost
        self.diagonalCost = diagonalCost

    def distBetween(self, current, neighbor):
        if current.x == neighbor.x or current.y == neighbor.y:
            cost = self.horizontalCost
        else:
            cost = self.diagonalCost
        # if type(current) == type(neighbor):
        #     cost /= 1.25

        return cost * neighbor.costMultiplier

    def heuristicEstimate(self, current, target):
        # using Diagonal distance
        dx = abs(current.x - target.x)
        dy = abs(current.y - target.y)
        return self.horizontalCost * (dx + dy) + (self.diagonalCost - 2 * self.horizontalCost) * min(dx, dy)

    def neighborNodes(self, current):
        """Returns a list of all 8 neighboring Tiles to the given Tile"""
        neighbors = []
        for i in range(current.y-1, current.y+2):
            for j in range(current.x-1, current.x+2):
                neighbor = self.tileArray[i][j]
                if not neighbor.isBorder and neighbor != current:
                    neighbors.append(neighbor)
        return neighbors

    def reconstructPath(self, parent, target):
        path = deque()
        node = target
        path.appendleft(node)
        while node in parent:
            node = parent[node]
            path.appendleft(node)
        return path

    def getLowest(self, openList, fScore):
        lowest = float("inf")
        lowestTile = None
        for node in openList:
            if fScore[node] < lowest:
                lowest = fScore[node]
                lowestTile = node
        return lowestTile

    def aStar(self, start, goal):
        openList, closedList = set([start]), set()
        gScore, fScore, parent = {}, {}, {}

        gScore[start] = 0
        fScore[start] = gScore[start] + self.heuristicEstimate(start, goal)
        
        while len(openList) != 0:
            current = self.getLowest(openList, fScore)

            if current == goal:
                return self.reconstructPath(parent, goal)
            
            openList.remove(current)
            closedList.add(current)

            for neighbor in self.neighborNodes(current):
                tentative_gScore = gScore[current] + self.distBetween(current, neighbor)

                if neighbor in closedList and tentative_gScore >= gScore[neighbor]:
                    continue

                if neighbor not in closedList or tentative_gScore < gScore[neighbor]:
                    parent[neighbor] = current
                    gScore[neighbor] = tentative_gScore
                    fScore[neighbor] = gScore[neighbor] + self.heuristicEstimate(neighbor, goal)

                    if neighbor not in openList:
                        openList.add(neighbor)
        
        return 0