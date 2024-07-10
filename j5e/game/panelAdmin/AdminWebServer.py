import socket

from os import getcwd, path
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from threading import Thread
from time import sleep
from urllib.parse import urlparse
from select import select


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
        if len(filename) == 0:
            filename = "index.html"
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
        types = {"htm":"text/html", "html":"text/html", "css": "text/css", "js": "text/javascript", "ico": "image/vnd.microsoft.icon"}
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
        self.from_game = None
        self.update_port = 8087

    def send_msg(self, msg):
        self.letterbox.append(msg)

    def stop(self):
        if self.from_game is not None:
            self.from_game.stop()
            self.from_game.join()
        
        self.stopped = True

    def send_letterbox(self, socket):
        # Envoie les commandes en attente
        to_send, self.letterbox = self.letterbox, []
        print(to_send)

        for val in to_send:
            print(val)
            socket.sendall(val.encode("utf-8"))

    def check_socket_alive(self, sock):
        try:
            # Utilisation de select pour vérifier si le socket est prêt pour la lecture ou l'écriture
            read_ready, _, _ = select([sock], [], [], 0)
            if read_ready:
                # Si le socket est prêt pour la lecture, essayer de lire un petit morceau de données
                data = sock.recv(1024, socket.MSG_PEEK)
                if len(data) == 0:
                    # Si recv retourne 0 octets, cela signifie que la connexion est fermée
                    return False
            return True
        except socket.error:
            return False
    

    def run(self):
        while not self.stopped:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((self.ip, self.port))
                    s.settimeout(0.0001)
                    print("Connecté au serveur")
                    
                    # Création d'une connexion retour
                    self.from_game = ConnectionFromGame(self.update_port)
                    self.from_game.start()
                    sleep(.05)
                    s.sendall(f"update_socket {self.update_port}".encode("utf-8"))

                    while True:
                        # 0 - Vérifier qu'on est pas arrété
                        if self.stopped:
                            break

                        # 1 - Verifier la connexion
                        is_alive = self.check_socket_alive(s)

                        if not is_alive:
                            self.from_game.stop()
                            break

                        # 2 - Envoyer les messages en attente
                        if len(self.letterbox) > 0:
                            self.send_letterbox(s)
                        
            except ConnectionRefusedError:
                print("Pas de serveur de jeu trouvé")
                sleep(1)


class ConnectionFromGame(Thread):

    def __init__(self, port):
        Thread.__init__(self)
        self.socket = None
        self.stopped = False
        self.port = port

    def stop(self):
        self.stopped = True
        sleep(.1)
        self.socket.close()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as self.socket:
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.bind(("127.0.0.1", self.port))
            self.socket.settimeout(0.01)
            self.socket.listen()

            while not self.stopped:
                try:
                    conn, addr = self.socket.accept()

                    while not self.stopped:
                        try:
                            data = conn.recv(1024)
                            if not data:
                                print(data)
                                break
                            else:
                                self.parse_msg(bytes.decode(data, 'utf-8'))
                        except socket.timeout:
                            continue
                        except OSError:
                            if self.running.is_set():
                                raise
                    
                except socket.timeout:
                    continue
                

    def parse_msg(self, msg):
        print(msg)


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