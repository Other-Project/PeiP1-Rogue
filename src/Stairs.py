from Element import Element


class Stairs(Element):
    def __init__(self, name="Stairs", abbrv="E", color="", image="assets/other/fountain.png"):
        Element.__init__(self, name=name, abbrv=abbrv, color=color, image=image)

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("The " + hero.name + " goes down")
            utils.theGame().lvl += 1
            utils.theGame().buildFloor()
        return None
