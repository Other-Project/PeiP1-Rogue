from Coord import Coord
from Room import Room


class RoomShop(Room):
    """A room with a merchant"""
    def __init__(self, c1: Coord, c2: Coord):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        from Merchant import Merchant
        floor.put(self.center(), Merchant())
