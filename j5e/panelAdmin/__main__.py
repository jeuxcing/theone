# from j5e.game.panelAdmin.AdminWebServer import http_server_start
import time
import os
from j5e.panelAdmin.AdminFlask import ServerFlask




def start_server():
    # Create an instance of the server using our custom request handler
    port = 8080
    server = ServerFlask(port)
    
    # Start the server and keep it running until manually stopped
    try:
        server.start()
        print(f'Server started on port {port}')
        while True:
            time.sleep(.1)
    except KeyboardInterrupt:
        server.stop()
        print('Server stopped.')
    


if __name__ == "__main__":
    start_server()
    os._exit(0)
    