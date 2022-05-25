from Equipment import Equipment


class Weapon(Equipment):
    """An item than can be used to attack"""
    from Hero import Hero
    from Creature import Creature
    from Map import Map

    def __init__(self, name: str, damage: int = 1, radius: int = 0, image=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param damage: The amount of damage that can be inflicted by using this weapon
        :param radius: The maximum distance at which the hero can attack
        """
        Equipment.__init__(self, name=name, image=image)
        self.damage = damage
        self.radius = radius

    def equip(self, hero: Hero):
        """Equip the weapon"""
        if hero.weapon is not None:
            hero.weapon.deEquip(hero)
        hero.weapon = self
        return True  # Removes the weapon from the inventory

    def deEquip(self, hero):
        """De-equip the armor"""
        hero.weapon = None  # Removes the weapon from the equipped slot
        hero.inventory.append(self)  # Add the weapon to the inventory

    def attackInRadius(self, creature: Creature, floor: Map):
        """Attack all ennemies in radius"""
        for m in floor.getAllCreaturesInRadius(creature, self.radius + 1, creature.enemyType):
            if m.meet(creature):
                floor.rm(floor.pos(m))
