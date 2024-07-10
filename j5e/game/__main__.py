from j5e.game.GameEngine import GameEngine
from j5e.game.level.Geometry import SegType, Coordinate, Direction

from j5e.network.NetworkControler import NetworkControler

from signal import signal, SIGINT

    

if __name__ == "__main__":
    # Construction des objets de jeu   
    gameEngine =  GameEngine()
    gameEngine.load_levels("levels/levels.txt")

    net_ctrl = NetworkControler(gameEngine)
    gameEngine.set_ctrl(net_ctrl)
    
    # Démarrage des threads
    gameEngine.start()
    net_ctrl.start()

    # Enregistrement des signaux d'interuption
    def signal_handler(sig, frame):
        print('Ctrl+C pressé !')
        net_ctrl.stop()
        gameEngine.stop_thread()
    signal(SIGINT, signal_handler)

    # Attente des threads pour conclure le programme
    net_ctrl.join()
    print("net_ctrl join")
    gameEngine.join()
    print("gameEngine join")
    
    print("fin du main")
    
