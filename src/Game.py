import copy
import random

from Coord import Coord
from Element import Element


def theGame():
    from utils import theGame
    return theGame()


class Game(object):
    from Hero import Hero
    from Map import Map

    _actions = {
        "z": lambda hero: theGame().floor.move(hero, Coord(0, -1)),
        "s": lambda hero: theGame().floor.move(hero, Coord(0, 1)),
        "d": lambda hero: theGame().floor.move(hero, Coord(1, 0)),
        "q": lambda hero: theGame().floor.move(hero, Coord(-1, 0)),
        "i": lambda hero: theGame().addMessage(hero.fullDescription()),
        "k": lambda hero: hero.__setattr__("hp", 0),
        "u": lambda hero: hero.use(theGame().select(hero.inventory)),
        "r": lambda hero: theGame().floor.rest(hero),
        " ": lambda hero: None
    }

    def __init__(self, hero: Hero = None, level: int = 1, floor: Map = None, message: [] = None):
        from Hero import Hero
        self.hero = hero or Hero()
        self.level = level
        self.floor = floor
        self._message = message or []

    def buildFloor(self):
        """Generates a new floor"""
        from Map import Map
        from Stairs import Stairs
        self.floor = Map(hero=self.hero)
        self.floor.put(self.floor.getRoom(-1).center(), Stairs())

    def addMessage(self, msg):
        """Adds a message to be print at the end of the turn"""
        self._message.append(msg)

    def readMessages(self):
        """Prints all the messages"""
        text = ".\n".join(self._message) + "." if len(self._message) > 0 else ""
        self._message.clear()
        return text

    def randElement(self, collection: {int: [Element]}) -> Element:
        """
        Returns a random element from a dictionary depending on the game level

        :param collection: A dictionary where the key is the minimum game level and the value is a list of elements
        """
        X = random.expovariate(1 / self.level)
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
        """Returns a random equipment"""
        import config
        return self.randElement(config.equipments)

    def randMonster(self):
        """Returns a random monster"""
        import config
        return self.randElement(config.monsters)

    def select(self, items):
        """Prompt the user to select an item from the list items"""
        import utils
        if len(items) <= 0:
            return None
        print("Choose item>", [str(i) + ": " + items[i].name for i in range(len(items))])
        entered = utils.getch()
        if not entered.isdigit():
            return None

        n = int(entered)
        if 0 <= n < len(items):
            return items[n]
        return None

    def play(self):
        """Main game loop"""
        import utils
        self.buildFloor()
        self.addMessage("--- Welcome Hero! ---")
        while self.hero.hp > 0:
            self.drawInterface()
            c = utils.getch()
            if c in Game._actions:
                Game._actions[c](self.hero)
                self.floor.moveAllMonsters()

        self.drawInterface()
        print("--- Game Over ---")

    def drawInterface(self):
        """draw the shell interface"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.floor)
        print("\033[0;31m♥\033[00m" * self.hero.hp)
        print("Inventory: " + ", ".join([str(e) for e in self.hero.inventory]))
        print(self.readMessages())
