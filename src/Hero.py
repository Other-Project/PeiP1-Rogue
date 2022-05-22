from Creature import Creature


class Hero(Creature):
    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, color="\033[0;32m"):
        from Monster import Monster
        Creature.__init__(self, name, hp, Monster, abbrv, strength, color)
        self.inventory = []
        self.armor = None
        self.weapon = None
        self.niv = 0
        self.exp = 0
        self.mana = 0


    def description(self):
        return Creature.description(self) + str(self.inventory) + str(self.mana)

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
        if elem in self.inventory or len(self.inventory) == 12:
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
        gainmana = {1: ["Goblin", "Bat", "Archer"], 2: ["Ork", "Blob"] ,3: ["Dragon"]}

        attacked.hp -= self.strength
        if self.weapon is not None:
            attacked.hp -= self.weapon.damage
        utils.theGame().addMessage("The " + self.name + " hits the " + attacked.description())

        if attacked.hp <= 0:
            self.exp += 1
            self.experience()
            manaMax = self.jaugeMana()              #On recupère la valeur de la quantité maximale de points de magie (PM)
            for i in gainmana.keys():               #En fonction du monstre tué on récupère plus ou moins de PM
                if attacked.name in gainmana[i]:
                    if self.mana + i > manaMax:     #On bloque l'obtention de PM suplémentaires
                        self.mana = manaMax
                    else:
                        self.mana += i

        #Temporaire, à ajouter dans l'interface
        utils.theGame().addMessage("niveau mana : "+str(self.mana))
        utils.theGame().addMessage("niveau xp : " + str(self.exp))
        utils.theGame().addMessage("niveau niveau : " + str(self.niv))


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

    def jaugeMana(self):                #renvoie la quatité de PM que peut contenir la jauge
        lniv = [0, 5, 15, 25, 50]
        manamax =[3,5,10,15,20]
        for i in range(len(lniv)-1):
            if lniv[i] <= self.niv <= lniv[i+1]:
                return manamax[i]
            if self.niv > 50:
                return manamax[-1]


