from abc import ABC, abstractmethod

#Autonomous elements
class Agent:
    def __init__(self, period, name, pos, game):
        self.name=name
        self.period=period
        self.counter=period
        self.active=True
        self.pos=pos
        self.game=game

    def go(self):
        self.counter-=1
        if not self.counter:
            self.action()
            self.counter=self.period    
    
    @abstractmethod
    def action(self):
        pass

class Trap(Agent):
    def __init__(self, period, name, pos, game):
        super().__init__(period, name, pos,game)
        self.activated = True

    def action(self): 
        if self.activated:
            print(self.name, " est actif en ", self.pos,)
            self.activated=False
        else:
            print(self.name,"se ferme en ", self.pos)
            self.activated=True
            
    
class Lemming(Agent):

    def __init__(self, period, name, pos, dir, goal, game):
        super().__init__(period,name, pos,game)
        self.goal=goal #TODO: will become EXIT ? reify ? managed by Game/level ?
        self.active = True
        self.dir = dir


    def action(self):
        #get_next_position
        next=self.game.get_next_position( (self.pos[0], self.pos[1], self.pos[2], self.pos[3], self.dir) )
        self.pos=next[0:4]
        self.dir=next[4]
        print(self.name," avance en ",self.pos)
        if self.pos==self.goal:
            self.active=False
            print(self.name," a fini")
        
