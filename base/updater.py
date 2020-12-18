import subprocess
import zmq
from zmq.eventloop import zmqstream

class ZmqUpdater:

    def __init__(self):
        context = zmq.Context()
        socket = context.socket(zmq.REP)
        socket.setsockopt(zmq.LINGER, 20)
        socket.bind("tcp://*:%s" % '5590')
        self.streamer = zmqstream.ZMQStream(socket)
        self.streamer.on_recv(self.command)

    def command(self, command):
        print(command)
        if command[0] == b'update':
            process = self.make_update_to_master()
            if process.returncode != 0:
                self.streamer.send_string('error: ' + process.stdout)
            else:
                self.streamer.send_string('ok')

    def check_update(self):
        pass

    def make_update_to_master(self):
        process = subprocess.run(['git', 'pull', 'origin', 'master'], stdout=subprocess.PIPE, 
                    stderr=subprocess.STDOUT, universal_newlines=True)
        if process.returncode == 0:
            subprocess.run(['sudo', 'cp', 'supervisord.conf', '/etc/supervisor/supervisord.conf'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
            #supervisorctl -c /etc/supervisor/supervisord.conf update
            subprocess.run(['supervisorctl', '-c', '/etc/supervisor/supervisord.conf', 'update'],
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
        return process
