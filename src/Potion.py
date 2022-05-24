from Item import Item

class Potion(Item):
    from Hero import Hero

    def __init__(self, name: str, abbrv: str = None, usage=None, color="\033[0;33m", image=None, price=0):
        """
        :param name: The name of the potion
        :param abbrv: The symbol used to represent the potion on the map
        :param usage: The function called by the potion to do something
        :param price: The price to use the potion
        """
        Item.__init__(self, name, abbrv, usage, color, image)
        self.price = price

    def activate(self, creature: Hero):
        """ Use a potion or a power"""
        import utils

        if creature.mana < self.price:
            utils.theGame().addMessage("The " + self.name + " is not usable\nYou don't have enough magic point yet")
            return False
        if self.usage is not None:
            utils.theGame().addMessage("The " + creature.name + " uses the " + self.name)
            creature.mana -= self.price
            return self.usage(self, creature)
