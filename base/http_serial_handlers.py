from base.http_basic import BasicHandler

class CicladoOnHandler(BasicHandler):
    def get(self, temp):
        self.write('ok')

class CicladoOffHandler(BasicHandler):
    def get(self):
        self.write('ok')

class FirstStatusHandler(BasicHandler):
    def get(self):
        get_board = False
        if self.application.board_arduino:
            get_board = True
        self.write({'status': get_board})