from tornado.ioloop import IOLoop
from base.updater import ZmqUpdater

if __name__ == "__main__":
    ZmqUpdater()
    IOLoop.instance().start()