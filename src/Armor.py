from Equipment import Equipment


class Armor(Equipment):
    """An item than can be used to protect"""
    from Hero import Hero

    def __init__(self, name: str, resistance: int = 0, armorType=None, image=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param resistance: The resistance provided by the armor
        :param armorType: The type of armor
        """
        Equipment.__init__(self, name=name, image=image)
        self.resistance = resistance
        self.armorType = armorType

    def equip(self, hero: Hero):
        """Equip the armor"""
        equipped: Equipment = getattr(hero, self.armorType)
        if equipped is not None:
            equipped.deEquip(hero)
        setattr(hero, self.armorType, self)
        return True  # Removes the armor from the inventory

    def deEquip(self, hero: Hero):
        """De-equip the armor"""
        setattr(hero, self.armorType, None)  # Removes the armor from the equipped slot
        hero.inventory.append(self)  # Add the armor to the inventory

    def description(self) -> str:
        return "Bonus resistance: +" + str(self.resistance)
