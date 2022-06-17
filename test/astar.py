import random
import unittest
import utils


def newMap(size, heroPos, monsterPos):
    from Map import Map
    from config import monsters

    floor = Map(size)
    floor._elem = {}
    floor._mat = [[floor.ground for x in range(floor.size)] for y in range(floor.size)]  # Clear the map

    floor.put(heroPos, floor.hero)  # Hero

    monster = monsters[0][0]  # Monster
    floor.put(monsterPos, monster)

    game = utils.theGame()
    game.floor = floor
    return game


def getAstar(floor, heroPos):
    from AStar import AStar
    return AStar(floor, heroPos)


def getPath(astar, monsterPos):
    path = astar.findPath(monsterPos)
    print("From", astar.startNode, "to", monsterPos)
    print(astar.getMatRepr(path))
    return path


class AStarTest(unittest.TestCase):
    def test_blocked(self):
        """An unreachable destination (small map)"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 3)
        monsterPos = Coord(4, 3)
        game = newMap(5, heroPos, monsterPos)

        for x in range(0, game.floor.size):  # Wall
            game.floor._mat[x][game.floor.size // 2] = game.floor.empty

        path = getPath(getAstar(game.floor, heroPos), monsterPos)
        self.assertListEqual(path, [])

    def test_blocked2(self):
        """An unreachable destination (big map)"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 12)
        monsterPos = Coord(24, 12)
        game = newMap(25, heroPos, monsterPos)

        for x in range(0, game.floor.size):  # Wall
            game.floor._mat[x][game.floor.size // 2] = game.floor.empty

        path = getPath(getAstar(game.floor, heroPos), monsterPos)
        self.assertListEqual(path, [])

    def test_direct(self):
        """A direct line"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 2)
        monsterPos = Coord(4, 2)
        game = newMap(5, heroPos, monsterPos)
        path = getPath(getAstar(game.floor, heroPos), monsterPos)
        self.assertNotEqual(path, [])
        self.assertEqual(len(path), 4)

    def test_monsters(self):
        """There are two monsters on the map"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 19)
        monsterPos1 = Coord(19, 0)
        monsterPos2 = Coord(19, 19)
        game = newMap(20, heroPos, monsterPos1)

        from config import monsters
        import copy
        monster = copy.copy(monsters[0][0])  # Monster
        game.floor.put(monsterPos2, monster)

        # Walls
        random.seed(1)
        for i in range(75):
            game.floor._mat[random.randint(0, 19)][random.randint(0, 19)] = game.floor.empty

        astar = getAstar(game.floor, heroPos)
        path1 = getPath(astar, monsterPos1)
        self.assertNotEqual(path1, [])
        self.assertEqual(len(path1), 38)
        path2 = getPath(astar, monsterPos2)
        self.assertNotEqual(path2, [])
        self.assertEqual(len(path2), 23)

    def test_spikes(self):
        """Navigate through a map made of random walls"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 19)
        monsterPos = Coord(19, 0)
        game = newMap(20, heroPos, monsterPos)

        # Walls
        random.seed(50)
        for i in range(150):
            game.floor._mat[random.randint(0, 19)][random.randint(0, 19)] = game.floor.empty

        path = getPath(getAstar(game.floor, heroPos), monsterPos)
        self.assertNotEqual(path, [])
        self.assertEqual(len(path), 38)

    def test_wall(self):
        """Going around a wall"""
        print("\n" + self.shortDescription())
        from Coord import Coord

        heroPos = Coord(0, 6)
        monsterPos = Coord(9, 5)
        game = newMap(10, heroPos, monsterPos)

        for x in range(2, 8):  # Wall
            game.floor._mat[x][4] = game.floor.empty

        path = getPath(getAstar(game.floor, heroPos), monsterPos)
        self.assertNotEqual(path, [])
        self.assertEqual(len(path), 14)


if __name__ == '__main__':
    unittest.main()
