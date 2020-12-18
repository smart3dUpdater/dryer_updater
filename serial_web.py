from base.application import ApplicationSerial
from tornado.ioloop import IOLoop
from utils import init_logger

init_logger('serial_connector')

if __name__ == "__main__":
    app = ApplicationSerial()
    app.listen(8887)
    IOLoop.instance().start()