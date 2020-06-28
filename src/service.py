from util import *
from pygame import mixer
from datetime import datetime
import time
import math
import ntplib

mixer.init()

id_char = 'a'
inet_fail = False

while True:
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../wavecfg.yaml", 'r') as stream:
        wavecfg = yaml.safe_load(stream)
    fullscale = wavecfg['fullsc']

    if not internet_on():
        if not inet_fail:
            print('Internet is gone!')
            inet_fail = True
            wav_output(fullscale/10,fullscale/10,1,0,id_char)
            id_char = flip_id(id_char)
        time.sleep(5)
    else:
        inet_fail = False
        c = ntplib.NTPClient()
        try:
            req = c.request('europe.pool.ntp.org', version=3)
        except:
            print('NTP service unresponsive!')
            wav_output(fullscale/5,fullscale/5,1,0,id_char)
            id_char = flip_id(id_char)
            time.sleep(60)
            continue
        timenow = datetime.fromtimestamp(req.tx_time)
        highest, lowest, status = get_forecast(timenow)
        print('Time: ' + str(timenow) + ' OWM status: ' + status)
        if status == 'owmfail':
            wav_output(fullscale/2,fullscale/2,1,0,id_char)
            time.sleep(60)
        else:
            if status == 'rain':
                boost = 10
                offset = 0.75
            elif status == 'clouds':
                boost = 10
                offset = 0
            else:           # this is supposed to be status == 'clear'
                boost = 1
                offset = 0
            print('Highest temp: ' + str(highest) + ' Lowest temp: ' + str(lowest))
            wav_output(highest,lowest,boost,offset,id_char)
            time.sleep(600)
        id_char = flip_id(id_char)

