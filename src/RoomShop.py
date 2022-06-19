from Coord import Coord
from Room import Room
from Chest import Chest


class Retailer(Chest):
    def __init__(self, name: str = 'Retailer', image="assets/other/retailer.png", contain: list = None, size: int = 3):
        Chest.__init__(self, name, image, contain, size)
        if contain is None:
            import utils
            self.contain = [utils.theGame().randEquipment() for _ in range(size)]
        else:
            self.contain = contain

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("You open the Chest")
            utils.theGame().gui.retailerPopup(self)
        return False

    def sell(self, item, hero):
        import utils
        if hero.gold >= item.price:
            hero.take(item)
            self.contain.remove(item)
            hero.gold -= item.price
            utils.theGame().addMessage("You bought " + item.name)
        else:
            utils.theGame().addMessage("Not enough gold yet")


class RoomShop(Room):
    from Coord import Coord
    """A room with a merchant"""
    def __init__(self, c1: Coord, c2: Coord):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        Room.__init__(self, c1=c1, c2=c2)

    def decorate(self, floor):
        floor.put(self.center(), Retailer())
