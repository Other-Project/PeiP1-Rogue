import utils
from Element import Element
from utils import theGame
from Weapon import Weapon
from Equipment import Equipment


class Chest(Element):
    def __init__(self, name: str='Chest', image = "assets/other/chest.png", contain: list = None, size = 3):
        Element.__init__(self, name, image = image)
        if contain is None:
            self.contain = [utils.theGame().randEquipment() for _ in range(size)]
        else:
            self.contain = contain





