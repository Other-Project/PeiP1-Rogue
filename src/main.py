import math
import random
import copy
import sys
from msvcrt import getch

"""
Rogue Five
"""


def heal(creature):
    creature.hp += 3
    return True


def teleport(creature, unique):
    map = theGame().floor
    newC = map.randEmptyCoord()
    c = map.pos(creature)
    map.rm(c)
    map.put(newC, creature)
    return unique


"""
Rogue Three
"""


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
        coins = lambda room: [room.c1, Coord(room.c2.x, room.c1.y), Coord(room.c1.x, room.c2.y),
                              room.c2]  # Renvoi les coordonnées des 4 coins de room
        return any([coin in other for coin in coins(self)]) or any([coin in self for coin in coins(other)])

    def randCoord(self):
        return Coord(random.randint(self.c1.x, self.c2.x), random.randint(self.c1.y, self.c2.y))

    def randEmptyCoord(self, map):
        centre = self.center()
        while True:
            c = self.randCoord()
            if c == centre or map.get(c) != map.ground:
                continue
            return c

    def decorate(self, map):
        map.put(self.randEmptyCoord(map), theGame().randEquipment())
        map.put(self.randEmptyCoord(map), theGame().randMonster())


"""
Rogue Two
"""


class Element:
    def __init__(self, name, abbrv=None, color=""):
        self.name = name
        self.abbrv = color + (abbrv or name[0]) + "\033[00m"

    def __repr__(self):
        return self.abbrv

    def description(self):
        return "<" + self.name + ">"

    def meet(self, hero):
        raise NotImplementedError("Not implemented yet")


class Equipment(Element):
    def __init__(self, name, abbrv=None, usage=None, color="\033[0;33m"):
        Element.__init__(self, name, abbrv, color)
        self.usage = usage

    def meet(self, hero):
        if isinstance(hero, Hero):
            theGame().addMessage("You pick up a " + self.name)
            return hero.take(self)
        return None

    def use(self, creature):
        if self.usage is None:
            theGame().addMessage("The " + self.name + " is not usable")
            return False

        theGame().addMessage("The " + creature.name + " uses the " + self.name)
        return self.usage(self, creature)


class Creature(Element):
    def __init__(self, name, hp, abbrv=None, strength=1, color="\033[0;31m"):
        Element.__init__(self, name, abbrv, color)
        self.hp = hp
        self.strength = strength

    def description(self):
        return Element.description(self) + "(" + str(self.hp) + ")"

    def meet(self, other):
        self.hp -= other.strength
        theGame().addMessage("The " + other.name + " hits the " + self.description())
        return self.hp <= 0


class Hero(Creature):
    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, color="\033[0;32m"):
        Creature.__init__(self, name, hp, abbrv, strength, color)
        self.inventory = []

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def take(self, elem):
        if not isinstance(elem, Equipment):
            raise TypeError('Not a Equipment')
        if elem in self.inventory:
            return False
        self.inventory.append(elem)
        return True

    def fullDescription(self):
        l = []
        for attr, val in self.__dict__.items():
            if not attr.startswith("_") and attr != "inventory":
                l.append("> " + attr + " : " + str(val))
        l.append("> INVENTORY : " + str([x.name for x in self.inventory]))
        return "\n".join(l)

    def use(self, item):
        if item is None:
            return
        if not isinstance(item, Equipment):
            raise TypeError("Not an equipment")
        if item not in self.inventory:
            raise ValueError("Not in the inventory")
        if item.use(self):
            self.inventory.remove(item)


"""
Rogue One
"""


