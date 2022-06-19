from Chest import Chest


class Marchand(Chest):
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
            utils.theGame().gui.retailerPopup(self, True)
        return False

    def takeItem(self, hero, element):
        import utils
        if hero.gold >= element.price:
            hero.take(element)
            self.contain.remove(element)
            hero.gold -= element.price
            utils.theGame().addMessage("You bought " + element.name)
            return True
        else:
            utils.theGame().addMessage("Not enough gold yet")
            return False
