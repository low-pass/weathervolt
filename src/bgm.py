from pygame import mixer
import time
import numpy as np
import scipy.io.wavfile
import math
import yaml
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/../wavecfg.yaml", 'r') as stream:
    wavecfg = yaml.safe_load(stream)
fsamp = wavecfg['fsamp']
fsine = wavecfg['fsine']
t_sec = wavecfg['t_sec']
filename = wavecfg['filename']

t = np.linspace(0.,t_sec,fsamp*t_sec)
amp = np.iinfo(np.int16).max
vol = 0.5
data = np.floor(vol*amp*np.sin(2.*np.pi*fsine*t))
data = np.asarray(data, dtype=np.int16)
scipy.io.wavfile.write('/tmp/' + filename + 'a.wav',fsamp,data)

vol = 1.0
data = np.floor(vol*amp*np.sin(2.*np.pi*fsine*t))
data = np.asarray(data, dtype=np.int16)
scipy.io.wavfile.write('/tmp/' + filename + 'b.wav',fsamp,data)

mixer.init()
mixer.music.load('/tmp/' + filename + 'a.wav')
mixer.music.play(-1)

time.sleep(2)
print('foo')
time.sleep(1)
mixer.music.stop()
mixer.music.load('/tmp/' + filename + 'b.wav')
mixer.music.play(-1)
time.sleep(4)
