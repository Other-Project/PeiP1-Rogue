class Element:
    def __init__(self, name, abbrv=None, color=""):
        self.name = name
        self.abbrv = color + (abbrv or name[0]) + "\033[00m"

    def __repr__(self):
        return self.abbrv

    def description(self):
        return "<" + self.name + ">"

    def meet(self, hero):
        raise NotImplementedError("Not implemented yet")
