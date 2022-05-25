from Creature import Creature


class Monster(Creature):
    from Map import Map

    def __init__(self, name, hp, image=None, strength=1, radius=0, xpGain=1, movingSpeed=1):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param hp: The health of the monster
        :param strength: The strength of the monster
        :param radius: The attack radius of the monster
        :param strength: The strength of the monster
        :param xpGain: The quantity of XP that the hero will gain
        :param movingSpeed: The number of moves the monster can make in one turn
        """
        from Hero import Hero
        Creature.__init__(self, name, hp=hp, enemyType=Hero, strength=strength, image=image)
        self.range = radius
        self.xpGain = xpGain
        self.movingSpeed = movingSpeed

    def doAction(self, floor: Map):
        """Moves the monster and attacks the hero if he is in range"""
        import random
        from AStar import AStar

        astar = AStar(floor, floor.pos(self), floor.pos(floor.hero))
        path = astar.findPath()
        for i in range(self.movingSpeed):
            if len(path) > i:
                floor.move(self, floor.pos(self).direction(path[i]))

        inRadius = floor.getAllCreaturesInRadius(self, self.range, self.enemyType)
        if len(inRadius) > 0:
            self.attack(random.choice(inRadius))
