import random
from Coord import Coord


class Room:
    def __init__(self, c1, c2):
        """
        :param c1: Point at the top left
        :param c2: Point at the bottom right
        """
        self.c1 = c1
        self.c2 = c2

    def __repr__(self):
        return "[" + str(self.c1) + ", " + str(self.c2) + "]"

    def __contains__(self, c):
        """Vérifie si une coordonnée c est comprise dans la salle"""
        return self.c1.x <= c.x <= self.c2.x and self.c1.y <= c.y <= self.c2.y

    def center(self):
        """Centre de la salle"""
        return (self.c1 + self.c2) // 2

    def intersect(self, other):
        """Vérifie si other chevauche la salle"""
        for x in range(self.c1.x, self.c2.x):
            for y in range(self.c1.y, self.c2.y):
                if Coord(x, y) in other:
                    return True
        return False

    def randCoord(self):
        return Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))

    def randEmptyCoord(self, floor):
        centre = self.center()
        while True:
            c = self.randCoord()
            if c == centre or floor.get(c) != floor.ground:
                continue
            return c

    def decorate(self, floor):
        raise NotImplementedError("Abstract Error")
