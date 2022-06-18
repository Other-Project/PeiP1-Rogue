from Room import Room
from Coord import Coord


class RoomChest(Room):
    def __init__(self, c1, c2):
        """
        :param name: The name of the special room
        :param c1, c2: extrémités haut/gauche c1 et bas/droite c2
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        from Chest import Chest
        floor.put(self.center(), Chest('Chest'))


