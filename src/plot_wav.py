from scipy.io import wavfile
import matplotlib.pyplot as plt
import numpy as np
import yaml
import os 

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(dir_path + "/../wavecfg.yaml", 'r') as stream:
    wavecfg = yaml.safe_load(stream)
filename = wavecfg['filename']
fullscale = wavecfg['fullsc']

samplerate, dataa = wavfile.read('/tmp/' + filename + 'a.wav')
samplerate, datab = wavfile.read('/tmp/' + filename + 'b.wav')

length = dataa.shape[0] / samplerate
time = np.linspace(0., length, dataa.shape[0])
dataa=dataa/2**16
datab=datab/2**16

figure,axes = plt.subplots(2,1,sharex=True)
axes[0].plot(time,dataa*fullscale*2,label='Sequence A')
axes[1].plot(time,datab*fullscale*2,label='Sequence B')
axes[0].set_ylabel('Sequence A')
axes[1].set_ylabel('Sequence B')
axes[1].set_xlabel('Time (s)')
axes[0].set_ylim(-fullscale,fullscale)
axes[1].set_ylim(-fullscale,fullscale)
axes[0].grid(True)
axes[1].grid(True)
titlestr = "AC signal sequences" 
plt.suptitle(titlestr,fontsize=20);
plt.show(block=False);

input()
