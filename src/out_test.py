from util import *
from pygame import mixer
from datetime import datetime
import time
import math
import ntplib

mixer.init()

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
    wav_output(fullscale/2,fullscale/2,1,0,'a')
else:
    print('Highest temp: ' + str(highest) + ' Lowest temp: ' + str(lowest))
    wav_output(highest,lowest,1,0,'a')
    time.sleep(10)
    print('Test done. Did it work?')
