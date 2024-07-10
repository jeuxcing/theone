import time
import socket
from threading import Thread, Event
from time import sleep
from j5e.game.level.LevelSerializer import LevelSerializer


class NetworkControler(Thread):

    def __init__(self, game):
        super().__init__()
        self.HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        self.PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        self.accept_socket = None # Accepte les connexions entrantes de controleurs
        self.update_sockets = []
        self.game = game
        self.running = Event()
        self.running.set()
        self.clients = []

    # msg : chaine de caractères
    def send_update(self, msg):
        # On envoie l'update à tous les clients connectés
        for socket in self.update_sockets:
            socket.sendall(msg.encode("utf-8"))


    def connect_update(self, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("127.0.0.1", port))
        self.update_sockets.append(sock)


    def notify(self, notified_object=None):
        # msg_list = notified_object.translate_to_msgs()
        self.send_update(notified_object)
        print("ctrl notified")


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.accept_socket:
            self.accept_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.accept_socket.bind((self.HOST, self.PORT))
            self.accept_socket.listen(5)
            self.accept_socket.settimeout(0.000001)

            while (not self.game.is_over()) and self.running.is_set():
                try:
                    client_socket, client_address = self.accept_socket.accept()
                    client_thread = ClientThread(client_socket, self.game, self)
                    client_thread.start()
                    self.clients.append(client_thread)
                except socket.timeout:
                    continue
                except OSError:
                    if self.running.is_set():
                        raise
                time.sleep(1)

        # Déconnexion des sockets clients d'update
        for sock in self.update_sockets:
            sock.close()

    
    def stop(self):
        if not self.running.is_set():
            return
        
        # On coupe et joint tous les threads
        for client in self.clients:
            client.stop()
            client.join()

        # on coupe le thread courant
        self.running.clear()
        self.accept_socket.close()
        

class ClientThread(Thread):
    def __init__(self, client_socket, game, ctrl):
        super().__init__()
        self.client_socket = client_socket
        self.client_socket.settimeout(0.001)
        self.game = game
        self.ctrl = ctrl
        self.running = Event()

    def parse_cmd(self, cmd):
        print(f"Commande: {cmd}")
        
        cmd = cmd.strip().split()
        match cmd[0]:
            case "update_socket":
                port = cmd[1]
                self.ctrl.connect_update(int(port))
                self.ctrl.notify(LevelSerializer.from_level(self.game.current_level))
            case "play":
                self.game.play()
            case "pause":
                self.game.pause()
            case  "reset":
                self.game.suicide_lemmings()
            case "rotation":
                row, col = cmd[1:]
                self.game.change_ring_rotation(int(row), int(col))

    def stop(self):
        self.running.clear()

    def run(self):
        self.running.set()

        while (not self.game.is_over()) and self.running.is_set():
            try:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                else:
                    self.parse_cmd(bytes.decode(data, 'utf-8'))
            except socket.timeout:
                continue
            except OSError:
                if self.running.is_set():
                    raise

        print("fin de connexion client")
