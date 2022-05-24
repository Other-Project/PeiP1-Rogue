from typing import Callable

from Element import Element


class Item(Element):
    """An object that can be collected by the hero"""

    def __init__(self, name: str, abbrv: str = None, usage: Callable = None, color="\033[0;33m", image=None):
        """
        :param name: The name of the item
        :param abbrv: The symbol used to represent the item on the map
        :param color: The color of the item on the map
        :param usage: The function that will be called when the item is used by the hero
        """
        Element.__init__(self, name, abbrv, color, image)
        self.usage = usage

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
