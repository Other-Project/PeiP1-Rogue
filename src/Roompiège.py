from Coord import Coord
from Room import Room
import utils


class RoomPiege(Room):

    def __init__(self, c1: Coord, c2: Coord, image="assets/grounds/cobble_blood12.png"):
        """
                :param c1: Point at the top left
                :param c2: Point at the bottom right
                """
        Room.__init__(self, c1=c1, c2=c2)
        self.image = image

    def decorate(self, floor, n=5):
        while len(floor.pieges) < n:
            co = self.randEmptyCoord(floor)
            if co not in floor.pieges:
                floor.pieges.append(co)




