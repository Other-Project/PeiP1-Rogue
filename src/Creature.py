from Element import Element


class Creature(Element):
    def __init__(self, name, hp, enemyType, abbrv=None, strength=1, color=""):
        Element.__init__(self, name, abbrv, color)
        self.hp = hp
        self.strength = strength
        self.enemyType = enemyType

    def description(self):
        return Element.description(self) + "(" + str(max(self.hp, 0)) + ")"

    def meet(self, other) -> bool:
        import utils
        self.hp -= other.strength
        utils.theGame().addMessage("The " + other.name + " hits the " + self.description())
        return self.hp <= 0
