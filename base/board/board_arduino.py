from serial import Serial, SerialException
import threading
from base.board.board import Board

class BoardArduino(Board):
    
    #TODO: hacer mas completo filtrando y parceando
    def preassure_on(self, prea):
        data = '<ON {}>'.format(prea.decode('ascii', 'ignore'))
        print(data)
        self.send(data)

    def preassure_off(self):
        self.send('<OFF>')

    def status(self):
        self.send('<STATUS>')

    def set_temperature(self, temp):
        data = '<TEMP {}>'.format(temp.decode('ascii', 'ignore'))
        print(data)
        self.send(data)


    
