from Element import Element


class Creature(Element):
    def __init__(self, name, hp, enemyType, strength=1, image=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param hp: The health of the monster
        :param enemyType: The type to attack
        :param strength: The strength of the monster
        """
        Element.__init__(self, name, image)
        self.hp = hp
        self.strength = strength
        self.enemyType = enemyType

    def description(self):
        return Element.description(self) + "(" + str(max(self.hp, 0)) + ")"

    def meet(self, attacker) -> bool:
        """Attacked by an enemy"""
        if not isinstance(attacker, self.enemyType):
            return False
        attacker.attack(self)
        return self.hp <= 0

    def attack(self, attacked):
        """Attacks an enemy"""
        import utils

        if attacked.chestplate is None:
            attacked.hp -= self.strength
        else:
            attacked.hp -= max(self.strength - attacked.chestplate.resistance, 1)
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

