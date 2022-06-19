from Room import Room
from Coord import Coord


class RoomBoss(Room):
    """A room with a boss"""
    def __init__(self, c1: Coord, c2: Coord):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        from config import bosses
        import copy
        import random
        floor.put(self.center(), copy.copy(random.choice(bosses)))
