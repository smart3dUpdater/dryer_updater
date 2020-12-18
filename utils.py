import logging
import os
import shutil
import json
from subprocess import check_output
from tornado.gen import coroutine, sleep
import collections

DB_PATH_GIT = '/home/pi/software'
DB_PATH = '/home/pi/db'
DB_FILE = '/base_db.db'
JSON_CONFIG = '/config.json'
JSON_CONFIG_PATH = '/home/pi/config-files'

def init_logger(logger_name):
    log_folder = "/home/pi/logs"
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    logger = logging.getLogger('{}_logger'.format(logger_name))
    connector_hdlr = logging.FileHandler('{}/{}_log.txt'.format(log_folder, logger_name))
    connector_hdlr.setFormatter(formatter)
    logger.addHandler(connector_hdlr)
    logger.setLevel(logging.INFO)

def verifications():
    if not os.path.exists(DB_PATH):
        os.mkdir(DB_PATH)
    if not os.path.exists(DB_PATH + DB_FILE):
        shutil.copyfile(DB_PATH_GIT + DB_FILE, DB_PATH + DB_FILE)
    if not os.path.exists(JSON_CONFIG_PATH):
        os.mkdir(JSON_CONFIG_PATH)
    if not os.path.exists(JSON_CONFIG_PATH + JSON_CONFIG):
        shutil.copyfile(DB_PATH_GIT + JSON_CONFIG, JSON_CONFIG_PATH + JSON_CONFIG)

def get_interface_connected():
    try:
        return check_output('route', universal_newlines=True).split('\n')[-2].split()[-1]
    except:
        return ''

def get_active():
    with open(JSON_CONFIG_PATH + JSON_CONFIG) as f:
        return json.load(f)['active']

def set_active(id):
    with open(JSON_CONFIG_PATH + JSON_CONFIG, 'w') as f:
        json.dump({'active': int(id)}, f)

@coroutine
def connect_private_wifi(network_name, password):
    network_number = int(check_output("wpa_cli add_network | grep -v \"Selected interface 'p2p-dev-wlan0'\"", shell=True, universal_newlines=True))
    os.system("sudo wpa_cli set_network {} ssid '\"{}\"'".format(network_number, network_name))
    os.system("sudo wpa_cli set_network {} psk '\"{}\"'".format(network_number, password))
    os.system("sudo wpa_cli enable_network {}".format(network_number))
    os.system("sudo wpa_cli select_network {}".format(network_number))
    os.system("sudo wpa_cli save_config")
    os.system("sudo wpa_cli -i wlan0 reconfigure")
    yield sleep(15)
    return wifi_connected()

def wifi_connected():
    return check_output("iwgetid wlan0 --raw", shell=True, universal_newlines=True).strip()

@coroutine
def connect_to_wifi(network_name, password=None):
    result = ''
    if password:
        result = yield connect_private_wifi(network_name, password)
        print('!!!!!!!!! RESULTADO: {}'.format(result))
    return result

def scan_wlan():
    scanoutput = check_output("sudo iwlist wlan0 scan | grep 'SSID\|Quality' | tr -s ' '", shell=True, universal_newlines=True)
    ssid_dict = {x.split('ESSID:"')[1].split('"')[0]: x.split('=')[1].split('/')[0] for x in scanoutput.split('Quality') if x.strip()}
    ssid_dict = {k : v for k, v in ssid_dict.items() if k}
    return list(collections.OrderedDict(sorted(ssid_dict.items(), key=lambda t: t[1], reverse=True)).keys())

def get_my_ip():
    return check_output("ifconfig -a | awk '$1==\"inet\" && $5==\"broadcast\"{print $2}'", shell=True, universal_newlines=True)

def get_my_ips():
    wifi_command = ''' ifconfig wlan0 | grep "inet " | awk -F'[: ]+' '{ print $3 }' '''
    eth_command = ''' ifconfig eth0 | grep "inet " | awk -F'[: ]+' '{ print $3 }' '''
    ip_wifi = check_output(wifi_command, shell=True, universal_newlines=True).strip()
    ip_eth = check_output(eth_command, shell=True, universal_newlines=True).strip()
    if ip_eth and not ip_wifi:
        ip_wifi = ip_eth
    return (ip_wifi, ip_eth)
