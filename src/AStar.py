# This script is inspired by the C# code available here: https://web.archive.org/web/20170505034417/http://blog.two-cats.com/2014/06/a-star-example/


from Coord import Coord
from Map import Map
from enum import Enum

debug = False


class State(Enum):
    Untested = 0
    Open = 1
    Closed = -1


class Node:
    def __init__(self, floor: Map, location: Coord, parentNode=None):
        """
        :param floor: The map
        :param location: The location of this node
        :param parentNode: The previous node in this path. None for the starting node
        """

        self.floor = floor
        """The map"""
        self.location = location
        """Keep a record of this node’s location in order to calculate distance to other locations."""
        self.isWalkable = self.floor.get(self.location) != self.floor.empty
        """Boolean value indicating whether the node can be used."""
        self.state = State.Untested if self.isWalkable else State.Closed
        """Can be one of three states: not tested yet; open; closed."""
        self.parentNode = parentNode
        """The previous node in this path. Always None for the starting node."""

    def h(self, dest):
        """The straight-line distance from this node to the end node."""
        return self.location.distance(dest)

    def g(self):
        """The length of the path from the start node to this node."""
        return len(self.getPath())

    def f(self, dest):
        """Estimated total distance/cost."""
        return self.g() + self.h(dest)

    def getPath(self):
        path = []
        node = self
        while node.parentNode is not None and node.parentNode.location not in path:
            node = node.parentNode
            path.append(node.location)
        return path

    ways = [Coord(0, 1), Coord(0, -1), Coord(1, 0), Coord(-1, 0)]

    def getAdj(self):
        """Returns the coordinates of adjacent reachable cells"""
        return [self.location + way for way in self.ways]

    def __repr__(self):
        color = {State.Untested: "\033[1;33m", State.Closed: "\033[0;31m", State.Open: "\033[0;32m"}
        return color[self.state] + "{:3d}".format(int(self.g())) + "\033[0m"


class AStar:
    def __init__(self, floor: Map, startCoord: Coord):
        self.openList = []
        self.closeList = []
        self.floor = floor
        self.nodes = [[Node(self.floor, Coord(x, y)) for x in range(self.floor.size)] for y in range(self.floor.size)]
        self.nodes[startCoord.y][startCoord.x].state = State.Open
        self.startNode = self.nodes[startCoord.y][startCoord.x]

    def __repr__(self):
        return '\n'.join(
            ["    " + ' '.join(["{:^3d}".format(x) for x in range(self.floor.size)])] +
            ["{:^3d}".format(y) + ' '.join([str(self.nodes[y][x]) for x in range(len(self.nodes[y]))]) for y in range(len(self.nodes))]
        )

    def getAdjacentWalkableNodes(self, fromNode: Node, endNode):
        """Returns the accessible nodes from the current node"""
        walkableNodes = []

        for location in fromNode.getAdj():
            if location not in self.floor:
                continue

            node: Node = self.nodes[location.y][location.x]
            if not node.isWalkable:
                continue  # Ignore non-walkable nodes

            if node.state == State.Closed:
                continue  # Ignore already-closed nodes

            # Already-open nodes are only added to the list if their G-value is lower going via this route.
            if node.state == State.Open and fromNode.g() < node.g():
                node.parentNode = fromNode
                walkableNodes.append(node)
            elif node.state == State.Untested:
                # If it's untested, set the parent and flag it as 'Open' for consideration
                node.parentNode = fromNode
                node.state = State.Open
                walkableNodes.append(node)
            self.nodes[location.y][location.x] = node  # Update the node

            if debug:
                print(self)
                import time
                time.sleep(0.05)
                import os
                os.system('cls' if os.name == 'nt' else 'clear')

        return walkableNodes

    def search(self, currentNode: Node, endNode):
        """Finds a path from the currentNode to the destination point"""
        currentNode.State = State.Closed
        nextNodes = self.getAdjacentWalkableNodes(currentNode, endNode)
        nextNodes.sort(key=lambda x: x.f(endNode.location))
        for nextNode in nextNodes:
            if nextNode.location == endNode.location:
                return True
            elif self.search(nextNode, endNode):  # Recurses
                return True
        return False

    def findPath(self, destination):
        """Returns a list of coordinates leading to the destination point"""
        endNode = self.nodes[destination.y][destination.x]
        success = self.search(self.startNode, endNode)
        return endNode.getPath() if success else []
