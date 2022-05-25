class Element:
    def __init__(self, name: str, image=None):
        """
        :param name: The name of the element
        :param image: The image of the element
        """
        self.name = name
        self.image = image

    def __repr__(self):
        return self.name

    def description(self):
        return "<" + self.name + ">"

    def meet(self, hero):
        raise NotImplementedError("Abstract method")
