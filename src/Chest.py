from Element import Element


class Chest(Element):
    def __init__(self, name: str = 'Chest', image="assets/items/chest.png", contain: list = None, size=3):
        import utils
        Element.__init__(self, name, image=image)
        self.size = size
        self.items = contain or [utils.theGame().randEquipment() for _ in range(self.size)]

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            if hero.key is True:
                utils.theGame().addMessage("You open the chest")
                utils.theGame().gui.chestPopup(self, False)
            else:
                utils.theGame().addMessage("You don't have the key.")
                utils.theGame().addMessage("Kill Monster to find the key")
        return False

    def takeItem(self, hero, element):
        hero.take(element)
        self.items.remove(element)
        return True
