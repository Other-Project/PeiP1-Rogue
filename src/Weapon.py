from Equipment import Equipment


class Weapon(Equipment):
    """An item than can be used to attack"""
    from Hero import Hero
    from Creature import Creature
    from Map import Map

    def __init__(self, name: str, abbrv: str = None, damage: int = 1, radius: int = 0):
        """
        :param name: The name of the item
        :param abbrv: The symbol used to represent the item on the map
        :param damage: The amount of damage that can be inflicted by using this weapon
        :param radius: The maximum distance at which the hero can attack
        """
        Equipment.__init__(self, name=name, abbrv=abbrv, usage=self.equip)
        self.damage = damage
        self.radius = radius

    @staticmethod
    def equip(item: Equipment, hero: Hero):
        """Equip the weapon"""
        if hero.weapon is not None:
            hero.inventory.append(hero.weapon)  # Add the old weapon to the inventory
        hero.weapon = item
        return True  # Removes the weapon from the inventory

    def attackInRadius(self, creature: Creature, floor: Map):
        """Attack all ennemies in radius"""
        for m in floor.getAllCreaturesInRadius(creature, self.radius + 1, creature.enemyType):
            if m.meet(creature):
                floor.rm(floor.pos(m))
