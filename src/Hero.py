from Creature import Creature
import utils


class Hero(Creature):
    def __init__(self, name="Hero", image="assets/hero/frontHero.png", healthMax=10, manaMax=10, strength=2, satietyMax=10):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param healthMax: The initial health of the hero
        :param manaMax: The initial mana tank of the hero
        :param strength: The initial strength of the hero
        :param satietyMax: The maximum satiety value
        """
        from Monster import Monster
        Creature.__init__(self, name=name, hp=healthMax, enemyType=Monster, strength=strength, image=image)
        self.healthMax = healthMax
        self.satiety, self.satietyMax = satietyMax, satietyMax
        self.inventory, self.inventorySize = [], 10
        self.chestplate, self.shield, self.boots, self.legs, self.helmet = None, None, None, None, None
        self.weapon = None
        self.amulet = None
        self.xp, self.lvl, self.xpMultiplier = 0, 1, 1
        self.monstersKilled = 0
        self.mana, self.manaMax = manaMax, manaMax

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def fullDescription(self):
        attributes = []
        for attr, val in self.__dict__.items():
            if not attr.startswith("_") and attr != "inventory":
                attributes.append("> " + attr + " : " + str(val))
        attributes.append("> INVENTORY : " + str([x.name for x in self.inventory]))
        return "\n".join(attributes)

    def take(self, item):
        """Collects an item on the ground"""
        from Item import Item
        if not isinstance(item, Item):
            raise TypeError('Not a Equipment')
        return self.addInventory(item)

    def addInventory(self, item):
        if item.name == "manaPotion":
            if self.mana == self.manaMax:
                utils.theGame().addMessage("Your mana tank is full")
            else:
                return item.use(self)

        if len(self.inventory) >= self.inventorySize:
            utils.theGame().addMessage("Your inventory is full")
            return False
        if item in self.inventory:
            return False
        self.inventory.append(item)
        return True

    def use(self, item):
        """Uses an item"""
        from Item import Item
        from Potion import Potion

        if item is None:
            return
        if not isinstance(item, Item):
            raise TypeError("Not an equipment")
        if item not in self.inventory:
            raise ValueError("Not in the inventory")
        if isinstance(item, Potion):
            return item.activate(self)

        if item.use(self):
            self.inventory.remove(item)
            return

    def attack(self, attacked, speAttack=None):
        """Attacks a monster"""
        import utils

        if speAttack is not None:
            attacked.hp -= speAttack
        else:
            if attacked.image is not None:
                attacked.hp -= self.strength
            if self.weapon is not None:
                attacked.hp -= self.weapon.damage
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

        if attacked.hp <= 0:
            self.xp += attacked.xpGain * self.xpMultiplier
            self.monstersKilled += 1
            self.experience()

    def lvlSup(self):
        import math
        return int(30 * math.exp((self.lvl - 1) / 4))

    def experience(self):
        if self.xp >= self.lvlSup():
            self.xp -= self.lvlSup()
            self.lvl += 1
            self.healthMax += 1
            self.manaMax = min(self.manaMax + 5, 50)

    def resistance(self):
        from Armor import Armor
        armor: list[Armor] = [self.boots, self.legs, self.chestplate, self.helmet, self.shield]
        return sum([0 if equipment is None else equipment.resistance for equipment in armor])

    def strengthTot(self):
        return self.strength + (self.weapon.damage if self.weapon is not None else 0)
