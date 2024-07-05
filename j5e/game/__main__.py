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

    gameEngine.set_ctrl(net_ctrl)

    def signal_handler(sig, frame):
        print('Ctrl+C pressé !')
        net_ctrl.stop()
        gameEngine.stop_thread()

    signal(SIGINT, signal_handler)

    net_ctrl.join()
    print("net_ctrl join")
    gameEngine.join()
    print("gameEngine join")
    
    print("fin du main")
    
