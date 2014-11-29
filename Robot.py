__author__ = 'richy734'
from PriorityQueue import PriorityQueue
from Graph import Graph

'''
Class to represent the robots in the game.
Requires:
    path finding algorithm
    detection algorithm
    designated route
    alert status
'''


class Robot(object):
    def __init__(self):
        self.alertStatus = False
        self.position = [300, 300]


    def designatedRoute(self):
        if self.alertStatus == False:
            # follow default path
            print "default"
        else:
            # follow path finding alg
            print "new path"


    def heuristic(self, a, b):
        (x1, y1) = a
        (x2, y2) = b
        return abs(x1 - x2) + abs(y1 - y2)

    def a_star_search(self, graph, start, goal):
        frontier = PriorityQueue()
        frontier.put(start, 0)
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while not frontier.empty():
            current = frontier.get()

            if current == goal:
                break

            for next in graph.neighbors(current):
                new_cost = cost_so_far[current] + graph.cost(current, next)
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(goal, next)
                    frontier.put(next, priority)
                    came_from[next] = current

        return came_from, cost_so_far

    def findPath(self, player, map):
        levelGraph = Graph(map, 50)
        return self.a_star_search(levelGraph, self.position, player.position)
