from tornado import web
from base.handler_list import serial_handlers, web_handlers
from base.board.board_arduino import BoardArduino
from base.board.board_controller import ArduinoController
from base.board.board_discover import *
from base.commander import ZmqCommander, ArduinoZmqSender, UpdateSender
from base.event_handler.arduino_handler import ZmqArduinoHandler
from base.db_connection import DbConnection
import logging
import zmq
from base.board.board_subscriber import ArduinoBoardSubscriber
from tornado.ioloop import PeriodicCallback

log_folder = "/home/pi/logs"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
logger = logging.getLogger('arduino_data_logger')
connector_hdlr = logging.FileHandler('{}/arduino_data_logger_log.txt'.format(log_folder))
connector_hdlr.setFormatter(formatter)
logger.addHandler(connector_hdlr)
logger.setLevel(logging.DEBUG)


class ApplicationSerial(web.Application):
    def __init__(self):
        web.Application.__init__(self, serial_handlers)
        logger = logging.getLogger('serial_connector_logger')
        self.board_arduino = None
        try:
            #self.discoverer = BoardDiscoverer()
            #self.board_arduino = BoardArduino(115200, self.discoverer.my_board['DEVNAME'])
            self.board_arduino = BoardArduino(115200, '/dev/ttyAMA0')
            self.commander = ZmqCommander(self.board_arduino)
            handler = ZmqArduinoHandler()
            self.board_arduino.add_event_handler(handler)
        except MoreThanOneBoardException:
            #TODO: enviar zmq con mensaje de error
            logger.error("More than one board founded")
        except NoBoardException:
            #TODO: enviar zmq con mensaje de error
            logger.error("No board founded")
        except BoardJsonFoundedException:
            #TODO: enviar zmq con mensaje de error
            logger.error("Found a json, please remove")

class ApplicationWeb(web.Application):
    def __init__(self):
        web.Application.__init__(self, web_handlers, template_path="/home/pi/software/templates/")
        self.logger = logging.getLogger('server_logger')
        #context = zmq.Context()
        #socket = context.socket(zmq.REQ)
        #socket.setsockopt(zmq.RCVTIMEO, 500)
        ## IMPORTANT!! Without this, zmq hangs the entire application
        #socket.setsockopt(zmq.LINGER, 20)
        #socket.connect("tcp://localhost:%s" % '5580')
        #socket.send_string('status')
        #self.my_board = False
        #try:
        #    resp = socket.recv_string()
        #    if resp == 'board':
        #        self.my_board= True
        #except:
        #    self.logger.error('Timeout serial response')
        #finally:
        #    socket.close()
        #TODO: Change this for a real verification!!
        self.my_board= True
        self.arduino_sender = ArduinoZmqSender()
        self.board_controller = ArduinoController(self.arduino_sender)
        self.arduino_subs = ArduinoBoardSubscriber(board_controller=self.board_controller)
        self.updater = UpdateSender()
        self.db = DbConnection()
        self.where = 'home'
        self.periodic_callback = PeriodicCallback(self.arduino_sender.status, 5000)
        self.periodic_callback.start()
