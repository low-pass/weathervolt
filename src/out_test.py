from util import *
from pygame import mixer
import time

mixer.init()

highest, lowest = get_forecast()
print(highest)
print(lowest)
wav_output(highest,lowest,'a')
time.sleep(6)

wav_output(highest-2,lowest+1,'b')
time.sleep(6)
