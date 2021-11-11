import unittest
from game.j5e.game.Agents import Lemming, Trap
from game.j5e.game.GameSpace import GameSpace

class TestMove(unittest.TestCase):

    def setUp(self):
        self.gs = GameSpace()
        self.gs.init_graph(3, 24, 12)
        
    def go(self,start,goal, turnsMax):
        agent=Lemming(1, "Lemmiwings",start, 1, goal, self.gs)
        turns=0
        while agent.active and turns<turnsMax:
            agent.go()
            turns+=1
        self.assertEqual(goal,agent.pos)

    def test_ring000_to_line001(self):
        start = ("ring", 0, 0, 0)
        goal = ("line", 0, 0, 1)
        self.go(start,goal,100)

    def test_line000_to_ring018(self):
        start = ("line", 0, 0, 0)
        goal = ("ring", 0, 1, 8)
        self.go(start,goal,100)
        
    def test_ring019_to_line010(self):
        start = ("ring", 0, 1, 9)
        goal = ("line", 0, 1, 0)
        self.go(start,goal,100)
        
    def test_line010_to_col020(self):
        start = ("line", 0, 1, 0)
        goal = ("column", 0, 1, 0)
        self.go(start,goal,200)

    
    def test_ring_213_to_line2023(self):
        start = ("ring", 2, 1, 3)
        goal = ("line", 2, 0, 12)
        self.go(start,goal,100)

if __name__ == '__main__':
    unittest.main()
