# This script is inspired by the C# code available here: https://web.archive.org/web/20170505034417/http://blog.two-cats.com/2014/06/a-star-example/


from Coord import Coord
from Map import Map
from enum import Enum


class State(Enum):
    Untested = 0
    Open = 1
    Closed = -1


class Node:
    def __init__(self, floor: Map, location: Coord, h: int, g: int = 0, state: State = State.Untested, parentNode=None):
        """
        :param floor: The map
        :param location: The location of this node
        :param g: The length of the path from the start node to this node
        :param h: The straight-line distance from this node to the end node
        :param state: Can be one of three states: not tested yet; open; closed
        :param parentNode: The previous node in this path. None for the starting node
        """
        self.floor = floor
        self.location = location  # Keep a record of this node’s location in order to calculate distance to other locations.
        self.isWalkable = self.floor.get(self.location) != self.floor.empty  # Boolean value indicating whether the node can be used.
        self.g = g  # The length of the path from the start node to this node.
        self.h = h  # The straight-line distance from this node to the end node.
        self.f = self.g + self.h  # Estimated total distance/cost.
        self.state = state  # Can be one of three states: not tested yet; open; closed.
        self.parentNode = parentNode  # The previous node in this path. Always None for the starting node.

    ways = [Coord(0, 1), Coord(0, -1), Coord(1, 0), Coord(-1, 0)]

    def getAdj(self):
        """Returns the coordinates of adjacent reachable cells"""
        return [self.location + way for way in self.ways]

    def __repr__(self):
        return "<" + str(self.location) + ", state: " + str(self.state) + ", g: " + str(self.g) + ", h: " + str(self.h) + ">"


class AStar:
    def __init__(self, floor: Map, startCoord: Coord, endCoord: Coord, maxDist: int = 6):
        self.openList = []
        self.closeList = []
        self.floor = floor
        self.nodes = [[Node(self.floor, Coord(x, y), Coord(x, y).distance(endCoord)) for x in range(self.floor.size)] for y in range(self.floor.size)]
        self.startNode = self.nodes[startCoord.y][startCoord.x]
        self.endNode = self.nodes[endCoord.y][endCoord.x]
        self.maxDist = maxDist

    def getAdjacentWalkableNodes(self, fromNode: Node):
        walkableNodes = []

        for location in fromNode.getAdj():
            if location not in self.floor:
                continue

            node: Node = self.nodes[location.y][location.x]
            if not node.isWalkable:
                continue  # Ignore non-walkable nodes

            if node.state == State.Closed:
                continue  # Ignore already-closed nodes

            if node.h > self.maxDist:
                continue

            # Already-open nodes are only added to the list if their G-value is lower going via this route.
            if node.state == State.Open:
                gTemp = fromNode.g
                if gTemp < node.g:
                    node.parentNode = fromNode
                    walkableNodes.append(node)
            else:
                # If it's untested, set the parent and flag it as 'Open' for consideration
                node.parentNode = fromNode
                node.g = node.parentNode.g + 1
                node.state = State.Open
                walkableNodes.append(node)

        return walkableNodes

    def search(self, currentNode: Node):
        currentNode.State = State.Closed
        nextNodes = self.getAdjacentWalkableNodes(currentNode)
        nextNodes.sort(key=lambda x: x.f)
        for nextNode in nextNodes:
            if nextNode.location == self.endNode.location:
                return True
            elif self.search(nextNode):  # Note: Recurses back into search(Node)
                return True
        return False

    def findPath(self):
        path = []
        success = self.search(self.startNode)
        if success:
            node = self.endNode
            while node.parentNode is not None and node.parentNode.location not in path:
                path.append(node.location)
                node = node.parentNode
            path.reverse()
        return path
