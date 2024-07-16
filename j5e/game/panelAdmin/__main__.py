# from j5e.game.panelAdmin.AdminWebServer import http_server_start
import time
from j5e.game.panelAdmin.AdminFlask import ServerFlask, ConnectionToGame




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
    