from Monster import Monster


class Ghost(Monster):
    def __init__(self, name, hp=5, abbrv="G", image=None, strength=1):
        Monster.__init__(self, name, hp, abbrv=None, image=None, strength=1, radius=0, color="\033[0;31m")
        self.image = image

    def meet(self, attacker) -> bool:
        """Attacked by an enemy"""
        if not isinstance(attacker, self.enemyType):
            return False
        attacker.attack(self)
        return self.hp <= 0

    def attack(self, attacked):
        """Attacks an enemy"""
        import utils
        self.image = "assets/monsters/ghost.png"
        attacked.hp -= self.strength
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())
