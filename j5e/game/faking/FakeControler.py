import time
import socket
from threading import Thread


class FakeControler(Thread):

    def __init__(self, game):
        super().__init__()
        self.HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        self.PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        self.game = game

    def parse_cmd(self, cmd):
        print(f"Commande: {cmd}")
        if cmd == "play" and self.game.pause:
            self.game.set_pause()
        if cmd == "pause" and not self.game.pause:
            self.game.set_pause()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f"Le faux controleur est connecté")
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        else:
                            self.parse_cmd(bytes.decode(data, 'utf-8'))
