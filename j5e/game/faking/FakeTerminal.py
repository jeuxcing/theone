import socket
import time

def connect():
    HOST = "127.0.0.1"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        val = input()
        while val != "quit":
            print(val)
            s.sendall(val.encode("utf-8"))
            val = input()
