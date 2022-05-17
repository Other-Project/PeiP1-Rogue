from Creature import Creature


class Hero(Creature):
    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, color="\033[0;32m"):
        from Monster import Monster
        Creature.__init__(self, name, hp, Monster, abbrv, strength, color)
        self.inventory = []
        self.armor = None
        self.weapon = None
        self.exp, self.niv = 0, 0

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

    def attack(self, attacked):
        import utils

        attacked.hp -= self.strength
        if self.weapon is not None:
            attacked.hp -= self.weapon.damage
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

        if attacked.hp <= 0:
            self.exp += 1
            self.experience()

    def experience(self):
        if 0 <= self.niv <= 5:
            if self.exp == 5:  # si le joueur à 20exp alors il gagne 1hp et son exp est réinitialisée à 0
                self.hp += 1
                self.exp = 0
                self.niv += 1
        if 5 <= self.niv <= 15:
            if self.exp == 10:
                self.hp += 1
                self.exp = 0
                self.niv += 1
        if 15 <= self.niv <= 25:
            if self.exp == 20:
                self.hp += 1
                self.exp = 0
                self.niv += 1
        if 25 <= self.niv <= 50:
            if self.exp == 50:
                self.exp = 0
            self.niv += 1
        if 50 <= self.niv:
            if self.exp == 75:
                self.exp = 0
            self.niv += 1
