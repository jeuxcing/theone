from threading import Thread
from multiprocessing import Event
from os import path

from j5e.game.GameExceptions import OutOfLedsException, NextLedOnOtherSegmentException
from j5e.game.level.Level import Level
from j5e.game.level.LevelBuilder import LevelBuilder
from j5e.game.elements.Element import Actions
from j5e.game.elements.Agent import Agent
from j5e.game.level.Geometry import Coordinate


class GameEngine(Thread):

    def __init__(self):
        super().__init__()
        self.timer = Event()
        self.levels = []

        self.current_level = None
        self.current_level_idx = None
        self._pause = True

    def load_levels(self, filepath):
        """ Charge les niveaux depuis une liste de chemin relatifs de json les décrivants                
        """
        with open(filepath) as fp:
            dirpath = path.dirname(path.abspath(filepath))
            # Charge les niveaux un à un
            for line in fp:
                line = line.strip()
                # Chemin relatif au fichier qui liste les niveaux
                lvlpath = path.join(dirpath, line) 
                self.levels.append(LevelBuilder.load_level_from_json(lvlpath))

            # Met en place le niveau après chargement
            if len(self.levels) > 0:
                self.current_level_idx = 0
        
    def run(self):
        while (not self.is_over()):
            print(' Level n°', self.current_level_idx)
            self.current_level = self.levels[self.current_level_idx].copy()
            self.pause()
            self.run_current_lvl()
            self.current_level_idx += 1
            print("Niveau complété :o\n")
        print("Game Over")
        
    
    def is_over(self):
        return self.current_level_idx >= len(self.levels)

    def run_current_lvl(self):
        i=0
        # boucle d'action des éléments de jeu
        while (not self.current_level.is_over()) and (not self.timer.wait(0.2)):
            if (not self._pause):
                print(' Tour n°', i,' : ')
                self.trigger_agents()
                i += 1

    def pause(self):
        self._pause = True

    def play(self):
        self._pause = False

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

    def change_ring_rotation(self, row, col):
        self.current_level.reverse_ring(row,col)

