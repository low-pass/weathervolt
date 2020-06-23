from util import *
from pygame import mixer
from datetime import datetime
import time
import math
import ntplib

mixer.init()

id_char = 'a'

while True:
    c = ntplib.NTPClient()
    req = c.request('europe.pool.ntp.org', version=3)
    timenow = datetime.fromtimestamp(req.tx_time)
    highest, lowest, status = get_forecast(timenow)
    print('Time: ' + str(timenow) + ' OWM status: ' + status)

    if status == 'owmfail':
        dir_path = os.path.dirname(os.path.realpath(__file__))
        with open(dir_path + "/../wavecfg.yaml", 'r') as stream:
            wavecfg = yaml.safe_load(stream)
        fullscale = wavecfg['fullsc']
        wav_output(fullscale/2,fullscale/2,id_char)
    else:
        print('Highest temp: ' + str(highest) + ' Lowest temp: ' + str(lowest))
        wav_output(highest,lowest,id_char)

    if id_char == 'a':
        id_char = 'b'
    else:
        id_char = 'a'

    time.sleep(600)

