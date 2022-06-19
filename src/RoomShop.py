from Room import Room
from Coord import Coord
from Chest import Chest


class Marchand(Chest):
    def __init__(self, name: str = 'Marchand', image="assets/other/deep_elf_demonologist.png", contain: list = None, size: int = 3):
        Chest.__init__(self, name, image, contain, size)

        self.product = {}

    def sell(self,item, hero):
        import utils
        from Hero import Hero
        from Equipment import Equipment

        if not isinstance(item, Equipment):
            raise TypeError("The item is not equipable")

        if isinstance(hero, Hero) and hero.gold > self.product[item]:
            hero.gold -= self.product[item]
            hero.inventory.append(item)
            utils.theGame().addMessage("You bought "+item.name)
        else:
            utils.theGame().addMessage("Not enough gold yet")


class RoomShop(Room):
    """A room with a merchant"""
    def __init__(self, c1: Coord, c2: Coord):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        floor.put(self.center(), Marchand())
