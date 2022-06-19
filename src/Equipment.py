from Item import Item


class Equipment(Item):
    def __init__(self, name: str, image=None, solidityMax=10):
        """
        :param name: The name of the element
        :param image: The image of the element
        """
        Item.__init__(self, name=name, usage=lambda item, hero: self.equip(hero), image=image, price=None)
        self.solidityMax, self.solidity = solidityMax, solidityMax

    def equip(self, hero):
        raise NotImplementedError("Abstract method")

    def deEquip(self, hero, remove=False):
        raise NotImplementedError("Abstract method")

