from j5e.game.GameEngine import GameEngine
from j5e.game.level.Geometry import SegType, Coordinate, Direction

from j5e.game.faking.FakeControler import FakeControler

import time
import socket

if __name__ == "__main__":
    gameEngine =  GameEngine()
    gameEngine.load_levels("levels/levels.txt")
    gameEngine.start()

    fake = FakeControler(gameEngine)
    fake.start()

    # while not gameEngine.is_over():
    #     time.sleep(.1)
    # print("shutdown")
    # fake.socket.shutdown(socket.SHUT_RDWR)
    # print("/shutdown")
    # print("close")
    # fake.socket.close()
    # print("/close")

    gameEngine.join()
    fake.join()

