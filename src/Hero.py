from Creature import Creature


class Hero(Creature):
    def __init__(self, name="Hero", image="assets/hero/frontHero.png", hp=10, abbrv="@", strength=2, color="\033[0;32m", satietyMax=10, monstersKilled=0):
        from Monster import Monster
        Creature.__init__(self, name, hp, Monster, abbrv, strength, color, image)
        self.inventory = []
        self.armor = None
        self.weapon = None
        self.xp, self.level = 0, 0
        self.satietyMax = satietyMax
        self.satiety = satietyMax
        self.monstersKilled = monstersKilled

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def fullDescription(self):
        attributs = []
        for attr, val in self.__dict__.items():
            if not attr.startswith("_") and attr != "inventory":
                attributs.append("> " + attr + " : " + str(val))
        attributs.append("> INVENTORY : " + str([x.name for x in self.inventory]))
        return "\n".join(attributs)

    def take(self, item):
        """Collects an item on the ground"""
        from Equipment import Equipment
        if not isinstance(item, Equipment):
            raise TypeError('Not a Equipment')
        if item in self.inventory:
            return False
        self.inventory.append(item)
        return True

    def use(self, item):
        """Uses an item"""
        from Equipment import Equipment
        if item is None:
            return
        if not isinstance(item, Equipment):
            raise TypeError("Not an equipment")
        if item not in self.inventory:
            raise ValueError("Not in the inventory")
        if item.use(self):
            self.inventory.remove(item)

    def attack(self, attacked):
        """Attacks a monster"""
        import utils

        attacked.hp -= self.strength
        if self.weapon is not None:
            attacked.hp -= self.weapon.damage
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

        if attacked.hp <= 0:
            self.xp += 1
            self.experience()
            self.monstersKilled += 1

    def experience(self):
        if 0 <= self.level <= 5:
            if self.xp == 5:  # si le joueur à 20exp alors il gagne 1hp et son exp est réinitialisée à 0
                self.hp += 1
                self.xp = 0
                self.level += 1
        if 5 <= self.level <= 15:
            if self.xp == 10:
                self.hp += 1
                self.xp = 0
                self.level += 1
        if 15 <= self.level <= 25:
            if self.xp == 20:
                self.hp += 1
                self.xp = 0
                self.level += 1
        if 25 <= self.level <= 50:
            if self.xp == 50:
                self.xp = 0
            self.level += 1
        if 50 <= self.level:
            if self.xp == 75:
                self.xp = 0
            self.level += 1
