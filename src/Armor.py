from Equipment import Equipment


class Armor(Equipment):
    """An item than can be used to protect"""
    from Hero import Hero
    from Creature import Creature
    from Map import Map

    def __init__(self, name: str, abbrv: str = None, resistance: int = 0, image=None):
        """
        :param name: The name of the item
        :param abbrv: The symbol used to represent the item on the map

        """
        Equipment.__init__(self, name=name, abbrv=abbrv, usage=self.equip, image=image)
        self.resistance = resistance

    @staticmethod
    def equip(item: Equipment, hero: Hero):
        """Equip the armor"""
        if hero.armor is not None:
            hero.inventory.append(hero.armor)  # Add the old armor to the inventory
        hero.armor = item
        return True  # Removes the armor from the inventory
