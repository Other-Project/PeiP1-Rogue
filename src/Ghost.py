from Monster import Monster


class Ghost(Monster):
    def __init__(self, name, hp, xpGain=2, image=None, strength=1):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param hp: The health of the monster
        :param strength: The strength of the monster
        :param xpGain: The quantity of XP that the hero will gain
        """
        Monster.__init__(self, name, hp, image=None, strength=strength, radius=0, xpGain=xpGain, visibility=False)
        self.imageWhenVisible = image

    def meet(self, attacker) -> bool:
        """Attacked by an enemy"""
        if not isinstance(attacker, self.enemyType):
            return False
        self.visibility, self.image = True, self.imageWhenVisible
        attacker.attack(self)
        return self.hp <= 0

    def attack(self, attacked, damage=None):
        """Attacks an enemy"""
        from Creature import Creature
        self.visibility, self.image = True, self.imageWhenVisible
        Creature.attack(self, attacked, damage)
