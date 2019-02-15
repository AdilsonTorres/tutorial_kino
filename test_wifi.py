import json
from subprocess import Popen, PIPE

wifi_score_command = ['sudo', '/usr/bin/ndsctl', 'json']
score_process = Popen(wifi_score_command, stdout=PIPE)
stdout = score_process.communicate(timeout=30)
response = json.loads(stdout[0].decode('utf-8'))
score_connected = response['client_length']
print(score_connected)
score_process.kill()

