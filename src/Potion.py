from Item import Item


class Potion(Item):
    from Hero import Hero

    def __init__(self, name: str, usage=None, image=None, price=0):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param usage: The function called by the potion to do something
        :param price: The price to use the potion
        """
        Item.__init__(self, name, usage, image)
        self.price = price

    def description(self) -> str:
        return "Mana usage: " + str(self.price)

    def activate(self, creature: Hero):
        """ Use a potion or a power"""
        import utils

        if creature.mana < self.price:
            utils.theGame().addMessage("The " + self.name + " is not usable, you don't have enough mana")
            return False
        if self.usage is None:
            return False

        utils.theGame().addMessage("The " + creature.name + " uses the " + self.name)
        creature.mana -= self.price
        result = self.usage(self, creature)
        utils.theGame().newTurn()
        return result
