from Element import Element


class Chest(Element):
    def __init__(self, name: str = 'Chest', image="assets/items/chest.png", contain: list = None, size=3):
        Element.__init__(self, name, image=image)
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
            utils.theGame().gui.retailerPopup(self, False)
        return False

    def takeItem(self, hero, element):
        hero.take(element)
        self.contain.remove(element)
        return True
