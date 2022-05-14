class Element:
    def __init__(self, name: str, abbrv: str = None, color="", image=None):
        """
        :param name: The name of the element
        :param abbrv: The symbol used to represent the element on the map
        :param color: The color of the element on the map
        """
        self.name = name
        self.abbrv = color + (abbrv or name[0]) + "\033[00m"
        self.image=image

    def __repr__(self):
        return self.abbrv

    def description(self):
        return "<" + self.name + ">"

    def meet(self, hero):
        raise NotImplementedError("Abstract method")
