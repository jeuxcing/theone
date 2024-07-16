from select import select
import socket

from threading import Thread
from time import sleep
import time


from flask import Flask, send_from_directory, send_file, request, Response



class ServerFlask:

    def __init__(self):
        self.app = Flask('Test flask')
        self.game = ConnectionToGame()
        self.game.start()

    def start(self):
        self.init()
        self.app.run(host='0.0.0.0', port=8080, debug=True)

    def init(self):
        @self.app.route('/<path:path>')
        def send_www(path):
            return send_from_directory('j5e/game/panelAdmin/www', path)
        
        @self.app.route('/')
        def send_index():
            return send_file('j5e/game/panelAdmin/www/index.html')
            
        @self.app.get('/gamemsg')
        def gamemsg():
        #localhost:xxx/gamemsg?play
            liste_de_cmd = frozenset(["play", "pause", "reset", "rotation"])
            for key in request.args.keys():
                if key in liste_de_cmd:                
                    self.game.send_msg(key)
            return 'Ok'

        @self.app.route('/gameStatus')    
        def gameUpdate():
            def event_handler():
                while True:
                    time.sleep(5)
                    yield "coucou"

            return Response(event_handler(), mimetype='text/event-stream')
        
        
        
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


