from Coord import Coord
import random
import copy


def theGame():
    import main
    return main.theGame()


class Game(object):

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
        from Hero import Hero
        self.hero = hero or Hero()
        self.level = level
        self.floor = floor
        self._message = message or []

    def buildFloor(self):
        from Map import Map
        from Stairs import Stairs
        self.floor = Map(hero=self.hero)
        self.floor.put(self.floor.getRoom(-1).center(), Stairs())

    def addMessage(self, msg):
        self._message.append(msg)

    def readMessages(self):
        text = ". ".join(self._message) + "." if len(self._message) > 0 else ""
        self._message.clear()
        return text

    def randElement(self, collection):
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
        import main
        return self.randElement(main.equipments)

    def randMonster(self):
        import main
        return self.randElement(main.monsters)

    def select(self, items):
        import main
        if len(items) <= 0:
            return None
        print("Choose item>", [str(i) + ": " + items[i].name for i in range(len(items))])
        entered = main.getch()
        if not entered.isdigit():
            return None

        n = int(entered)
        if 0 <= n < len(items):
            return items[n]
        return None

    def play(self):
        import main
        """Main game loop"""
        self.buildFloor()
        print("--- Welcome Hero! ---")
        while self.hero.hp > 0:
            import os
            os.system("cls||clear")
            print(self.floor)
            print("\033[0;31m♥\033[00m" * self.hero.hp)
            print("Inventory: " + ", ".join([str(e) for e in self.hero.inventory]))
            print(self.readMessages())
            c = main.getch()
            if c in Game._actions:
                Game._actions[c](self.hero)
                self.floor.moveAllMonsters()
        print("--- Game Over ---")
