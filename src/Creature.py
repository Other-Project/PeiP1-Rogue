from Element import Element


class Creature(Element):
    def __init__(self, name, hp, enemyType, abbrv=None, strength=1, color=""):
        Element.__init__(self, name, abbrv, color)
        self.hp = hp
        self.strength = strength
        self.enemyType = enemyType

    def description(self):
        return Element.description(self) + "(" + str(max(self.hp, 0)) + ")"

    def meet(self, attacker) -> bool:
        """Attacked by an enemy"""
        import utils
        if not isinstance(attacker, self.enemyType):
            return False
        self.hp -= attacker.strength
        utils.theGame().addMessage("The " + attacker.name + " hits the " + self.description())
        return self.hp <= 0
