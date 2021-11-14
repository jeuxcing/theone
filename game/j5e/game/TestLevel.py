import unittest
from game.j5e.game.Agents import Lemming, Trap
from game.j5e.game.GameSpace import GameSpace, Direction
from game.j5e.hardware.led_strip import Grid, GridDims as gd, GridDims
from game.j5e.game.level import Config,Level

class TestLevel(unittest.TestCase):

    def setUp(self):
        self.level = Level()
        

    def test_level_demo(self):
        self.level.set_config_from_json("levels/level_demo.json")
        turns=0
        agent = self.level.agent
        while agent.active:
            #print(agent.dir)
            agent.go()
            turns+=1
        self.assertEqual(agent.goal,agent.pos)

        
if __name__ == '__main__':
    unittest.main()
