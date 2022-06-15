import random
import unittest
import utils


def newMap(size, heroPos, monsterPos):
    from Map import Map
    from config import monsters

    floor = Map(size)
    floor._mat = [[floor.ground for x in range(floor.size)] for y in range(floor.size)]  # Clear the map

    floor.put(heroPos, floor.hero)  # Hero

    monster = monsters[0][0]  # Monster
    floor.put(monsterPos, monster)

    game = utils.theGame()
    game.floor = floor
    return game


def getAstar(floor, heroPos, monsterPos):
    from AStar import AStar
    astar = AStar(floor, heroPos)
    path = astar.findPath(monsterPos)
    print("From", heroPos, "to", monsterPos)
    print(astar.getMatRepr(path))
    return astar, path


class AStarTest(unittest.TestCase):
    def test_blocked(self):
        """An unreachable destination"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 3)
        monsterPos = Coord(4, 3)
        game = newMap(5, heroPos, monsterPos)

        for x in range(0, 5):  # Wall
            game.floor._mat[x][2] = game.floor.empty

        astar, path = getAstar(game.floor, heroPos, monsterPos)
        self.assertListEqual(path, [])

    def test_direct(self):
        """A direct line"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 2)
        monsterPos = Coord(4, 2)
        game = newMap(5, heroPos, monsterPos)
        astar, path = getAstar(game.floor, heroPos, monsterPos)
        self.assertLessEqual(len(path), 4)

    def test_wall(self):
        """Going around a wall"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 6)
        monsterPos = Coord(9, 5)
        game = newMap(10, heroPos, monsterPos)

        for x in range(2, 8):  # Wall
            game.floor._mat[x][4] = game.floor.empty

        astar, path = getAstar(game.floor, heroPos, monsterPos)
        self.assertLessEqual(len(path), 14)

    def test_spikes(self):
        """Navigate through a map made of random walls"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 19)
        monsterPos = Coord(19, 0)
        game = newMap(20, heroPos, monsterPos)

        # Walls
        random.seed(1)
        for i in range(150):
            game.floor._mat[random.randint(0, 19)][random.randint(0, 19)] = game.floor.empty

        astar, path = getAstar(game.floor, heroPos, monsterPos)
        self.assertLessEqual(len(path), 40)


if __name__ == '__main__':
    unittest.main()
