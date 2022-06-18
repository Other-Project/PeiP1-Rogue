import utils
from Element import Element


class Chest(Element):
    def __init__(self, name: str='Chest', image="assets/items/chest.png", contain: list = None, size=3):
        Element.__init__(self, name, image=image)
        if contain is None:
            self.contain = [utils.theGame().randEquipment() for _ in range(size)]
        else:
            self.contain = contain

    def open(self):
        return ".\n".join(self.contain)

    def meet(self, hero):
        import utils
        from Hero import Hero
        if isinstance(hero, Hero):
            utils.theGame().addMessage("You open the Chest")
            '''
            return self.open()
            '''
            utils.theGame().GUI.popContain(self.contain)
        return None