class Coord:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "<" + str(self.x) + "," + str(self.y) + ">"

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):  # Division décimale
        return Coord(self.x / other, self.y / other)

    def __floordiv__(self, other):  # Quotient de la division euclidienne
        return Coord(self.x // other, self.y // other)

    def distance(self, other):
        return math.sqrt(math.pow(other.x - self.x, 2) + math.pow(other.y - self.y, 2))

    def norme(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def direction(self, other):
        if self == other:
            return Coord(0, 0)
        d = self - other
        cos = d.x / Coord(0, 0).distance(d)
        if cos > 1 / math.sqrt(2):
            return Coord(-1, 0)
        if cos < -1 / math.sqrt(2):
            return Coord(1, 0)
        return Coord(0, -1) if d.y > 0 else Coord(-0, 1)


class Map:
    ground = '\033[0;90m.\033[00m'
    empty = " "

    def __init__(self, size=20, hero=None, nbrooms=7):
        self.size = size
        self._roomsToReach, self._rooms = [], []
        self._mat = [[self.empty for x in range(size)] for y in range(size)]
        self.generateRooms(nbrooms)
        self.reachAllRooms()
        self.position = self._rooms[0].center()
        self.hero = hero or Hero()
        self._elem = {}
        self.put(self.position, self.hero)
        for room in self._rooms:
            room.decorate(self)

    def __repr__(self):
        return '\n'.join([''.join([str(x) for x in y]) for y in self._mat]) + '\n'

    def __len__(self):
        return len(self._mat)

    def __contains__(self, item):
        if not isinstance(item, Coord):
            for line in self._mat:
                if item in line:
                    return True
            return False
        return 0 <= item.x < self.size and 0 <= item.y < self.size

    def __getitem__(self, key):
        if isinstance(key, Coord):
            return self.get(key)
        return self.pos(key)

    def __delitem__(self, item):
        if isinstance(item, Coord):
            self.rm(item)
        self.rm(self.pos(item))

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

    def get(self, c):
        self.checkCoord(c)
        return self._mat[c.y][c.x]

    def pos(self, e):
        self.checkElement(e)
        return self._elem[e] if e in self._elem else False

    def put(self, c, e):
        self.checkCoord(c)
        self.checkElement(e)
        if self._mat[c.y][c.x] != self.ground:
            raise ValueError('Incorrect cell')
        if e in self:
            raise KeyError('Already placed')
        self._mat[c.y][c.x] = e
        self._elem[e] = c

    def rm(self, c):
        self.checkCoord(c)
        e = self._mat[c.y][c.x]
        if e in self._elem:
            del self._elem[e]
            self._mat[c.y][c.x] = self.ground

    def move(self, e, way):
        """Moves the element e in the direction way."""
        orig = self.pos(e)
        dest = orig + way
        if dest not in self:
            return
        if self.get(dest) == Map.ground:
            self._mat[orig.y][orig.x] = Map.ground
            self._mat[dest.y][dest.x] = e
            self._elem[e] = dest
        elif self.get(dest) != Map.empty and self.get(dest).meet(e) and self.get(dest) != self.hero:
            self.rm(dest)

    def addRoom(self, room):
        self._roomsToReach.append(room)
        for y in range(room.c1.y, room.c2.y + 1):
            for x in range(room.c1.x, room.c2.x + 1):
                if self._validCoord(Coord(x, y)):
                    self._mat[y][x] = self.ground

    def findRoom(self, coord):
        for room in self._roomsToReach:
            if coord in room:
                return room
        return False

    def intersectNone(self, room):
        for r in self._roomsToReach:
            if r.intersect(room):
                return False
        return True

    def dig(self, coord):
        if self._validCoord(coord):
            self._mat[coord.y][coord.x] = self.ground
        room = self.findRoom(coord)
        if room != False:
            self._roomsToReach.remove(room)
            self._rooms.append(room)
        return room

    def corridor(self, start, end):
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
        c1 = Coord(random.randint(0, self.size - 3), random.randint(0, self.size - 3))
        l, h = random.randint(3, 8), random.randint(3, 8)
        return Room(c1, Coord(min(self.size - 1, c1.x + l), min(self.size - 1, c1.y + h)))

    def generateRooms(self, n):
        for i in range(0, n):
            room = self.randRoom()
            if self.intersectNone(room):
                self.addRoom(room)

    def moveAllMonsters(self):
        for e, pos in self._elem.items():
            if e == self.hero or not isinstance(e, Creature) or not isinstance(pos, Coord):
                continue
            if pos.distance(self.pos(self.hero)) >= 6:
                continue
            self.move(e, pos.direction(self.pos(self.hero)))

    def randEmptyCoord(self):
        return random.choice(self._rooms).randEmptyCoord(self)


"""
Rogue Four
"""


class Game(object):
    equipments = {
        0: [Equipment("gold", "o"), Equipment("potion", "!", lambda item, hero: heal(hero))],
        1: [Equipment("sword"), Equipment("bow"), Equipment("potion", "!", lambda item, hero: teleport(hero, True))],
        2: [Equipment("chainmail")],
        3: [Equipment("portoloin", "w", lambda item, hero: teleport(hero, False))]
    }
    monsters = {
        0: [Creature("Goblin", 4), Creature("Bat", 2, "W")],
        1: [Creature("Ork", 6, strength=2), Creature("Blob", 10)],
        5: [Creature("Dragon", 20, strength=3)]
    }

    _actions = {
        "z": lambda hero: theGame().floor.move(hero, Coord(0, -1)),
        "s": lambda hero: theGame().floor.move(hero, Coord(0, 1)),
        "d": lambda hero: theGame().floor.move(hero, Coord(1, 0)),
        "q": lambda hero: theGame().floor.move(hero, Coord(-1, 0)),
        "i": lambda hero: theGame().addMessage(hero.fullDescription()),
        "k": lambda hero: hero.__setattr__("hp", 0),
        "u": lambda hero: hero.use(theGame().select(hero.inventory)),
        " ": lambda hero: None
    }

    def __init__(self, hero=None, level=1, floor=None, message=None):
        self.hero = hero or Hero()
        self._level = level
        self.floor = floor
        self._message = message or []

    def buildFloor(self):
        self.floor = Map(hero=self.hero)

    def addMessage(self, msg):
        self._message.append(msg)

    def readMessages(self):
        text = ". ".join(self._message) + "." if len(self._message) > 0 else ""
        self._message.clear()
        return text

    def randElement(self, collection):
        X = random.expovariate(1 / self._level)
        index = -1
        for x in collection:
            if x < X:
                index = x
            else:
                break
        if index == -1:
            return None
        return copy.copy(random.choice(collection[index]))

    def randEquipment(self):
        return self.randElement(self.equipments)

    def randMonster(self):
        return self.randElement(self.monsters)

    def select(self, items):
        if len(items) <= 0:
            return None
        print("Choose item>", [str(i) + ": " + items[i].name for i in range(len(items))])
        # noinspection PyUnresolvedReferences
        entered = getch()
        if not entered.isdigit():
            return None

        n = int(entered)
        if 0 <= n < len(items):
            return items[n]
        return None

    def play(self):
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self.hero.hp > 0:
            import os
            os.system("cls||clear")
            print(self.floor)
            print("❤" * self.hero.hp)
            print("Inventory: " + ", ".join([str(e) for e in self.hero.inventory]))
            print(self.readMessages())
            c = getch()
            if c == b'\x1b' or c == b'\x03':  # Escape or Ctrl + C
                print("Are you sure you want to quit the game ? [Y/N]")
                while True:
                    sure = getch()
                    sureStr = sure.upper().decode("utf-8", 'ignore')
                    if sureStr == "Y" or sure == b'\x03':
                        sys.exit()
                    elif sureStr == "N":
                        c = None  # To skip the turn
                        break
            decodedC = None if c is None else c.decode("utf-8", "ignore")
            if decodedC in Game._actions:
                Game._actions[decodedC](self.hero)
                self.floor.moveAllMonsters()
        print("--- Game Over ---")


def theGame(game=Game()):
    return game


theGame().play()
