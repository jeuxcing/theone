import time
import socket
from threading import Thread


class NetworkControler(Thread):

    def __init__(self, game):
        super().__init__()
        self.HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        self.PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        self.accept_socket = None # Accepte les connexions entrantes de controleurs
        self.update_sockets = []
        self.game = game
        self.stopped = False

    def parse_cmd(self, cmd):
        print(f"Commande: {cmd}")
        
        cmd = cmd.strip().split()
        match cmd[0]:
            case "update_socket":
                port = cmd[1]
                self.connect_update(int(port))
            case "play":
                self.game.play()
            case "pause":
                self.game.pause()
            case  "reset":
                self.game.suicide_lemmings()
            case "rotation":
                row, col = cmd[1:]
                self.game.change_ring_rotation(int(row), int(col))

    # msg : chaine de caractères
    def send_update(self, msg):
        # On envoie l'update à tous les clients connectés
        for socket in self.update_sockets:
            socket.sendall(msg.encode("utf-8"))


    def connect_update(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        self.update_sockets.append(sock)


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.accept_socket:
            self.accept_socket.bind((self.HOST, self.PORT))
            self.accept_socket.listen()
            while (not self.game.is_over()) and (not self.stopped):
                conn, addr = self.accept_socket.accept()

                print(f"Le controleur est connecté")
                while (not self.game.is_over()) and (not self.stopped):
                    data = conn.recv(1024)
                    if not data:
                        break
                    else:
                        self.parse_cmd(bytes.decode(data, 'utf-8'))

                    print("fin de connexion")
                time.sleep(.1)

        # Déconnexion des sockets clients d'update
        for sock in self.update_sockets:
            sock.shutdown()
            sock.close()

    
    def stop(self):
        self.stopped = True
        self.accept_socket.close()
