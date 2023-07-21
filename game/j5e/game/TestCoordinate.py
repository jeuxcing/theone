import unittest
from game.j5e.game.GameSpace import GameSpace, Direction

class TestCoordinate(unittest.TestCase):

    def setUp(self):
        self.gs = GameSpace(1)

    def test_next_coord_fw_00ring0_is_00ring_1(self):
        origin = Coordinate(0, 0, SegType.RING, 0)
        dest = Coordinate(0, 0, SegType.RING, 1)
        self.assertEqual(dest, origin.get_next_coord(Direction.FORWARD))
        
if __name__ == '__main__':
    unittest.main()
