import copy
import random

import pygame

from Coord import Coord
from Element import Element


def theGame():
    from utils import theGame
    return theGame()


class Game(object):
    from Hero import Hero
    from Map import Map

    _actions = {
        pygame.K_z: lambda hero: theGame().floor.move(hero, Coord(0, -1)),
        pygame.K_s: lambda hero: theGame().floor.move(hero, Coord(0, 1)),
        pygame.K_d: lambda hero: theGame().floor.move(hero, Coord(1, 0)),
        pygame.K_q: lambda hero: theGame().floor.move(hero, Coord(-1, 0)),
        pygame.K_i: lambda hero: theGame().addMessage(hero.fullDescription()),
        pygame.K_k: lambda hero: hero.__setattr__("hp", 0),
        pygame.K_u: lambda hero: hero.use(theGame().select(hero.inventory)),
        pygame.K_r: lambda hero: theGame().floor.rest(hero),
        pygame.K_SPACE: lambda hero: None
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
        # TODO: Fix this
        if len(items) <= 0:
            return None
        print("Choose item>", [str(i) + ": " + items[i].name for i in range(len(items))])
        entered = "0"  # No longer working
        if not entered.isdigit():
            return None

        n = int(entered)
        if 0 <= n < len(items):
            return items[n]
        return None

    def play(self):
        """Main game loop"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
        from GUI import GUI
        self.buildFloor()
        self.addMessage("--- Welcome Hero! ---")
        GUI(self).main()

    def newTurn(self, c):
        if c in Game._actions:
            Game._actions[c](self.hero)
            if self.hero.satiety > 0:
                self.hero.satiety -= 0.25
            else:
                self.hero.hp -= 1
            self.floor.moveAllMonsters()
