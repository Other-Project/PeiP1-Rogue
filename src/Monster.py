from Creature import Creature


class Monster(Creature):
    from Map import Map

    def __init__(self, name, hp, abbrv=None, image=None, strength=1, radius=0, color="\033[0;31m"):
        from Hero import Hero
        Creature.__init__(self, name, abbrv=abbrv, color=color, hp=hp, enemyType=Hero, strength=strength, image=image)
        self.range = radius

    def doAction(self, floor: Map):
        """Moves the monster and attacks the hero if he is in range"""
        import random
        from AStar import AStar

        astar = AStar(floor, floor.pos(self), floor.pos(floor.hero))
        path = astar.findPath()
        if len(path) > 0:
            floor.move(self, floor.pos(self).direction(path[0]))

        inRadius = floor.getAllCreaturesInRadius(self, self.range, self.enemyType)
        if len(inRadius) > 0:
            self.attack(random.choice(inRadius))
