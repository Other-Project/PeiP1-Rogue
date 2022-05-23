from Equipment import Equipment
import utils


class Amulette(Equipment):
    from Hero import Hero
    def __init__(self, name: str, abbrv: str = None, image=None, type=None):
        Equipment.__init__(self, name=name, abbrv=abbrv, usage=self.equip, image=image)
        self.image = image
        self.type = type

    def equip(self, item, hero: Hero):
        """Equip the weapon"""
        if hero.amulette is not None:
            hero.inventory.append(hero.amulette)  # Add the old weapon to the inventory
        hero.amulette = item
        if self.type is "strength":
            utils.theGame().hero.strength += 2
        if self.type is "xp":
            utils.theGame().hero.xp += utils.theGame().hero.xp * 1.5
        return True  # Removes the weapon from the inventory
