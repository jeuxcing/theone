from threading import Thread
from multiprocessing import Event
from os import path

from game.j5e.game.GameExceptions import OutOfLedsException, NextLedOnOtherSegmentException
from game.j5e.game.Level import Level, LevelBuilder
from game.j5e.game.Agents import Actions


class GameEngine(Thread):

    def __init__(self):
        super().__init__()
        self.timer = Event()
        self.levels = LevelBuilder.load_level_list_from_json(
            path.join("game","j5e","game","levels","level_1.json"))
        self.current_level_idx = 0
        self.current_level = self.levels[0].copy()

    def add(self,el):
        self.elements.append(el)

        
    def run(self):
        i=0
        # boucle d'action des éléments de jeu
        while (not self.current_level.is_over()) and (not self.timer.wait(0.2)):
            print(' Tour n°', i,' : ')
            for agent in self.current_level.agents:
                action = agent.play()
                match(action):
                    case Actions.MOVE:
                        # update agent vector
                        agent.segment, agent.offset, agent.dir = agent.segment.get_next_destination(agent.offset, agent.dir) 
                        print(agent.name," va en ", agent.segment.coord, agent.offset)
                         
            i+=1
    
