from Coord import Coord
from Room import Room


class RoomTrap(Room):
    def __init__(self, c1: Coord, c2: Coord):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor, n=5):
        while len(floor.traps) < n:
            co = self.randEmptyCoord(floor)
            if co not in floor.traps:
                floor.traps.append(co)
