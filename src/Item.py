from typing import Callable
from Element import Element


class Item(Element):
    """An object that can be collected by the hero"""

    def __init__(self, name: str, usage: Callable = None, image=None, desc="", price=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        :param usage: The function that will be called when the item is used by the hero
        """
        Element.__init__(self, name=name, image=image)
        self.usage = usage
        self.desc = desc
        self.price = price

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("You pick up a " + self.name)
            return hero.take(self)
        return None

    def use(self, creature):
        import utils
        if self.usage is None:
            utils.theGame().addMessage("The " + self.name + " is not usable")
            return False

        utils.theGame().addMessage("The " + creature.name + " uses the " + self.name)
        return self.usage(self, creature)

    def description(self) -> str:
        return self.desc
