import math


class Coord:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "<" + str(self.x) + "," + str(self.y) + ">"

    def __add__(self, other):
        return Coord(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Coord(self.x - other.x, self.y - other.y)

    def __truediv__(self, other):  # Division décimale
        return Coord(self.x / other, self.y / other)

    def __floordiv__(self, other):  # Quotient de la division euclidienne
        return Coord(self.x // other, self.y // other)

    def __mul__(self, other):
        import numbers
        if isinstance(other, Coord):
            return Coord(self.x * other.x, self.y * other.y)
        elif isinstance(other, numbers.Number):
            return Coord(self.x * other, self.y * other)
        raise TypeError("Not a coordinate or a number")

    def distance(self, other):
        return math.sqrt(math.pow(other.x - self.x, 2) + math.pow(other.y - self.y, 2))

    def norme(self):
        return math.sqrt(math.pow(self.x, 2) + math.pow(self.y, 2))

    def direction(self, other):
        if self == other:
            return Coord(0, 0)
        d = self - other
        cos = d.x / Coord(0, 0).distance(d)
        if cos > 1 / math.sqrt(2):
            return Coord(-1, 0)
        if cos < -1 / math.sqrt(2):
            return Coord(1, 0)
        return Coord(0, -1) if d.y > 0 else Coord(-0, 1)
