from abc import abstractmethod
from enum import Enum
from game.j5e.game.GameExceptions import OutOfLedsException

#Autonomous elements
class Agent:
    def __init__(self, name, segment = None, offset = None, period = 1):
        self.name = name
        self.turn_to_wait = period
        self.segment = segment
        self.offset = offset
        self.period = period

    def play(self):
        self.turn_to_wait -= 1
        if not self.turn_to_wait:
            action = self.action()
            self.turn_to_wait = self.period    
            return action
        else:
            return Actions.NOTHING
    
    @abstractmethod
    def action(self):
        pass
    
    @abstractmethod
    def copy(self):
        pass

    
class Lemming(Agent):

    def __init__(self, name, segment, offset, dir, period=1):
        super().__init__(name, segment, offset, period)
        self.dir = dir


    def action(self):
        return Actions.MOVE

    def copy(self):
        return Lemming(self.name, self.segment, self.offset, self.dir, self.period)



class Actions(Enum):
    NOTHING=0,
    MOVE=1

'''
class Trap(Agent):
    def __init__(self, period, name, coord):
        super().__init__(period, name, cord)
        self.activated = True

    def action(self): 
        if self.activated:
            print(self.name, " est actif en ", self.coord,)
            self.activated = False
        else:
            print(self.name,"se ferme en ", self.coord)
            self.activated = True
'''
