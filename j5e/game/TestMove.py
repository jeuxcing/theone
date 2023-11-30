import unittest
from j5e.game.Geometry import Coordinate, Direction, SegType
from j5e.game.Level import Level

class TestMove(unittest.TestCase):

    def setUp(self):
        self.lvl = Level(3)

    
'''        
    def go(self,start,goal,initialDir,turnsMax):
        agent=Lemming(1, "Lemmiwings",start, initialDir, goal, self.gs)
        turns=0
        while agent.active and turns<turnsMax:
            #print(agent.dir)
            agent.go()
            turns+=1
        self.assertEqual(goal,agent.pos)


    def test_00line0_to_00line1(self):
        start = Coordinate(0, 0, SegType.RING, 0)
        goal = Coordinate(0, 0, SegType.RING, 1)
        self.go(start,goal,Direction.FORWARD,100)

        
    def test_line000_to_ring018(self):
        start = ("line", 0, 0, 0)
        goal = ("ring", 0, 1, 8)
        self.go(start,goal,Direction.FORWARD,100)
        
    def test_ring019_to_line010(self):
        start = ("ring", 0, 1, 9)
        goal = ("line", 0, 1, 0)
        self.go(start,goal,Direction.RING_FORWARD,100)
        
    def test_line010_to_col020(self):
        start = ("line", 0, 1, 0)
        goal = ("column", 0, 1, 0)
        self.go(start,goal,Direction.FORWARD,200)

    
    def test_ring_213_to_line2023(self):
        start = ("ring", 2, 1, 3)
        goal = ("line", 2, 0, 12)
        self.go(start,goal,Direction.FORWARD,100)

    def test_line_011_to_line_010_fw_wall_l012(self):
        start = ("line", 0, 1, 1)
        goal = ("line", 0, 1, 0)
        self.gs.set_section_status("line",0,1,2,2,0)
        self.go(start,goal,Direction.FORWARD,1)
        
    def test_col_011_to_col_010_fw_wall_c012(self):
        start = ("column", 0, 1, 1)
        goal = ("column", 0, 1, 0)
        self.gs.set_section_status("column",0,1,2,2,0)
        self.go(start,goal,Direction.FORWARD,1)


    def test_line_001_to_col_101_reverse_ring_01(self):
        start = ("line", 0, 0, 1)
        goal = ("column", 1, 0, 1)
        self.gs.change_direction_segment("ring", 0, 1)
        self.go(start, goal, Direction.FORWARD, 100)
'''        
        
if __name__ == '__main__':
    unittest.main()
