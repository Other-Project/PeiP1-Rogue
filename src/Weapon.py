from Equipment import Equipment


class Weapon(Equipment):
    """An item than can be used to attack"""
    from Hero import Hero
    from Creature import Creature

    def __init__(self, name: str, damage: int = 1, radiusDamage: int = 0, radius: int = 0, solidityMax=25, image=None, price=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param damage: The amount of damage that can be inflicted by using this weapon
        :param radius: The maximum distance at which the hero can attack
        """
        Equipment.__init__(self, name=name, image=image, solidityMax=solidityMax)
        self.damage = damage
        self.radius, self.radiusDamage = radius, radiusDamage
        self.price = price

    def equip(self, hero: Hero):
        """Equip the weapon"""
        if hero.weapon is not None:
            hero.weapon.deEquip(hero)
        hero.weapon = self
        return True  # Removes the weapon from the inventory

    def deEquip(self, hero, remove=False):
        """De-equip the armor"""
        hero.weapon = None  # Removes the weapon from the equipped slot
        if not remove:
            hero.inventory.append(self)  # Add the weapon to the inventory

    def description(self) -> str:
        txt = []
        if self.damage > 0:
            txt.append("Bonus strength: +" + str(self.damage))
        if self.radiusDamage > 0:
            txt.append("Range attack: " + str(self.radiusDamage))
        return " ; ".join(txt)

    def rangedAttack(self, creature: Creature):
        import utils
        creaturePos = utils.theGame().floor.pos(creature)
        if utils.theGame().floor.pos(utils.theGame().hero).distance(creaturePos) <= self.radius:
            self.solidity -= 1
            utils.theGame().hero.attack(creature, self.radiusDamage)
            if creature.hp <= 0:
                utils.theGame().floor.rm(creaturePos)
            utils.theGame().newTurn()
