import time
import socket


class FakeControler:

    def __init__(self):
        self.HOST = "127.0.0.1"  # Standard loopback interface address (localhost)
        self.PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

    def parse_cmd(self, cmd):
        print(cmd)

    def listen(self):
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
