from Element import Element


class Stairs(Element):
    def __init__(self, name="Stairs", abbrv="E", color=""):
        Element.__init__(self, name, abbrv, color)

    def meet(self, hero):
        import main
        from Hero import Hero
        if isinstance(hero, Hero):
            main.theGame().addMessage("The " + hero.name + " goes down")
            main.theGame().level += 1
            main.theGame().buildFloor()
        return None
