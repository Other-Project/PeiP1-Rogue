from Creature import Creature


class Monster(Creature):
    def __init__(self, name, hp, abbrv=None, strength=1, color="\033[0;31m", image=None):
        from Hero import Hero
        Creature.__init__(self, name, abbrv=abbrv, color=color, hp=hp, enemyType=Hero, strength=strength, image=image)
