from Element import Element

class Creature(Element):
    def __init__(self, name, hp, enemyType, abbrv=None, strength=1, color="", image=None):
        Element.__init__(self, name, abbrv, color, image)
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

        if attacked.armor is None:
            attacked.hp -= self.strength
        else:
            attacked.hp -= max(self.strength - attacked.armor.resistance, 1)
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

