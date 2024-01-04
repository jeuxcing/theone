from abc import abstractmethod
from j5e.game.GameExceptions import OutOfLedsException
from j5e.game.Actions import Actions
from j5e.game.elements.AbstractElement import AbstractElement

#Autonomous elements
class Agent(AbstractElement):
    def __init__(self, name, coord, period = 1):
        super().__init__(coord)
        self.name = name
        self.turn_to_wait = period
        self.period = period

    @abstractmethod
    def act(self):
        pass
    
    def play(self):
        self.turn_to_wait -= 1
        if not self.turn_to_wait:
            action = self.act()
            self.turn_to_wait = self.period    
            return action
        else:
            return Actions.NOTHING

    
class Lemming(Agent):

    def __init__(self, name, coord, dir, period=1):
        super().__init__(name, coord, period)
        self.dir = dir

    def act(self):
        return Actions.MOVE

    def copy(self):
        return Lemming(self.name, self.coord, self.dir, self.period)


