import pygame.sprite
from typing import List, Optional

from Creature import Creature


class Hero(Creature):
    def __init__(self, name="Hero", image="assets/hero/hero.png", healthMax=10, manaMax=10, strength=10, satietyMax=10):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param healthMax: The initial health of the hero
        :param manaMax: The initial mana tank of the hero
        :param strength: The initial strength of the hero
        :param satietyMax: The maximum satiety value
        """
        from Monster import Monster
        from AStar import AStar
        Creature.__init__(self, name=name, hp=healthMax, enemyType=Monster, strength=strength, image=image, visibility=True)
        self.healthMax = healthMax
        self.satiety, self.satietyMax = satietyMax, satietyMax
        self.inventory, self.inventorySize = [], 10
        self.chestplate, self.shield, self.boots, self.legs, self.helmet = None, None, None, None, None
        self.weapon = None
        self.amulet = None
        self.xp, self.lvl, self.xpMultiplier = 0, 1, 1
        self.monstersKilled = 0
        self.mana, self.manaMax = manaMax, manaMax
        self.gold = 0
        self.astarTree: Optional[AStar] = None
        self.all_projectiles = pygame.sprite.Group()
        self.invisible = 0
        self.poisoned = 0
        self.invincible = 0
        self.superStrength = 0

    def getImage(self):
        if self.hp <= 0:
            return "assets/hero/grave.png"
        if self.poisoned > 0:
            return "assets/hero/heroPoisened.png"
        elif self.invincible > 0:
            return "assets/hero/heroInvincible.png"
        elif self.superStrength > 0:
            return "assets/hero/heroSuperStrength.png"
        elif self.invisible > 0:
            return "assets/hero/invisibleHero.png"
        return self.image

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def take(self, item):
        """Collects an item on the ground"""
        from Item import Item
        if not isinstance(item, Item):
            raise TypeError('Not a Equipment')
        elif item.name == 'gold':
            self.gold += 1
            return True
        return self.addInventory(item)

    def addInventory(self, item):
        import utils
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
        damage = 0
        self.invisible = 0  # The hero is no longer invisible
        if speAttack is not None:
            damage += speAttack
        elif attacked.visibility:
            damage += self.strength
            if self.weapon is not None and self.weapon.damage > 0:
                damage += self.weapon.damage
                self.weapon.solidity -= 1
                if self.weapon.solidity <= 0:
                    self.weapon = None
        Creature.attack(self, attacked, damage)

        import utils
        import Chest
        if attacked.hp <= 0:
            self.xp += attacked.xpGain * self.xpMultiplier
            self.monstersKilled += 1
            self.experience()
            if attacked.key is True:
                self.inventory.append(Chest.Chest().key)
                utils.theGame().addMessage("You found a chest key")
            else:
                utils.theGame().addMessage("This monster hadn't the key")

    def doAction(self, floor):
        from AStar import AStar
        import utils
        self.astarTree = AStar(floor, floor.pos(floor.hero))
        if utils.theGame().hero.invisible != 0:
            utils.theGame().hero.invisible -= 1
            print()
        else:
            utils.theGame().hero.image = "assets/hero/hero.png"

    def lvlSup(self):
        import math
        return int(30 * math.exp((self.lvl - 1) / 4))

    def experience(self):
        while self.xp >= self.lvlSup():
            self.xp -= self.lvlSup()
            self.lvl += 1
            self.healthMax = min(self.healthMax + 1, 20)
            self.manaMax = min(self.manaMax + 3, 20)

    def resistance(self):
        from Armor import Armor
        armor: List[Armor] = [self.boots, self.legs, self.chestplate, self.helmet, self.shield]
        return sum([0 if equipment is None else equipment.resistance for equipment in armor])

    def strengthTot(self):
        return self.strength + (self.weapon.damage if self.weapon is not None else 0)

    def rangeStrengthTot(self):
        return self.weapon.radiusDamage if self.weapon is not None else 0

    def equippedArmor(self):
        """returns equipped armor"""
        potentialArmor = [self.chestplate, self.shield, self.boots, self.legs, self.helmet]
        equippedArmor = []
        for armor in potentialArmor:
            if armor is not None:
                equippedArmor.append(armor)
        return equippedArmor
