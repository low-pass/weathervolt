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

seq = []
part = False

try:
    samplerate, dataa = wavfile.read('/tmp/' + filename + 'a.wav')
    seq.append('A')
    part = True
    data = dataa
except FileNotFoundError:
    print('Sequence A not found')
try:    
    samplerate, datab = wavfile.read('/tmp/' + filename + 'b.wav')
    seq.append('B')
    part = True
    data = datab
except FileNotFoundError:
    print('Sequence B not found')

if part:
    length = data.shape[0] / samplerate
    time = np.linspace(0., length, data.shape[0])
    data=data/2**16
    figure = plt.figure()
    plt.plot(time,data*fullscale*2,label='Sequence ' + seq[0])
    plt.ylabel('Sequence' + seq[0])
    plt.xlabel('Time (s)')
    plt.ylim(-fullscale,fullscale)
    plt.grid(True)
    titlestr = "AC signal sequence" 
    plt.suptitle(titlestr,fontsize=17)
    plt.show(block=False)
else:
    if not seq:
        print('Nothing to plot, aborting..')
        exit()
    else:
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
        plt.suptitle(titlestr,fontsize=20)
        plt.show(block=False)

print('press any key')
input()
