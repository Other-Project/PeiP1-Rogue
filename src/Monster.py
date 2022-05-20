from Creature import Creature


class Monster(Creature):
    from Map import Map

    def __init__(self, name, hp, abbrv=None, image=None, strength=1, range=0, color="\033[0;31m"):
        from Hero import Hero
        Creature.__init__(self, name, abbrv=abbrv, color=color, hp=hp, enemyType=Hero, strength=strength, image=image)
        self.range = range

    def doAction(self, floor: Map):
        import random

        floor.move(self, floor.pos(self).direction(floor.pos(floor.hero)))
        inRadius = floor.getAllCreaturesInRadius(self, self.range, self.enemyType)
        if len(inRadius) > 0:
            self.attack(random.choice(inRadius))
