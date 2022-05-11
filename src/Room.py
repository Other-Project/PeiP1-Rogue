import random

from Coord import Coord


class Room:
    def __init__(self, c1, c2):
        """Instancie une salle d'extrémité haut/gauche c1 et bas/droite c2"""
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
        coins = lambda room: [room.c1, Coord(room.c2.x, room.c1.y), Coord(room.c1.x, room.c2.y), room.c2]  # Renvoi les coordonnées des 4 coins de room
        return any([coin in other for coin in coins(self)]) or any([coin in self for coin in coins(other)])

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
        import utils
        floor.put(self.randEmptyCoord(floor), utils.theGame().randEquipment())
        floor.put(self.randEmptyCoord(floor), utils.theGame().randMonster())
