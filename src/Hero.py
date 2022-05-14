from Creature import Creature
import pygame

class Hero(Creature):
    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, color="\033[0;32m", image=pygame.image.load("assets/hero equipment/sword/sword1.png")):
        from Monster import Monster
        Creature.__init__(self, name, hp, Monster, abbrv, strength, color, image)
        self.inventory = []
        self.armor = None
        self.weapon = None

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def fullDescription(self):
        attributs = []
        for attr, val in self.__dict__.items():
            if not attr.startswith("_") and attr != "inventory":
                attributs.append("> " + attr + " : " + str(val))
        attributs.append("> INVENTORY : " + str([x.name for x in self.inventory]))
        return "\n".join(attributs)

    def take(self, elem):
        from Equipment import Equipment
        if not isinstance(elem, Equipment):
            raise TypeError('Not a Equipment')
        if elem in self.inventory:
            return False
        self.inventory.append(elem)
        return True

    def use(self, item):
        from Equipment import Equipment
        if item is None:
            return
        if not isinstance(item, Equipment):
            raise TypeError("Not an equipment")
        if item not in self.inventory:
            raise ValueError("Not in the inventory")
        if item.use(self):
            self.inventory.remove(item)
