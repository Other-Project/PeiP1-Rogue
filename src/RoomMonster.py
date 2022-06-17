from Room import Room
from Coord import Coord


class RoomMonster(Room):
    def __init__(self, c1: Coord, c2:Coord):
        Room.__init__(self, c1, c2)

    def decorate(self, floor):
        import utils
        floor.put(self.randEmptyCoord(floor), utils.theGame().randEquipment())
        floor.put(self.randEmptyCoord(floor), utils.theGame().randMonster())