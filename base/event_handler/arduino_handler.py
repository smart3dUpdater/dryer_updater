import zmq

#envia los mensajes a la aplicación web
class ZmqArduinoHandler():

    def __init__(self):
        self.port = "5560"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.PUB)
        self.socket.bind("tcp://*:%s" % self.port)
        self.topic_status = 'status'
        self.topic_received = 'command'

    def send(self, data):
        if data.startswith('<T'):
            self.socket.send_string("{} {}".format(self.topic_status, data))
        elif data.startswith('<Received'):
            self.socket.send_string("{} {}".format(self.topic_received, data))

class HttpArduinoHandler():

    def __init__(self):
        pass

    def send(self, data):
        pass