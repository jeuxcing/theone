from j5e.game.GameEngine import GameEngine
from j5e.game.level.Geometry import SegType, Coordinate, Direction

from j5e.game.faking.FakeControler import FakeControler

if __name__ == "__main__":
    fake = FakeControler()
    fake.listen()

    # gameEngine =  GameEngine()
    # gameEngine.load_levels("levels/levels.txt")
    # gameEngine.start()
