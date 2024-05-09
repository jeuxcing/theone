from j5e.game.GameEngine import GameEngine
from j5e.game.level.Geometry import SegType, Coordinate, Direction

from j5e.network.NetworkControler import NetworkControler

from signal import signal, SIGINT

    

if __name__ == "__main__":    
    gameEngine =  GameEngine()
    gameEngine.load_levels("levels/levels.txt")
    gameEngine.start()

    net_ctrl = NetworkControler(gameEngine)
    net_ctrl.start()

    def signal_handler(sig, frame):
        print('You pressed Ctrl+C!')
        net_ctrl.stop()
        gameEngine.stop_thread()

    signal(SIGINT, signal_handler)

    # while not gameEngine.is_over():
    #     time.sleep(.1)
    # print("shutdown")
    # net_ctrl.socket.shutdown(socket.SHUT_RDWR)
    # print("/shutdown")
    # print("close")
    # net_ctrl.socket.close()
    # print("/close")

    net_ctrl.join()
    print("net_ctrl join")
    gameEngine.join()
    print("gameEngine join")

