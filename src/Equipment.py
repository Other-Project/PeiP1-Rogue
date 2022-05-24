from Item import Item


class Equipment(Item):
    def __init__(self, name: str, abbrv: str = None, color="\033[0;33m", image=None):
        """
        :param name: The name of the item
        :param abbrv: The symbol used to represent the item on the map
        :param color: The color of the item on the map
        :param usage: The function that will be called when the item is used by the hero
        """
        Item.__init__(self, name, abbrv, lambda item, hero: self.equip(hero), color, image)

    def equip(self, hero):
        raise NotImplementedError("Abstract method")

    def deEquip(self, hero):
        raise NotImplementedError("Abstract method")

