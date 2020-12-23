import os
import subprocess
import zmq
from zmq.eventloop import zmqstream
from socket import create_connection, gethostbyname


git_path = f'{os.getcwd()}/software'

def bash_command(cmd='', path = '.'):
    pipe = subprocess.Popen(cmd, shell=True, cwd=path,stdout = subprocess.PIPE,stderr = subprocess.PIPE )
    (out, error) = pipe.communicate()
    pipe.wait()
    return {'out':out.decode("utf-8"),'error':error.decode("utf-8")}

def check_connection():
    try:
        gethostbyname('www.google.com')
        testConn = create_connection(('www.google.com', 80),1)
        print ("Connection OK")
        testConn.close()
        return True
    except Exception as error:
        print(error)
        return False

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
        if process.get('error') != '':
            self.streamer.send_string(f'error: ' + process.get('error'))
        else:
            self.streamer.send_string(process.get('out'))

    def check_update(self):
        pass

    def make_update_to_master(self):
        # try:
        #     print('pasamos por acá:...')
        #     process = subprocess.run(['cd', '/home/pi/software','&','git', 'pull'], stdout=subprocess.PIPE, 
        #             stderr=subprocess.STDOUT, universal_newlines=True, shell=True, check=True)
        # except:
        #     print('pasamos por acá tambien :/...')
        #     process = subprocess.run(['git', 'pull'], stdout=subprocess.PIPE, 
        #             stderr=subprocess.STDOUT, universal_newlines=True)

        # if process.returncode == 0:
        #     check = subprocess.run(['sudo', 'cp', 'supervisord.conf', '/etc/supervisor/supervisord.conf'],
        #         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,shell=True, check=True)
        #     #supervisorctl -c /etc/supervisor/supervisord.conf update
        #     print(check)
        #     check = subprocess.run(['supervisorctl', '-c', '/etc/supervisor/supervisord.conf', 'update'],
        #         stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True,shell=True, check=True)
        #     print(check)
        update_available_msg = 'On branch main\nYour branch is behind \'origin/main\' by'
        up_to_date = 'On branch main\nYour branch is up to date'
        error_msg = 'Error: update could not be performed, please try again later'
        try:
            if check_connection() == False:
                raise Exception('Not internet connection')
            bash_command('git fetch', git_path)
            process = bash_command('git status', git_path)
            if process.get('error') != '':
                return process
            elif process.get('out').find(update_available_msg) != -1:
                process = bash_command('git pull', git_path)
                process = bash_command('git status', git_path)
                if process.get('out').find(up_to_date) != -1:
                    bash_command('nohup  bash -c "sleep 10; shutdown -r -t now"', git_path)
                    tag = bash_command('git tag', git_path)
                    last_tag = tag.get('out')[-7:-1]  
                    return {'out': f'The system has been updated to {last_tag}, restarting ...', 'error': ''}
                else:
                    return {'out': '', 'error': error_msg}
            elif process.get('out').find(up_to_date) != -1:
                tag = bash_command('git tag', git_path)
                last_tag = tag.get('out')[-7:-1]
                return {'out': f'System is up to date {last_tag}', 'error': ''}
            else:
                return process
        except Exception as e:
            return {'out': '', 'error': f'{error_msg}\n Traceback: {e}'}