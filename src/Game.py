import random
import pygame
from typing import List, Optional

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
        pygame.K_k: lambda hero: hero.__setattr__("hp", 0),
        pygame.K_r: lambda hero: theGame().floor.rest(hero),
        pygame.K_SPACE: lambda hero: True
    }

    def __init__(self, hero: Hero = None, level: int = 1, floor: Map = None, message: List[str] = None):
        from GUI import GUI
        self.newGame(hero, level, floor, message)
        self.gui = GUI(self)

    # noinspection PyAttributeOutsideInit
    def newGame(self, hero: Hero = None, level: int = 1, floor: Map = None, message: List[str] = None):
        from Hero import Hero
        self.hero = hero or Hero()
        self.level = level
        self.floor = floor
        self._message = message or []

    # noinspection PyAttributeOutsideInit
    def buildFloor(self):
        """Generates a new floor"""
        from Map import Map
        self.floor = Map(hero=self.hero, nbRooms=random.randint(3, 7))

    def addMessage(self, msg):
        """Adds a message to be print at the end of the turn"""
        self._message.append(msg)
        print("[New message]", msg)

    def readMessages(self, nbr=-1):
        """Gets `nbr` latest messages"""
        msgs = []
        for i in range(min(nbr, len(self._message))):
            msgs.append(self._message[(i + 1) * -1])
        return msgs

    def randElement(self, collection: {int: [Element]}) -> Optional[Element]:
        """
        Returns a random element from a dictionary depending on the game level
        :param collection: A dictionary where the key is the minimum game level and the value is a list of elements
        """
        import copy
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

    def play(self):
        """Main game loop"""
        import os
        self.buildFloor()
        os.system('cls' if os.name == 'nt' else 'clear')
        self.addMessage("--- Welcome Hero! ---")
        self.gui.main()

    def keyPressed(self, c: int):
        """
        A key has been pressed, perform the associated action
        :param c: The pygame id of the key
        """
        if c in Game._actions:
            self._message.clear()
            if Game._actions[c](self.hero):
                self.newTurn()

    def newTurn(self):
        """Performs a new turn"""
        from datetime import datetime
        import utils
        print("---", datetime.now().strftime("%H:%M:%S"), "New turn", "---")
        if self.hero.satiety > 0:
            self.hero.satiety -= 0.05  # 1 food every 20 actions
        else:
            self.hero.hp -= 0.2
        if self.hero.poisoned > 0:
            self.hero.hp -= 0.5
            self.hero.poisoned -= 1
            utils.theGame().addMessage("The hero is poisoned")
        if self.hero.invincible > 0:
            self.hero.invincible -= 1
            self.hero.poisoned = 0
            utils.theGame().addMessage("The hero is invincible")
        if self.hero.superStrength > 0:
            self.hero.strength += 4
            self.hero.superStrength -= 1
            utils.theGame().addMessage("The hero is stronger")
        self.floor.moveAllMonsters()
