from game.j5e.game.Agents import Lemming, Trap
from game.j5e.game.GameEngine import GameEngine, SegType, Coordinate, Direction

if __name__ == "__main__":
    gameEngine =  GameEngine(3)
    goal = Coordinate(1, 0, SegType.ROW, 0)
    start_lemmi = Coordinate(0, 0, SegType.ROW, 0)
    gameEngine.add(Lemming(1, "Lemmiwings", start_lemmi, Direction.FORWARD, goal))
    start_octo = Coordinate(0, 0, SegType.RING, 0)
    gameEngine.add(Lemming(2, "Octodon", start_octo, Direction.RING_CLOCKWISE, goal))
    #gameEngine.add(Trap(3, "une porte",4))
       
    gameEngine.start()
