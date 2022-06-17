from Room import Room
from Chest import Chest
from utils import theGame
from Coord import Coord
from Stairs import Stairs


class RoomChest(Room):
    def __init__(self, c1=Coord(6, 6), c2=Coord(12, 12)):
        """
        :param name: The name of the special room
        :param c1, c2: extrémités haut/gauche c1 et bas/droite c2
        """
        Room.__init__(self, c1=c1, c2=c2)
        self.c1 = c1
        self.c2 = c2

    def decorate(self, floor):
        theGame().floor.put(Coord(9, 12), Chest('Chest'))
        theGame().floor.put(Coord(9, 6), Stairs())


