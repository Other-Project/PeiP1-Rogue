import utils
from Element import Element


class Chest(Element):
    def __init__(self, name: str='Chest', image = "assets/other/chest.png", contain: list = None, size = 3):
        Element.__init__(self, name, image = image)
        if contain is None:
            self.contain = [utils.theGame().randEquipment() for _ in range(size)]
        else:
            self.contain = contain

    def open(self):
        return ".\n".join(self.contain)




