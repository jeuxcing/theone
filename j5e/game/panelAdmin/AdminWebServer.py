import socket

from os import getcwd, path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from threading import Thread
from time import sleep
from urllib.parse import urlparse


WWW_DIRECTORY = path.join(getcwd(), "j5e/game/panelAdmin/www")

game = None

class MyRequestHandler(BaseHTTPRequestHandler):
    
    # Function to handle GET requests
    def do_GET(self):
        # Get the requested URL
        requested_url = self.path

        # Search for the file in the www directory
        filepath = self.get_file_path(requested_url)

        # If the file exists, serve it; otherwise, route the request
        if filepath:
            self.serve_file(filepath)
        else:
            self.route_request(requested_url)
    

     # Method to get the full path of the file in the www directory
    def get_file_path(self, url):
        # Extract the filename from the URL
        filename = url[1:]  # Remove the leading "/"
        filepath = path.join(WWW_DIRECTORY, filename)

        # Check if the file exists
        if path.exists(filepath) and path.isfile(filepath):
            return filepath
        else:
            return None

    # Method to serve a file
    def serve_file(self, filepath):
        # Read the content of the file
        with open(filepath, "rb") as file:
            content = file.read()

        # Send the response with code 200 (OK) and the appropriate MIME type for HTML
        self.send_response(200)
        types = {"htm":"text/html", "html":"text/html", "css": "text/css", "js": "text/javascript"}
        ext = filepath[filepath.rfind(".")+1:]
        self.send_header('Content-type', types[ext])

        self.end_headers()
        self.wfile.write(content)

    # Method to route requests
    def route_request(self, url):
        path = urlparse(url).path
        print(path, url)
        if path == "/gamemsg":
        #localhost:xxx/gamemsg?play
            liste_de_cmd = frozenset(["play", "pause", "reset", "rotation"])
            if urlparse(url).query in liste_de_cmd:                

                global game
                msg = urlparse(url).query
                game.send_msg(msg)

                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes("Msg sent to game: {}".format(msg), "utf-8"))
            else:
                # Here you can add your routing logic for URLs
                # In this example, we simply send a response indicating that the URL is not found
                self.send_response(404)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(bytes("404 Not Found: {}".format(url), "utf-8"))


class ConnectionToGame(Thread):
    def __init__(self, ip="127.0.0.1", port=65432):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.letterbox = []
        self.stopped = False

    def send_msg(self, msg):
        self.letterbox.append(msg)

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.ip, self.port))
                    print("Connecté au serveur")

                    while not self.stopped:
                        print("game socket - boucle générale")
                        # Attend une commande à envoyer
                        while len(self.letterbox) == 0:
                            sleep(.01)
                            if self.stopped:
                                return
                        # Envoie les commandes en attente
                        to_send, self.letterbox = self.letterbox, []
                        print(to_send)
                        for val in to_send:
                            print(val)
                            s.sendall(val.encode("utf-8"))

                            if val == "quit":
                                return
            except ConnectionRefusedError:
                print("Pas de serveur de jeu trouvé")
                sleep(1)

def http_server_start():
    # Specify the IP address and port on which the server will listen
    address = ('', 8080)
    
    # Create an instance of the server using our custom request handler
    server = HTTPServer(address, MyRequestHandler)
    print('Server started on {}:{}'.format(*address))

    global game
    game = ConnectionToGame()
    game.start()
    
    # Start the server and keep it running until manually stopped
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()
        print('Server stopped.')

    game.stop()
    game.join()