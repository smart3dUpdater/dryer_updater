import zmq
from zmq.eventloop import zmqstream
import logging

class ArduinoBoardSubscriber:

    def __init__(self, board_controller=None):
        context = zmq.Context()
        self.arduino_logger = logging.getLogger('arduino_data_logger')
        self.topic_status = 'status'
        self.topic_received = 'command'
        self.port = '5560'
        self.socket = context.socket(zmq.SUB)
        self.socket.setsockopt(zmq.LINGER, 20)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic_status)
        self.socket.setsockopt_string(zmq.SUBSCRIBE, self.topic_received)
        self.socket.connect("tcp://localhost:%s" % self.port)
        self.stream_sub = zmqstream.ZMQStream(self.socket)
        self.stream_sub.on_recv(self.receive)
        self.command_receive = None
        self.status = None
        self.board_controller = board_controller

    def receive(self, data):
        #topic, messagedata = data[0].split()
        command = data[0].split()[0]
        board_data = data[0].split()[1]
        if command == b'status' and self.board_controller:
            self.board_controller.set_status(board_data.decode('ascii', 'ignore'))
        print(data)
        self.arduino_logger.info(str(data))
