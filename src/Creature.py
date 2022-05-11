from Element import Element


class Creature(Element):
    def __init__(self, name, hp, abbrv=None, strength=1, resistance=0, color="\033[0;31m"):
        Element.__init__(self, name, abbrv, color)
        self.hp = hp
        self.strength = strength
        self.resistance = resistance

    def description(self):
        return Element.description(self) + "(" + str(self.hp) + ")"

    def meet(self, other) -> bool:
        import utils
        self.hp -= other.strength
        utils.theGame().addMessage("The " + other.name + " hits the " + self.description())
        return self.hp <= 0
