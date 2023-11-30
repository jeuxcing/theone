import unittest
from j5e.game.Geometry import Coordinate, Direction, SegType

class TestCoordinate(unittest.TestCase):

    def setUp(self):
        pass

    def test_next_coord_fw_00ring0_is_00ring_1(self):
        origin = Coordinate(0, 0, SegType.RING, 0)
        dest = Coordinate(0, 0, SegType.RING, 1)
        self.assertEqual(dest, origin.get_next_coord(Direction.RING_CLOCKWISE))

    def test_next_coord_bw_11col1_is_11col_0(self):
        origin = Coordinate(1, 1, SegType.COL, 1)
        dest = Coordinate(1, 1, SegType.COL, 0)
        self.assertEqual(dest, origin.get_next_coord(Direction.BACKWARD))

if __name__ == '__main__':
    unittest.main()
