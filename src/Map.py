import random
from typing import Union, Optional, List
from RoomMonster import RoomMonster
import utils
from Coord import Coord
from Element import Element


class Map:
    from Creature import Creature

    ground = Element("ground")
    empty = None

    def __init__(self, size=20, hero=None, nbRooms=7, roomSpe=None):
        from Hero import Hero
        self.size = size
        self._roomsToReach, self._rooms = [], []
        self._mat = [[self.empty for _ in range(size)] for _ in range(size)]
        self.roomSpe = roomSpe
        if self.roomSpe is None:
            self.generateRooms(nbRooms)
        else:
            self.addRoom(self.roomSpe)
        self.reachAllRooms()
        self.position = self._rooms[0].center()
        self.hero = hero or Hero()
        self._elem = {}
        self.put(self.position, self.hero)
        self.visited = []
        for room in self._rooms:
            room.decorate(self)
        self.reposEffectue = False

    def __repr__(self):
        return '\n'.join([''.join([str(x) for x in y]) for y in self._mat]) + '\n'

    def __len__(self):
        return len(self._mat)

    def __contains__(self, item):
        if not isinstance(item, Coord):
            return item in self._elem
        return 0 <= item.x < self.size and 0 <= item.y < self.size

    def __getitem__(self, key):
        if isinstance(key, Coord):
            return self.get(key)
        return self.pos(key)

    def __delitem__(self, item):
        if isinstance(item, Coord):
            self.rm(item)
        self.rm(self.pos(item))

    # region Validation

    def _validCoord(self, c):
        return 0 <= c.x < self.size and 0 <= c.y < self.size

    def checkCoord(self, c):
        if not isinstance(c, Coord):
            raise TypeError('Not a Coord')
        if not self._validCoord(c):
            raise IndexError('Out of map coord')

    def checkElement(self, e):
        if not isinstance(e, Element):
            raise TypeError('Not a Element')

    # endregion

    # region Mat operations

    def get(self, c: Coord) -> Union[str, Element]:
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self, e: Element) -> Optional[Coord]:
        self.checkElement(e)
        return self._elem[e] if e in self._elem else None

    def put(self, c: Coord, e: Element):
        self.checkCoord(c)
        self.checkElement(e)
        if self._mat[c.y][c.x] != self.ground:
            raise ValueError('Incorrect cell')
        if e in self:
            raise KeyError('Already placed')
        self._mat[c.y][c.x] = e
        self._elem[e] = c

    def rm(self, c: Coord):
        self.checkCoord(c)
        e = self._mat[c.y][c.x]
        if e in self._elem:
            del self._elem[e]
            self._mat[c.y][c.x] = self.ground

    # endregion

    # region Rooms

    def getRoom(self, i: int):
        return self._rooms[i]

    def addRoom(self, room):
        self._roomsToReach.append(room)
        for y in range(room.c1.y, room.c2.y + 1):
            for x in range(room.c1.x, room.c2.x + 1):
                if self._validCoord(Coord(x, y)):
                    self._mat[y][x] = self.ground

    def findRoom(self, coord: Coord):
        for room in self._roomsToReach:
            if coord in room:
                return room
        return False

    def intersectNone(self, room):
        for r in self._roomsToReach:
            if r.intersect(room):
                return False
        return True

    def dig(self, coord: Coord):
        if self._validCoord(coord):
            self._mat[coord.y][coord.x] = self.ground
        room = self.findRoom(coord)
        if room:
            self._roomsToReach.remove(room)
            self._rooms.append(room)
        return room

    def corridor(self, start: Coord, end: Coord):
        coord = start
        while (start.y < end.y and coord.y < end.y) or (start.y > end.y and coord.y > end.y):
            coord += Coord(0, -1 if start.y > end.y else 1)
            self.dig(coord)
        while (start.x < end.x and coord.x < end.x) or (start.x > end.x and coord.x > end.x):
            coord += Coord(-1 if start.x > end.x else 1, 0)
            self.dig(coord)

    def reach(self):
        self.corridor(random.choice(self._rooms).center(), random.choice(self._roomsToReach).center())

    def reachAllRooms(self):
        if len(self._roomsToReach) == 0:
            return None
        self._rooms.append(self._roomsToReach[0])
        self._roomsToReach.pop(0)
        while len(self._roomsToReach) > 0:
            self.reach()

    def randRoom(self):
        from Room import Room
        c1 = Coord(random.randint(0, self.size - 3), random.randint(0, self.size - 3))
        l, h = random.randint(3, 8), random.randint(3, 8)
        return RoomMonster(c1, Coord(min(self.size - 1, c1.x + l), min(self.size - 1, c1.y + h)))

    def generateRooms(self, n):
        for i in range(0, n):
            room = self.randRoom()
            if self.intersectNone(room):
                self.addRoom(room)

    def randEmptyCoord(self):
        return random.choice(self._rooms).randEmptyCoord(self)

    # endregion

    # region Movements

    def move(self, e: Element, way: Coord) -> bool:
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        if orig is None:
            print("[Warning] Couldn't get position of", e)
            return False
        dest = orig + way
        if dest not in self:
            return False
        if self.get(dest) == Map.ground:
            self._mat[orig.y][orig.x] = Map.ground
            self._mat[dest.y][dest.x] = e
            self._elem[e] = dest
            return True
        elif self.get(dest) != Map.empty:
            if self.get(dest).meet(e) and self.get(dest) != self.hero:
                self.rm(dest)
            return True
        return False

    def getAllCreaturesInRadius(self, caller: Creature, radius: int, searchType: type = Creature) -> Optional[List[Creature]]:
        """
        Gets all creatures from a certain type in a specific radius

        :param caller: The center of the radius
        :param radius: The maximum distance from the caller
        :param searchType: The type that the creatures needs to match
        """
        creatures = []
        posCaller = self.pos(caller)
        if not posCaller:  # The hero isn't on the map
            return  # TODO: Need to investigate this
        for e, pos in self._elem.items():
            if e == caller or not isinstance(e, searchType) or not isinstance(pos, Coord):
                continue
            if pos.distance(posCaller) < radius:
                creatures.append(e)
        # noinspection PyTypeChecker
        return creatures

    def moveAllMonsters(self, radius: int = 6):
        """
        Moves the monsters of the map

        :param radius: The maximum distance from the hero in which to perform the movement
        """
        from Monster import Monster
        self.hero.doAction(self)
        for e in self.getAllCreaturesInRadius(self.hero, radius, Monster):
            if utils.theGame().hero.invisible <= 0:
                e.doAction(self)

    def rest(self, hero):
        """The hero recovers 5 hp and the monsters move 10 times"""

        from utils import theGame
        if self.reposEffectue:
            theGame().addMessage("The " + hero.name + " has already rested")
            return False
        theGame().addMessage("The " + hero.name + " is resting")
        hero.hp += 5
        for i in range(10):
            self.moveAllMonsters()
        self.reposEffectue = True
        return True

# endregion
