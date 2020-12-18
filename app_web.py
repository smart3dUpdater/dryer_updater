from utils import init_logger, verifications
from base.application import ApplicationWeb
from tornado.ioloop import IOLoop

init_logger('server')
verifications()

if __name__ == "__main__":
    app = ApplicationWeb()
    app.listen(8888)
    IOLoop.instance().start()