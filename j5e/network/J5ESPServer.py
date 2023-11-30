from Server import ESPServer, connection_callback
from signal import signal, SIGINT
from time import sleep

class J5ESPServer(ESPServer):
    def __init__(self):
        super().__init__()

if __name__ == "__main__":
    server = ESPServer()
    signal(SIGINT, lambda sig, frame : server.stop())
    server.register_connection_handler(connection_callback)
    server.start()
    while True:
        for i in range(24):
            msg = [ord('L'),0,0,0,0,1,i,1]
            for client in server.clients.values():
                client.send_msg(bytes(msg))
            sleep(.1)
            msg = [ord('L'),0,0,0,0,1,i,0]
            for client in server.clients.values():
                client.send_msg(bytes(msg))
            