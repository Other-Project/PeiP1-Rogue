from Element import Element


class Equipment(Element):
    def __init__(self, name, abbrv=None, usage=None, color="\033[0;33m"):
        Element.__init__(self, name, abbrv, color)
        self.usage = usage

    def meet(self, hero):
        import main
        from Hero import Hero
        if isinstance(hero, Hero):
            main.theGame().addMessage("You pick up a " + self.name)
            return hero.take(self)
        return None

    def use(self, creature):
        import main
        if self.usage is None:
            main.theGame().addMessage("The " + self.name + " is not usable")
            return False

        main.theGame().addMessage("The " + creature.name + " uses the " + self.name)
        return self.usage(self, creature)
