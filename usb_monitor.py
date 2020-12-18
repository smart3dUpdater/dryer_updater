import pyudev
import zmq
import logging

log_folder = "/home/pi/logs"
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
usb_monitor_logger = logging.getLogger('usb_monitor_logger')
usb_monitor_hdlr = logging.FileHandler('{}/usb_monitor_log.txt'.format(log_folder))
usb_monitor_hdlr.setFormatter(formatter)
usb_monitor_logger.addHandler(usb_monitor_hdlr)
usb_monitor_logger.setLevel(logging.INFO)

class ZmqConnector():

    def __init__(self):
        self.context = zmq.Context()
        self.port_board = '5556'
        self.sock_board = self.context.socket(zmq.PAIR)
        self.sock_board.connect("tcp://localhost:%s" % self.port_board)
        self.port_flash = '5557'
        self.sock_flash = self.context.socket(zmq.PAIR)
        self.sock_flash.connect("tcp://localhost:%s" % self.port_flash)

    def send_board(self, info):
        self.sock_board.send_string(info)

    def send_flash(self, info):
        self.sock_flash.send_string(info)

if __name__ == "__main__":
    zmqConnector = ZmqConnector()
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='tty')
    monitor.filter_by(subsystem='block')
    monitor.start()
    for dev in iter(monitor.poll, None):
        if dev.action == 'add':
            device = dict(dev)
            if device['SUBSYSTEM'] == 'tty':
                usb_monitor_logger.info('Board detected: {} - {}'.format(device['ID_USB_DRIVER'], device['ID_VENDOR_FROM_DATABASE']))
                zmqConnector.send_board(device['DEVNAME'])
            elif device['SUBSYSTEM'] == 'block' and device['DEVTYPE'] == 'partition':
                zmqConnector.sock_flash(device['DEVNAME'])
