from Creature import Creature


class Hero(Creature):
    def __init__(self, name="Hero", hp=10, abbrv="@", strength=2, resistance=0, color="\033[0;32m"):
        Creature.__init__(self, name, hp, abbrv, strength, resistance, color)
        self.inventory = []
        self.armor = None
        self.weapon = None

    def description(self):
        return Creature.description(self) + str(self.inventory)

    def fullDescription(self):
        l = []
        for attr, val in self.__dict__.items():
            if not attr.startswith("_") and attr != "inventory":
                l.append("> " + attr + " : " + str(val))
        l.append("> INVENTORY : " + str([x.name for x in self.inventory]))
        return "\n".join(l)

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
