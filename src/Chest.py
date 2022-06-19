from Element import Element
from    Item import Item


class Chest(Element):
    key = Item("Key", image="assets/items/key.png")

    def __init__(self, name: str = 'Chest', image="assets/items/chest.png", items: list = None, size=3):
        import utils
        Element.__init__(self, name, image=image)
        self.size = size
        self.items = items or [utils.theGame().randEquipment() for _ in range(self.size)]
        self.opened = False

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            if not self.opened:
                if self.key in hero.inventory:
                    utils.theGame().addMessage("You open the chest")
                    self.opened = True
                    hero.inventory.remove(self.key)
                else:
                    utils.theGame().addMessage("You don't have the key, kill monsters to find it")
            if self.opened:
                utils.theGame().gui.chestPopup(self, False)
        return False

    def takeItem(self, hero, element):
        import utils
        if len(hero.inventory)<hero.inventorySize:
            hero.take(element)
            self.items.remove(element)
        else:
            utils.theGame().addMessage("Your inventory is full")
        return True
