from Item import Item


class Armor(Item):
    """An item than can be used to protect"""
    from Hero import Hero
    from Creature import Creature
    from Map import Map

    def __init__(self, name: str, abbrv: str = None, resistance: int = 0, armorType=None, image=None):
        """
        :param name: The name of the item
        :param abbrv: The symbol used to represent the item on the map

        """
        Item.__init__(self, name=name, abbrv=abbrv, usage=self.equip, image=image)
        self.resistance = resistance
        self.armorType = armorType

    @staticmethod
    def equip(item: Item, hero: Hero):
        """Equip the armor"""
        if getattr(hero, item.armorType) is not None:
            hero.inventory.append(getattr(hero, item.armorType))  # Add the old armor to the inventory
        setattr(hero, item.armorType, item)
        return True  # Removes the armor from the inventory
