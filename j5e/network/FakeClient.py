import socket
import time


if __name__ == "__main__":
    with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as sck:
        # try to reduce delay (doesn't work)
        # sck.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        sck.connect(("127.0.0.1",65432))

        sck.sendall(b"ESP azerty")

        while True:
            data = sck.recv(1024)
            print(time.time())
