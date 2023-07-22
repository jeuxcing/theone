from abc import abstractmethod
from game.j5e.game.GameExceptions import OutOfLedsException

#Autonomous elements
class Agent:
    def __init__(self, period, name, coord):
        self.name = name
        self.period = period
        self.turn_to_wait = period
        self.active = True
        self.coord = coord

    def go(self):
        self.turn_to_wait -= 1
        if not self.turn_to_wait:
            self.action()
            self.turn_to_wait = self.period    
    
    @abstractmethod
    def action(self):
        pass

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
            
    
class Lemming(Agent):

    def __init__(self, period, name, coord, dir, goal):
        super().__init__(period, name, coord)
        self.goal = goal #TODO: will become EXIT ? reify ? managed by Game/level ?
        self.active = True
        self.dir = dir


    def action(self):
        try:
            self.coord = self.coord.get_next_coord(self.dir)
        except OutOfLedsException:
            self.dir = self.dir.opposite()       
            self.coord = self.coord.get_next_coord(self.dir)
        print(self.name," va en ",self.coord)
        if self.coord == self.goal:
            self.active = False
            print(self.name," a fini")
        
