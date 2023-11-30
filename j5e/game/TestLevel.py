import unittest
from j5e.game.Geometry import Coordinate, Direction, SegType
from j5e.game.Level import Level

class TestLevel(unittest.TestCase):

    def setUp(self):
        self.level = Level(3)
        

    def test_level_demo_without_connection(self):
        for i in range(12):
            self.assertEqual(None, self.level.rings[0][0].paths[i])

    def test_level_connection(self):
        self.level.add_connection_to_ring(0,0,3)
        self.assertEqual(self.level.rows[0][0], self.level.rings[0][0].paths[3])

    def test_level_multiple_connection(self):
        middle_ring = self.level.rings[1][1]
        self.level.connect_all()
        self.assertEqual(self.level.cols[0][1], middle_ring.paths[0])
        self.assertEqual(self.level.rows[1][1], middle_ring.paths[3])
        self.assertEqual(self.level.cols[1][1], middle_ring.paths[6])
        self.assertEqual(self.level.rows[1][0], middle_ring.paths[9])


if __name__ == '__main__':
    unittest.main()
