from j5e.game.GameEngine import GameEngine
from j5e.game.Geometry import SegType, Coordinate, Direction

if __name__ == "__main__":
    gameEngine =  GameEngine()
    gameEngine.load_levels("levels/levels.txt")
    gameEngine.start()
