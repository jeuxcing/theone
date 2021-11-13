import subprocess as sp
import sys
import serial
import time
from threading import Thread, Lock


class SerialManager(Thread):

    def __init__(self, serial_id, verbose=False):
        super().__init__()
        self.arduinos = {}
        self.list_arduinos()
        # self.current_port = 5555
        self.ended = False
        self.serial_id = serial_id
        self.serial = None
        self.inbox = []
        self.outbox = {}
        self.waitbox = None
        self.outbox_size = 0
        self.current_dest = None
        # self.redirector = None
        self.on_event_functions = []
        self.verbose = verbose
        self.outbox_mutex = Lock()



    def add_handeling_function(self, function):
        self.on_event_functions.append(function)


    def send_msg(self, msg, max_size=32):
        # Add the message size
        # msg = [len(msg)] + list(msg.iterbytes())
        self.outbox_mutex.acquire()
        msg = [len(msg) + 1] + [int.from_bytes(msg[i:i+1], "big") for i in range(len(msg))]
        if (self.verbose):
            print("send_msg(",msg,")")
        dest = msg[2]
        # outbox destination check
        if dest not in self.outbox:
            self.outbox[dest] = [bytes(msg)]
            self.outbox_size += 1
        # Case of first msg
        elif len(self.outbox[dest]) == 0:
            self.outbox[dest].append(bytes(msg))
            self.outbox_size += 1
        # Case of multiple messages
        else:   
            last_msg = self.outbox[dest][-1]
            last_msg = [int.from_bytes(last_msg[i:i+1], "big") for i in range(len(last_msg))]
            # last_msg = [int.from_bytes(b, "big") for b in self.outbox[dest][-1]]
            # Not a multiple message => Create a multiple message
            if last_msg[1] != ord('M'):
                size = last_msg[0]
                last_msg = [4 + size, ord('M'), dest, 1] + last_msg
                self.outbox[dest] = self.outbox[dest][:-1]
                self.outbox[dest].append(bytes(last_msg))
            # Complete the last message ?
            new_size = last_msg[0] + msg[0]
            if new_size <= max_size:
                last_msg.extend(msg) # Add the new msg at the end
                last_msg[0] = new_size # Change the global message size
                last_msg[3] += 1 # Change the number of messages in the multi-msg
                self.outbox[dest] = self.outbox[dest][:-1]
                self.outbox[dest].append(bytes(last_msg))
            else:
                print("large message")
                self.outbox[dest].append(bytes(msg))
                self.outbox_size += 1
        self.outbox_mutex.release()


    def list_arduinos(self):
        # sys call to read kernel messages
        dmesg = ["sudo", "dmesg"]
        val = str(sp.run(dmesg, capture_output=True))
        # split messages related to arduino
        lines = val.split("\\n")
        for idx, line in enumerate(lines):
            if ("USB ACM device" in line):
                port = line.split(":")[-2][1:]
                serial = lines[idx-1].split(" ")[-1]
                self.arduinos[serial] = port


    def run(self):
        acknowledged = True
        while not self.ended:
            # find the arduino
            if self.serial == None:
                self.list_arduinos()
                # when arduino absent
                if self.serial_id not in self.arduinos:
                    if self.verbose:
                        print(f"T Arduino {self.serial_id} not plugged")
                    time.sleep(1)
                    continue

                # Opent the serial
                try:
                    self.serial = serial.Serial(f"/dev/{self.arduinos[self.serial_id]}", baudrate=115200)
                except serial.serialutil.SerialException:
                    self.serial = None
            # Communicate with arduinos
            else:
                try:
                    if len(self.inbox) > 10 or self.outbox_size > 10:
                        print("T Mailbox warning: <", len(self.inbox), "   >", self.outbox_size)
                    # Write to device

                    self.outbox_mutex.acquire()
                    if acknowledged and self.outbox_size > 0:
                        msg = None
                        for dest in self.outbox:
                            if len(self.outbox[dest]) > 0:
                                msg = self.outbox[dest][0]
                                self.current_dest = dest
                                break
                        if self.verbose:
                            print("T send:", msg)
                        self.last_send = time.time()
                        self.serial.write(msg)
                        self.serial.flush() # Rayan: useful?
                        if self.waitbox != None:
                            print("waitbox already full")
                        self.waitbox = msg
                        self.outbox[self.current_dest] = self.outbox[self.current_dest][1:]
                        self.outbox_size -= 1
                        acknowledged = False
                    elif (not acknowledged and time.time() - self.last_send > 5): 
                                                            #Wait delay before sending next packet batch
                                                            # ie minimum time before 2 exchanges of packets
                        acknowledged = True
                    self.outbox_mutex.release()

                    # Read from device
                    for i in range(min(100, self.serial.in_waiting)):
                        self.inbox.append(self.serial.read())

                    while len(self.inbox) > 0:
                        size = int.from_bytes(self.inbox[0], "big")
                        if size <= len(self.inbox) - 1:
                            msg = self.inbox[1:size+1]
                            self.inbox = self.inbox[size+1:]

                            if self.verbose:
                                print("T recv:", msg)

                            if not acknowledged and int.from_bytes(msg[0], "big") == 0xFF:
                                if self.verbose:
                                    print("T ack [latency", time.time() - self.last_send, "]")
                                self.outbox_mutex.acquire()
                                self.waitbox = None
                                self.outbox_mutex.release()
                                acknowledged = True
                                continue

                            for function in self.on_event_functions:
                                function("T msg", msg)
                        else:
                            break
                except serial.serialutil.SerialException:
                    self.serial = None
                except Exception as e:
                    self.serial = None
                    print(e, file=sys.stderr)

            time.sleep(0.0001)
        if self.verbose:
            print("T Serial Closed")


    def stop(self):
        self.ended = True
        if self.serial is not None:
            self.serial.close()
