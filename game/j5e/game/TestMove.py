import unittest
from game.j5e.game.Agents import Lemming, Trap
from game.j5e.game.GameSpace import GameSpace

class TestMove(unittest.TestCase):

    def setUp(self):
        self.gs = GameSpace()
        self.gs.init_graph(3, 24, 12)

    def test_strip00_to_ring01(self):
        start = ("line", 0, 0, 0)
        goal = ("ring", 0, 1, 8)
        agent=Lemming(1, "Lemmiwings",start, 1, goal, self.gs)
        turns=0
        while agent.active and turns<100:
            agent.go()
            turns+=1
        self.assertEqual (goal,agent.pos)

    def test_ring01_to_strip01(self):
        start = ("ring", 0, 1, 9)
        goal = ("strip", 0, 1, 0)
        agent=Lemming(1, "Lemmiwings", start, 1, goal, self.gs)
        turns=0
        while agent.active and turns<100:
            agent.go()
            turns+=1
        self.assertEqual (goal,agent.pos)
        
    def test_ring_21_to_strip20(self):
        start = ("ring", 2, 1, 3)
        goal = ("strip", 2, 0, 23)
        agent=Lemming(1, "Lemmiwings", start, 1, goal, self.gs)
        turns=0
        while agent.active and turns<100:
            agent.go()
            turns+=1
        self.assertEqual (goal,agent.pos)

if __name__ == '__main__':
    unittest.main()