# from j5e.game.panelAdmin.AdminWebServer import http_server_start
from j5e.game.panelAdmin.AdminFlask import ServerFlask

if __name__ == "__main__":
    # http_server_start
    server = ServerFlask()
    server.start()