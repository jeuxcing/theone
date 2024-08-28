from select import select
import socket

from threading import Thread
import multiprocessing
from time import sleep
import time
from queue import Queue, Full

import requests
from flask import Flask, send_from_directory, send_file, request, Response



class ServerFlask:

    def __init__(self, port=8080):
        self.port = port
        self.app = Flask('Flask server')
        self.clients = []
        self.msgs_to_webclients = Queue()
        self.client_msg_queues = {}
        self.game_connect = ConnectionToGame(self.msgs_to_webclients)
        self.game_connect.start()

    def start(self):
        self.init()
        def thread_fun():
            self.app.run(host='0.0.0.0', port=self.port, threaded=True)
        self.thread = Thread(target=thread_fun)
        self.thread.start()
        
    def stop(self):
        # requests.post(f'http://127.0.0.1:{self.port}/shutdown')
        self.game_connect.stop()
        self.game_connect.join()
        

    def init(self):
        @self.app.route('/shutdown', methods=['POST'])
        def shutdown():
            shutdown_func = request.environ.get('werkzeug.server.shutdown')
            if shutdown_func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            shutdown_func()
            return 'Server shutting down...'
        
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
                    self.game_connect.send_msg(key)
            return 'Ok'

        @self.app.route('/gameStatus')    
        def gameUpdate():
            print("SSE request received")
            client = request.environ['wsgi.input']
            # Ajouter la boite de message du client
            self.clients.append(client)
            self.client_msg_queues[client] = Queue()

            def event_handler():
                nonlocal client

                try:
                    while True:
                        if not self.msgs_to_webclients.empty():
                            # Récupérer le message général en attente
                            msg = self.msgs_to_webclients.get()
                            # Ajouter ce message dans toutes les boites des clients
                            for client_name in self.clients:
                                self.client_msg_queues[client_name].put_nowait(msg)

                        # Traiter le premier message de ma boite client
                        if not self.client_msg_queues[client].empty():
                            msg = self.client_msg_queues[client].get()
                            msg = f"data: {msg}\n\n"
                            # print("MESSAGE", msg)
                            yield msg

                        time.sleep(.01)
                except GeneratorExit:
                    self.clients.remove(client)

            # return Response(stream_with_context(event_stream()), content_type='text/event-stream')
            return Response(event_handler(), mimetype='text/event-stream')
        
        
        
class ConnectionToGame(Thread):
    def __init__(self, msg_queue, ip="127.0.0.1", port=65432):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.letterbox = []
        self.stopped = False
        self.from_game = None
        self.update_port = 8087
        self.msg_queue = msg_queue

    def send_msg(self, msg):
        print(hex(id(self)))
        self.letterbox.append(msg)
        print(len(self.letterbox), self.letterbox)

    def stop(self):
        if self.from_game is not None:
            self.from_game.stop()
            self.from_game.join()
        
        self.stopped = True

    def send_letterbox(self, socket):
        # Envoie les commandes en attente
        to_send, self.letterbox = self.letterbox, []

        for val in to_send:
            print("sending:", val)
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
                    self.from_game = ConnectionFromGame(self.update_port, self.msg_queue)
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

    def __init__(self, port, msg_queue):
        Thread.__init__(self)
        self.socket = None
        self.stopped = False
        self.port = port
        self.msg_queue = msg_queue

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
                    conn.settimeout(0.01)

                    while not self.stopped:
                        try:
                            data = conn.recv(1024)
                            if not data:
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
        self.msg_queue.put_nowait(msg)
        print(msg)

