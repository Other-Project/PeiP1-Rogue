from Element import Element


class Stairs(Element):
    def __init__(self, name="Stairs", abbrv="E", color=""):
        Element.__init__(self, name, abbrv, color)

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("The " + hero.name + " goes down")
            utils.theGame().level += 1
            utils.theGame().buildFloor()
        return None
