from abc import abstractmethod

class AbstractElement:
    def __init__(self, coord):
        self.coord = coord.copy()
    
    @abstractmethod
    def copy(self):
        pass

    @abstractmethod
    def receive(self, agent):
        pass