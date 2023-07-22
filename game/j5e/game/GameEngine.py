from threading import Thread
from multiprocessing import Event

from game.j5e.game.GameExceptions import OutOfLedsException, NextLedOnOtherSegmentException
from game.j5e.game.Level import Level
from game.j5e.game.Agents import Actions




class GameEngine(Thread):

    def __init__(self, ):
        super().__init__()
        self.timer = Event()
        self.level = Level(3)


    def add(self,el):
        self.elements.append(el)

    def get_next_coord(self, coord, dir):

        #Select the current segment
        current_segment = None
        if (coord.segment_type == SegType.RING):
            current_segment = self.rings[coord.row][coord.col]
        elif (coord.segment_type == SegType.ROW):
            current_segment = self.rows[coord.row][coord.col]
        else:
            current_segment = self.cols[coord.row][coord.col]

        #Get the next coord
        try:
            return current_segment.get_next_coord(coord, dir)
        except OutOfLedsException:
            raise OutOfLedsException            
        except NextLedOnOtherSegmentException:
            #TODO calcul coordonné en sortie de segment
            if dir==Direction.FORWARD:
                +1
            else :
                -1
            return Coordinate()

        
    def run(self):
        i=0
        # boucle d'action des éléments de jeu
        while (not self.level.is_over()) and (not self.timer.wait(0.2)):
            print(' Tour n°', i,' : ')
            for agent in self.level.agents:
                action = agent.play()
                match(action):
                    case Actions.MOVE:
                        # update agent vector
                        agent.segment, agent.offset, agent.dir = agent.segment.get_next_destination(agent.offset, agent.dir) 
                        print(agent.name," va en ", agent.segment.coord, agent.offset)
                         
            i+=1


'''
        try:
            self.coord = self.coord.get_next_coord(self.dir)
        except OutOfLedsException:
            self.dir = self.dir.opposite()       
            self.coord = self.coord.get_next_coord(self.dir)
        if self.coord == self.goal:
            self.active = False
            print(self.name," a fini")
        
'''