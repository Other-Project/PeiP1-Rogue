import utils
from Item import Item


class Chest(Item):
    def __init__(self, name: str='Chest', image="assets/items/chest.png", contain: list = None, size=3):
        Item.__init__(self, name, image=image)
        if contain is None:
            self.contain = [utils.theGame().randEquipment() for _ in range(size)]
        else:
            self.contain = contain

    def open(self):
        return ".\n".join(self.contain)




