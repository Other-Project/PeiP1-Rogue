from Creature import Creature


class Monster(Creature):
    from Map import Map
    from Hero import Hero

    def __init__(self, name, hp, image=None, strength=1, radius=0, xpGain=1, movingSpeed=1, visibility=True, key = False):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param hp: The health of the monster
        :param strength: The strength of the monster
        :param radius: The attack radius of the monster
        :param strength: The strength of the monster
        :param xpGain: The quantity of XP that the hero will gain
        :param movingSpeed: The number of moves the monster can make in one turn
        :param key: a random monster have the key to open the chest
        """
        from Hero import Hero
        Creature.__init__(self, name, hp=hp, enemyType=Hero, strength=strength, image=image, visibility=visibility)
        self.range = radius
        self.xpGain = xpGain
        self.movingSpeed = movingSpeed
        self.hpMax = hp
        self.key = key

    def attack(self, attacked: Hero, damage=None):
        """Attacks the hero"""
        from Hero import Hero
        import random
        if attacked.invincible > 0:
            return True
        damage = damage or max(self.strength - attacked.resistance(), 1)
        Creature.attack(self, attacked, damage)

        if isinstance(attacked, Hero):
            equippedArmor = attacked.equippedArmor()
            if len(equippedArmor) > 0:
                attackedArmor = random.choice(equippedArmor)
                armorType = attackedArmor.armorType
                attackedArmor.solidity -= 1
                if attackedArmor.solidity <= 0:
                    attackedArmor = None
                setattr(attacked, armorType, attackedArmor)

    def doAction(self, floor: Map):
        """Moves the monster and attacks the hero if he is in range"""
        astar = floor.hero.astarTree
        if astar is None:
            return
        path = astar.findPath(floor.pos(self))
        for i in range(self.movingSpeed):
            if len(path) > i:
                floor.move(self, floor.pos(self).direction(path[i]))

        inRadius = floor.getAllCreaturesInRadius(self, self.range, self.enemyType)
        if len(inRadius) > 0:
            self.shootProjectile(floor.pos(inRadius[0]), onCollide=lambda coord: self.attack(inRadius[0]))
