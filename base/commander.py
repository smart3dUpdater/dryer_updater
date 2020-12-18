import zmq
from zmq.eventloop import zmqstream

# Recibe los mensajes que le envia la aplicación Web para la Arduino
class ZmqCommander:

    def __init__(self, board):
        self.board = board
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.setsockopt(zmq.LINGER, 20)
        self.socket.bind("tcp://*:%s" % '5570')
        self.stream_pull = zmqstream.ZMQStream(self.socket)
        self.stream_pull.on_recv(self.zmq_command)

    def zmq_command(self, command):
        print(command)
        if b'on' in command[0]:
            self.board.preassure_on(command[0].split()[1])
        elif b'temp' in command[0]:
            self.board.set_temperature(command[0].split()[1])
        elif b'off' in command[0]:
            self.board.preassure_off()
        elif b'status' in command:
            self.board.status()
        self.socket.send_string('recibido')

class ZmqCommanderSender:

    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.PAIR)
        self.socket.setsockopt(zmq.LINGER, 20)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.connect("tcp://localhost:%s" % '5570')

#envia las ordenes al ZmqCommander de la aplicacion serie
class ArduinoZmqSender(ZmqCommanderSender):

    def status(self):
        self.socket.send(b'status')

    def on(self, pressure):
        self.socket.send('on {}'.format(pressure).encode())
    
    def off(self):
        self.socket.send(b'off')

    def temp(self, temp):
        self.socket.send('temp {}'.format(temp).encode())

class UpdateSender:
    
    def __init__(self):
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.setsockopt(zmq.LINGER, 20)
        self.socket.connect("tcp://localhost:%s" % '5590')

    def make_update(self):
        #TODO: Pegar el supervisord.conf y con el control reiniciar todo
        self.socket.send(b'update')
        resp = self.socket.recv_string()
        return resp