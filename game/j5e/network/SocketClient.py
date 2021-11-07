import socket
import time
from threading import Thread


class SocketClient(Thread):

    def __init__(self, verbose=False):
        super().__init__()

        self.port = 6000
        self.stopped = False
        self.mailbox = []
        self.inbox = []
        self.msg_handlers = []
        self.verbose = verbose


    def port_event(self, event_name, attrs):
        if event_name == "connect":
            self.port = attrs[1]


    def register_msg_handler(self, function):
        self.msg_handlers.append(function)


    def send(self, msg):
        # print(len(msg), msg)
        self.mailbox.append(msg)


    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            while not self.stopped:
                try:
                    current_port = self.port
                    sock.setblocking(1)
                    sock.connect(("127.0.0.1", current_port))
                    sock.settimeout(0.05)
                    if self.verbose:
                        print(f"Socket opened on port {current_port}")
                    acknowledged = True
                    last_send = 0.
                    while current_port == self.port and not self.stopped:
                        # receive messages
                        data = None
                        try:
                            for i in range(100):
                                byte = sock.recv(1)
                                self.inbox.append(byte)
                        except socket.timeout:
                            pass

                        while len(self.inbox) > 0:
                            # Is there a full message ?
                            size = int.from_bytes(self.inbox[0], "big")
                            if size > len(self.inbox)-1:
                                break

                            # Transmit message
                            data = self.inbox[:size+1]
                            self.inbox = self.inbox[size+1:]

                            val = int.from_bytes(data[1], "big")
                            if size == 1 and val == 0xFF:
                                self.mailbox = self.mailbox[1:]
                                acknowledged = True
                            if self.verbose:
                                print("receiving:", data)
                            for function in self.msg_handlers:
                                function(data)

                        # send messages from the mailbox
                        msg = None
                        print("POUET", len(self.mailbox), acknowledged, -last_send + time.time())
                        if len(self.mailbox) > 0 and acknowledged:
                            msg = self.mailbox[0]
                        elif not acknowledged and time.time() - last_send > .1:
                            msg = self.mailbox[0]

                        if msg is not None:
                            sock.setblocking(1)
                            if self.verbose:
                                print(f"sending: {msg}")
                            acknowledged = False
                            last_send = time.time()
                            sock.send(bytes([len(msg)]))
                            sock.send(msg)
                            sock.settimeout(0.05)


                except ConnectionRefusedError:
                    if self.verbose:
                        print(f"Connexion refused on port {self.port}")
                    time.sleep(1)
                    continue
        if self.verbose:
            print("Socket closed")
    

    # def run(self):
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    #         while not self.stopped:
    #             try:
    #                 current_port = self.port
    #                 sock.setblocking(1)
    #                 sock.connect(("127.0.0.1", current_port))
    #                 sock.settimeout(0.05)
    #                 if self.verbose:
    #                     print(f"Socket opened on port {current_port}")
    #                 acknowledged = True
    #                 last_send = 0.
    #                 while current_port == self.port and not self.stopped:
    #                     # receive messages
    #                     data = None
    #                     try:
    #                         for i in range(100):
    #                             byte = sock.recv(1)
    #                             self.inbox.append(byte)
    #                     except socket.timeout:
    #                         pass

    #                     while len(self.inbox) > 0:
    #                         # Is there a full message ?
    #                         size = int.from_bytes(self.inbox[0], "big")
    #                         if size > len(self.inbox)-1:
    #                             break

    #                         # Transmit message
    #                         data = self.inbox[:size+1]
    #                         self.inbox = self.inbox[size+1:]

    #                         val = int.from_bytes(data[1], "big")
    #                         if size == 1 and val == 0xFF:
    #                             self.mailbox = self.mailbox[1:]
    #                             acknowledged = True
    #                         if self.verbose:
    #                             print("receiving:", data)
    #                         for function in self.msg_handlers:
    #                             function(data)

    #                     # send messages from the mailbox
    #                     msg = None
    #                     print("POUET", len(self.mailbox), acknowledged, -last_send + time.time())
    #                     if len(self.mailbox) > 0 and acknowledged:
    #                         msg = self.mailbox[0]
    #                     elif not acknowledged and time.time() - last_send > .1:
    #                         msg = self.mailbox[0]

    #                     if msg is not None:
    #                         sock.setblocking(1)
    #                         if self.verbose:
    #                             print(f"sending: {msg}")
    #                         acknowledged = False
    #                         last_send = time.time()
    #                         sock.send(bytes([len(msg)]))
    #                         sock.send(msg)
    #                         sock.settimeout(0.05)


    #             except ConnectionRefusedError:
    #                 if self.verbose:
    #                     print(f"Connexion refused on port {self.port}")
    #                 time.sleep(1)
    #                 continue
    #     if self.verbose:
    #         print("Socket closed")

    def stop(self):
        self.stopped = True