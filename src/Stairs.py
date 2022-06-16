from Element import Element


class Stairs(Element):
    def __init__(self, name="Stairs", image="assets/items/portal.png"):
        """
        :param name: The name of the element
        :param image: The image of the element
        """
        Element.__init__(self, name=name, image=image)

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("The " + hero.name + " goes down")
            utils.theGame().level += 1
            utils.theGame().buildFloor()
        return None
