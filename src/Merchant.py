from Chest import Chest


class Merchant(Chest):
    def __init__(self, name: str = 'Retailer', image="assets/other/retailer.png", items: list = None, size: int = 3):
        Chest.__init__(self, name, image, items, size)

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("You start to trade")
            utils.theGame().gui.chestPopup(self, True)
        return False

    def takeItem(self, hero, element):
        import utils
        if hero.gold >= element.price:
            if len(hero.inventory) < hero.inventorySize:
                hero.take(element)
                self.items.remove(element)
                hero.gold -= element.price
                utils.theGame().addMessage("You bought " + element.name)
                return True
        else:
            utils.theGame().addMessage("Not enough gold yet")
            return False
        utils.theGame().addMessage("Your inventory is full")
        return False
