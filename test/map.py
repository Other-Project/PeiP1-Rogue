import random
import unittest


class MyTestCase(unittest.TestCase):
    def test_roomGeneration(self):
        from config import rooms
        from Map import Map
        random.seed(1)
        roomKeys = list(rooms.keys())
        for j in range(1, 10000):
            for i in range(len(rooms)):
                rooms[roomKeys[i]] = (len(rooms) + 1 - i) * j * random.randint(1, 100)
            nbRooms = random.randint(5, 15)
            try:
                Map(50, nbRooms=nbRooms)
            except:
                print(nbRooms, rooms)
                self.assertTrue(False)

if __name__ == '__main__':
    unittest.main()
