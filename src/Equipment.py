from Item import Item


class Equipment(Item):
    def __init__(self, name: str, image=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        """
        Item.__init__(self, name=name, usage=lambda item, hero: self.equip(hero), image=image)

    def equip(self, hero):
        raise NotImplementedError("Abstract method")

    def deEquip(self, hero):
        raise NotImplementedError("Abstract method")

