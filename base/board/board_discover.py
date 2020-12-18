import pyudev
import os
import json
import zmq
from zmq.eventloop import zmqstream

class BoardDiscoverer:
    
    BOARD_PATH = "/home/pi/config-files/board.json"

    def __init__(self):
        self.boards = []
        self.max_boards = 3
        self.my_board = None
        if os.path.exists(self.BOARD_PATH):
            with open(self.BOARD_PATH) as f:
                self.my_board = json.load(f)
                self.check_my_board()           
        else:
            self.discover_my_board_first_time()
        context = zmq.Context()
        self.socket = context.socket(zmq.REP)
        self.socket.setsockopt(zmq.LINGER, 20)
        self.socket.bind("tcp://*:%s" % '5580')
        self.stream_pull = zmqstream.ZMQStream(self.socket)
        self.stream_pull.on_recv(self.status)

    def status(self, ask):
        if self.my_board:
            self.socket.send_string('board')
        else:
            self.socket.send_string('no-board')


    def get_devices(self):
        context = pyudev.Context()
        devices = []
        for dev in context.list_devices(subsystem='tty', ID_BUS='usb'):
            devices.append(dict(dev))
        return devices      

    def get_my_board(self):
        """
        Discover the board main at first time and storage data on a file
        Raise an exception if can not save the json
        """
        devices = self.get_devices()
        if len(devices) > 1:
            raise MoreThanOneBoardException()
        elif len(devices) == 0:
            raise NoBoardException()
        elif len(devices) == 1:
            self.save_board(devices[0])
    
    def discover_my_board_first_time(self):
        if not os.path.exists(self.BOARD_PATH):
            self.get_my_board()
        else:
            raise BoardJsonFoundedException()

    def save_board(self, device):
        with open(self.BOARD_PATH, 'w') as f:
            self.my_board = device
            json.dump(device, f)
    
    def check_my_board(self):
        for dev in self.get_devices():
            if self.my_board['ID_VENDOR'] == dev['ID_VENDOR'] and self.my_board['ID_SERIAL'] == dev['ID_SERIAL'] and \
                self.my_board['ID_MODEL_ID'] == dev['ID_MODEL_ID']:
                if self.my_board['DEVNAME'] != dev['DEVNAME']:
                    self.save_board(dev)
                    break


class MoreThanOneBoardException(Exception):
   """Base class for other exceptions"""
   pass

class NoBoardException(Exception):
   """Base class for other exceptions"""
   pass

class BoardJsonFoundedException(Exception):
   """Base class for other exceptions"""
   pass