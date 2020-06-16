from pygame import mixer
import time
import numpy as np
import scipy.io.wavfile
import math

fsamp = 44100
fsine = 100
length = 5
t = np.linspace(0.,length,fsamp*length)
amp = np.iinfo(np.int16).max
vol = 0.5
data = np.floor(vol*amp*np.sin(2.*np.pi*fsine*t))
data = np.asarray(data, dtype=np.int16)
scipy.io.wavfile.write('/tmp/test.wav',fsamp,data)

vol = 0.9
data = np.floor(vol*amp*np.sin(2.*np.pi*fsine*t))
data = np.asarray(data, dtype=np.int16)
scipy.io.wavfile.write('/tmp/test2.wav',fsamp,data)

vol = 0.2
data = np.floor(vol*amp*np.sin(2.*np.pi*fsine*t))
data = np.asarray(data, dtype=np.int16)
scipy.io.wavfile.write('/tmp/test3.wav',fsamp,data)

mixer.init()
mixer.music.load('/tmp/test.wav')
mixer.music.play(-1)

time.sleep(1)
print('foo')
time.sleep(1)
mixer.music.stop()
mixer.music.load('/tmp/test2.wav')
mixer.music.play(-1)
time.sleep(1)
print('bar')
time.sleep(3)
mixer.music.stop()
mixer.music.load('/tmp/test3.wav')
mixer.music.play(-1)
time.sleep(4)

