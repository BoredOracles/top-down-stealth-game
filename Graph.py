__author__ = 'richy734'


class Graph(object):
    def __init__(self, map, squareSize):
        self.width = map.length / squareSize
        self.height = map.breadth / squareSize
        self.walls = map.walls
        self.weights = {}

    def inBounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x + 1, y), (x, y - 1), (x - 1, y), (x, y + 1)]
        if (x + y) % 2 == 0: results.reverse()
        results = filter(self.inBounds, results)
        results = filter(self.passable, results)
        return results

    def cost(self, a, b):
        return self.weights.get(b, 1)
