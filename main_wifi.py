import sys
import json
import os
import datetime
from time import sleep
from subprocess import Popen, PIPE


MACS_CONNECTED = set()

FILE_NAME = datetime.datetime.now().strftime('%d-%m-%Y') + '_' + 'wifi' + '.txt'
FILE_PATH = os.path.abspath(os.path.dirname(sys.argv[0])) + '/'


def colorful_print(msg, color):
    print(color + msg + Colors.END)


def get_wifi_score():
    global MACS_CONNECTED
    wifi_score_command = ['sudo', '/usr/bin/ndsctl', 'json']
    score_process = Popen(wifi_score_command, stdout=PIPE)
    stdout = score_process.communicate(timeout=30)
    response = json.loads(stdout[0].decode('utf-8'))
    score_connected = response['client_length']

    if score_connected > 0:
        score = 0
        for client in response['clients']:
            if response['clients'][client]['state'] == 'Authenticated':
                score += 1
                MACS_CONNECTED.add(client)

    read_macs = set()

    try:
        with open(FILE_NAME, 'r') as f:
            index = 0
            for line in f.readlines():
                if index != 0:
                    read_macs.add(line.strip())
                index += 1
    except FileNotFoundError:
        pass

    mac_totals = MACS_CONNECTED.union(read_macs)
    score_connected = len(mac_totals)
    with open(FILE_NAME, 'w') as f:
        content = '{}'.format(score_connected)
        for mac in mac_totals:
            content += '\n{}'.format(mac)
        f.write(content)

    return score_connected


def main():
    try:
        while True:
            wifi_score = get_wifi_score()
            msg = '[{}]: '.format(datetime.datetime.now().strftime('%H:%M:%S'))
            msg += 'Wifi = {}.'.format(wifi_score)

            color = Colors.GREEN
            colorful_print(msg, color)
            sleep(30)

    except KeyboardInterrupt:
        sys.exit()


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


if __name__ == '__main__':
    main()
