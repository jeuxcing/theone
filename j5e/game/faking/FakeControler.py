import time
import socket
from threading import Thread


class FakeControler(Thread):

    def __init__(self, game):
        super().__init__()
        self.HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        self.PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
        self.socket = None
        self.game = game

    def parse_cmd(self, cmd):
        print(f"Commande: {cmd}")
        if cmd == "play":
            self.game.play()
        elif cmd == "pause":
            self.game.pause()
        elif cmd == "reset":
            self.game.suicide_lemmings()

        elif cmd.startswith("rotation"):
            _, row, col = cmd.strip().split(' ')
            self.game.change_ring_rotation(int(row), int(col))

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.bind((self.HOST, self.PORT))
            self.socket.listen()
            # self.socket.setblocking(False)
            while not self.game.is_over():
                conn, addr = self.socket.accept()
                with conn:
                    print(f"Le faux controleur est connecté")
                    while not self.game.is_over():
                        # try:
                        data = conn.recv(1024)
                        if not data:
                            break
                        else:
                            self.parse_cmd(bytes.decode(data, 'utf-8'))
                        # except socket.error as e:
                        #     continue

                    print("fin de connexion")
                time.sleep(.1)
