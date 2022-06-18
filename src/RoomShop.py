from Room import Room
from Coord import Coord
from Equipment import Equipment
from Stairs import Stairs
from Chest import Chest
from Hero import Hero
import utils


class Marchand(Chest):
    def __init__(self, name: str = 'Marchand', image="assets/other/deep_elf_demonologist.png", contain: list = None, size: int = 3):
        Chest.__init__(self, name, image, contain, size)

        self.product = {}

    def sell(self,item, hero):
        if not isinstance(item, Equipment):
            raise TypeError("The item is not equipable")

        if isinstance(hero, Hero) and hero.gold > self.product[item]:
            hero.gold -= self.product[item]
            hero.inventory.append(item)
            utils.theGame().addMessage("You bought "+item.name)
        else:
            utils.theGame().addMessage("Not enough gold yet")


class RoomShop(Room):
    def __init__(self, c1=Coord(6, 6), c2=Coord(12, 12)):
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        utils.theGame().floor.put(Coord(5, 5), Marchand())
        utils.theGame().floor.put(Coord(13, 13), Stairs())


