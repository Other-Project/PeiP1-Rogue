from Monster import Monster


class Spider(Monster):
    def __init__(self, name, hp, image=None, strength=1, xpGain=1, movingSpeed=2):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param hp: The health of the monster
        :param strength: The strength of the monster
        :param xpGain: The quantity of XP that the hero will gain
        """
        Monster.__init__(self, name, hp, image=None, strength=strength, radius=0, xpGain=xpGain, visibility=True)
        self.image = image
        self.movingSpeed = movingSpeed

    def meet(self, attacker) -> bool:
        """Attacked by an enemy"""
        if not isinstance(attacker, self.enemyType):
            return False
        attacker.attack(self)
        return self.hp <= 0

    def attack(self, attacked, damage=None):
        """Attacks an enemy"""
        import utils
        from Creature import Creature
        Creature.attack(self, attacked, damage)
        utils.theGame().hero.poisoned = 4

