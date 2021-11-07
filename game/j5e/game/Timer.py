from threading import Thread
from multiprocessing import Event
from j5e.game.Agents import Lemming

class Timer(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.stopped = Event()
        self.elements=[]
        
    def add(self,el):
        self.elements.append(el)  
        
    def run(self):
        i=0
        while not self.stopped.wait(0.2):
            print(i,' : ')
            for element in self.elements:
                element.go()
                if  isinstance(element,Lemming) and element.active==False:
                    self.elements.remove(element)
                    if True not in [isinstance(ele,Lemming) for ele in self.elements] :
                        self.stopped.set()
            i+=1