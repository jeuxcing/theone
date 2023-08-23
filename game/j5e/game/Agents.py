from abc import abstractmethod
from enum import Enum
from game.j5e.game.GameExceptions import OutOfLedsException

class Element:
    def __init__(self, coord):
        self.coord = coord.copy()
    
    @abstractmethod
    def action(self):
        pass
    
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def receive(self):
        pass

class Exit(Element):
    def __init__(self, coord, remaining_lemmings):
        super().__init__(coord)
        self.remaining_lemmings = remaining_lemmings

    def action(self):
        pass

    def copy(self):
        return Exit(self.coord, self.remaining_lemmings)

    def receive(self, agent):
        if isinstance(agent,Lemming):
            self.remaining_lemmings -= 1
        return Actions.DELETE

#Autonomous elements
class Agent(Element):
    def __init__(self, name, coord, period = 1):
        super().__init__(coord)
        self.name = name
        self.turn_to_wait = period
        self.period = period

    def play(self):
        self.turn_to_wait -= 1
        if not self.turn_to_wait:
            action = self.action()
            self.turn_to_wait = self.period    
            return action
        else:
            return Actions.NOTHING

    
class Lemming(Agent):

    def __init__(self, name, coord, dir, period=1):
        super().__init__(name, coord, period)
        self.dir = dir


    def action(self):
        return Actions.MOVE

    def copy(self):
        return Lemming(self.name, self.coord, self.dir, self.period)



class Actions(Enum):
    NOTHING=0,
    MOVE=1,
    DELETE=2

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
