from Element import Element


class Equipment(Element):
    def __init__(self, name, abbrv=None, usage=None, color="\033[0;33m"):
        Element.__init__(self, name, abbrv, color)
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
