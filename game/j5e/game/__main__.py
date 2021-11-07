from j5e.game.Timer import Timer
from j5e.game.Agents import Lemming, Trap
from j5e.game.GameSpace import GameSpace

if __name__ == "__main__":
    #stopFlag = Event()
    #timer = Timer(stopFlag)
    timer = Timer()
    gs = GameSpace()
    gs.init_graph(3, 24, 12)
    pos1 = ("line", 0, 0, 0)
    pos2 = ("ring", 0, 1, 0)
    goal = ("ring", 0, 1, 11) 
    timer.add(Lemming(1, "Lemmiwings",pos1, 1, goal, gs))
    timer.add(Lemming(2, "Octodon",pos2, 1, goal, gs))
    #timer.add(Trap(3, "une porte",4))
       
    timer.start()