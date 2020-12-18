from serial import Serial, SerialException, PARITY_ODD, PARITY_NONE, EIGHTBITS
import threading
import logging

#TODO: Poner todos los try que faltan
class Board:

    def __init__(self, baud=None, port=None):
        self.arduino_logger = logging.getLogger('arduino_data_logger')
        self.serial = Serial(timeout=10.0)
        self.read_thread = None
        self.continue_reading = True
        self.event_handler = []
        if port and baud:
            self.connect(baud, port)

    #Sirve para recibir los mensajes de la placa
    def add_event_handler(self, handler):
        self.event_handler.append(handler)
    
    def connect(self, baud, port):
        self.serial.baudrate = baud
        self.serial.port = port
        self.serial.open()
        #self.serial = Serial(port = port,
        #        baudrate = baud,
        #        timeout = 0.25,
        #        parity = PARITY_ODD,
        #        bytesize = EIGHTBITS)
        #self.serial.close()
        #self.serial.open()
        self.read_thread = threading.Thread(target = self.read)
        self.read_thread.start()
        return self.serial.is_open

    def disconnect(self):
        #if threading.current_thread() != self.read_thread:
        #    self.read_thread.join()
        self.continue_reading = False
        # According this doc: https://www.bogotobogo.com/python/Multithread/python_multithreading_Daemon_join_method_threads.php
        # Put timeout, check of necesary
        self.read_thread.join(1.0)
        self.read_thread = None
        self.serial.close()
        resp = not self.serial.is_open
        self.serial = None
        return resp

    def read(self):
        while self.continue_reading:
            line = self.serial.readline().decode('ascii', 'ignore')
            self.arduino_logger.info("Arduino: {}".format(str(line)))
            for handler in self.event_handler:
                handler.send(line)

    def send(self, data):
        self.arduino_logger.info(str(data))
        self.serial.write(data.encode('ascii'))
