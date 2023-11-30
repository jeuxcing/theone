from threading import Thread
from multiprocessing import Event
from os import path

from game.j5e.game.GameExceptions import OutOfLedsException, NextLedOnOtherSegmentException
from game.j5e.game.Level import Level
from game.j5e.game.LevelBuilder import LevelBuilder
from game.j5e.game.Element import Actions
from game.j5e.game.Agent import Agent
from game.j5e.game.Geometry import Coordinate


class GameEngine(Thread):

    def __init__(self):
        super().__init__()
        self.timer = Event()
        self.levels = LevelBuilder.load_level_list_from_json(
            path.join("game","j5e","game","levels","level_1.json"))
        self.current_level_idx = 0
        self.current_level = self.levels[0].copy()

        
    def run(self):
        i=0
        # boucle d'action des éléments de jeu
        while (not self.current_level.is_over()) and (not self.timer.wait(0.2)):
            print(' Tour n°', i,' : ')
            self.trigger_agents()
            i+=1
    
    def trigger_agents(self):
        for agent in self.current_level.agents:
            self.execute(agent, agent.play())

    def execute(self, agent, action):
        match(action):
            case Actions.MOVE:
                segment = self.current_level.get_segment(agent.coord)
                # update agent vector
                agent.coord, agent.dir = segment.get_next_destination(agent.coord.seg_offset, agent.dir)
                elements = self.current_level.get_elements(agent.coord)
                print(agent.name," va en ", agent.coord)
                self.apply_elements(agent,elements)
    
    def apply_elements(self, agent, elements):
        for el in elements:
            action = el.receive(agent)
            match(action):
                case Actions.DELETE:
                    self.current_level.delete_agent(agent)
                case Actions.TELEPORT:
                    agent.coord = el.coord_dest
                    print(agent.name," téléporté en ", agent.coord)
                    new_elements = self.current_level.get_elements(agent.coord)
                    self.apply_elements(agent, new_elements)



