# This script is inspired by the C# code available here: https://web.archive.org/web/20170505034417/http://blog.two-cats.com/2014/06/a-star-example/


from Coord import Coord
from Map import Map
from enum import Enum

# DEBUG MODE
debug = False
"""Prints the matrix state at each operation"""


class State(Enum):
    """The state of the node"""
    Unreachable = -1
    """The node isn't walkable"""
    Untested = 0
    """The node hasn't been tested"""
    Closed = 0.5
    """The node has been tested"""
    Open = 1
    """The node will be tested (has a direct connection with a closed one)"""


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
        self.state = State.Untested if self.floor.get(self.location) == self.floor.ground else State.Unreachable
        """The state of the node"""
        self.parentNode = parentNode
        """The previous node in this path. Always None for the starting node."""

    def h(self, dest):
        """The straight-line distance from this node to the end node."""
        return self.location.distance(dest)

    def g(self):
        """The length of the path from the start node to this node."""
        return len(self.getPath())

    def f(self, dest):
        """Estimated total distance/cost"""
        return self.g() + self.h(dest)

    def getPath(self):
        """Returns a list of coordinates leading to this node"""
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
        return "(" + str(self.location) + ", " + str(self.g()) + ")"


class AStar:
    def __init__(self, floor: Map, startCoord: Coord):
        self.openList = []
        self.closeList = []
        self.floor = floor
        self.nodes = [[Node(self.floor, Coord(x, y)) for x in range(self.floor.size)] for y in range(self.floor.size)]
        self.startNode = self.nodes[startCoord.y][startCoord.x]

    def __repr__(self):
        return self.getMatRepr()

    def getMatRepr(self, path=None):
        """Returns a representation of the current matrix with (optionally) a highlighted set of nodes"""
        path = path or []
        color = {State.Untested: "\033[0;37m", State.Unreachable: "\033[0;31m", State.Closed: "\033[1;33m", State.Open: "\033[0;32m", "Highlight": "\033[0;34m"}

        lines = ["     " + ' '.join(["{:^3d}".format(x) for x in range(self.floor.size)])]
        for y in range(len(self.nodes)):
            columns = ["{:^3d}".format(y)]
            for x in range(len(self.nodes[y])):
                node = self.nodes[y][x]
                columns.append(color["Highlight" if Coord(x, y) in path else node.state] + "{:3d}".format(int(node.g())) + "\033[0m")
            lines.append(' '.join(columns))
        return '\n'.join(lines)

    def getAdjacentWalkableNodes(self, fromNode: Node):
        """Returns the accessible nodes from the current node"""
        walkableNodes = []

        for location in fromNode.getAdj():
            if location not in self.floor:
                continue

            node: Node = self.nodes[location.y][location.x]
            if node.state == State.Closed or node.state == State.Unreachable:
                continue  # Ignore already-closed nodes and non-walkable nodes

            # Already-open nodes are only added to the list if their G-value is lower going via this route.
            if node.state == State.Open and (False if node.parentNode is None else fromNode.g() < node.parentNode.g()):
                node.parentNode = fromNode
                walkableNodes.append(node)
            elif node.state == State.Untested:
                # If it's untested, set the parent and flag it as 'Open' for consideration
                node.parentNode = fromNode
                node.state = State.Open
                walkableNodes.append(node)
            self.nodes[location.y][location.x] = node  # Update the node

        return walkableNodes

    def search(self, currentNode: Node, endNode):
        """Finds a path from the currentNode to the destination point"""
        currentNode.state = State.Closed
        nextNodes = list(set(filter(lambda node: node.state == State.Open, sum(self.nodes, []))).union(self.getAdjacentWalkableNodes(currentNode)))  # The opened/adjacent nodes (w/o duplicates)
        nextNodes.sort(key=lambda x: x.f(endNode.location))

        if debug:
            print(currentNode, nextNodes)
            print(self)

        for nextNode in nextNodes:
            nextNodes.remove(nextNode)
            if nextNode.location == endNode.location:
                return True
            elif self.search(nextNode, endNode):  # Recurses
                return True
        return False

    def findPath(self, destination):
        """Returns a list of coordinates leading to the destination point"""
        endNode = self.nodes[destination.y][destination.x]
        endNode.state = State.Untested
        success = self.search(self.startNode, endNode)
        return endNode.getPath() if success else []
