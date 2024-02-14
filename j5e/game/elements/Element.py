from j5e.game.Actions import Actions
from j5e.game.elements.Agent import Lemming
from j5e.game.elements.AbstractElement import AbstractElement

class Exit(AbstractElement):
    def __init__(self, coord, remaining_lemmings):
        super().__init__(coord)
        self.remaining_lemmings = remaining_lemmings

    def action(self):
        pass

    def copy(self):
        return Exit(self.coord, self.remaining_lemmings)

    def receive(self, agent):
        if isinstance(agent, Lemming):
            self.remaining_lemmings -= 1
            print(self)
            return Actions.EXIT
        return Actions.NOTHING
    
    def __repr__(self) -> str:
        return f'Exit ({self.remaining_lemmings}) : {self.coord} '

class Teleporter(AbstractElement):
    def __init__(self, coord_src, coord_dest):
        super().__init__(coord_src)
        self.coord_dest = coord_dest
    
    def copy(self):
        return Teleporter(self.coord, self.coord_dest)

    def receive(self, agent):
        return Actions.TELEPORT
    
