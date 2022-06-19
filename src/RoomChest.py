from Room import Room
from Coord import Coord


class RoomChest(Room):
    """A room with a chest"""
    def __init__(self, c1: Coord, c2: Coord):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        from Chest import Chest
        floor.put(self.center(), Chest('Chest'))


