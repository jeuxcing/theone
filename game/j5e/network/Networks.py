from j5e.network.SerialManager import SerialManager
from j5e.network.SocketClient import SocketClient


class Networks:

    # To know the serial number of an arduino (linux only):
    # 1 - plug the arduino to the computer usb
    # 2 - sudo dmesg
    # 3 - read the last "SerialNumber"

    # The following 2 values needs to be changed regarding the arduino used
    wall_serial = "758333139333512021D2"
    ctrl_serial = "POUET"
    # ctrl_serial = "758303339383511090A1"


    def __init__(self):
        # Init connections to the wall
        self.wall = SerialManager(Networks.wall_serial, verbose=True)

        # Init connections to the controller
        self.ctrl = SerialManager(Networks.ctrl_serial)

        # run threads
        self.wall.start()
        self.ctrl.start()


    def ctrl_msg_register(self, function):
        """ function is registered to be called when a message arrives
        """
        self.ctrl.register_msg_handler(function)


    def stop(self):
        self.wall.stop()
        self.ctrl.stop()

        self.wall.join()
        self.ctrl.join()