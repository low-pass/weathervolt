from pygame import mixer
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.weatherapi25.weather import Weather
from datetime import datetime, timedelta
from dateutil import tz
import numpy as np
import scipy.io.wavfile
import math
import yaml
import os 

def wav_output(highest,lowest,id_char):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../wavecfg.yaml", 'r') as stream:
        wavecfg = yaml.safe_load(stream)
    fsamp = wavecfg['fsamp']
    fsine = wavecfg['fsine']
    fmod = wavecfg['fmod']
    fullscale = wavecfg['fullsc']
    t_sec = wavecfg['t_sec']
    filename = wavecfg['filename']
    t = np.linspace(0.,t_sec,fsamp*t_sec)
    vol = (highest-lowest)/2+lowest
    mod_ampl = (highest-lowest)/vol/2
    amp = np.iinfo(np.int16).max
    carrier = vol*np.sin(2.*np.pi*fsine*t)/fullscale
    mod = mod_ampl*np.sin(2.*np.pi*fmod*t)+1
    data = np.clip(np.multiply(carrier,mod),a_min=-1,a_max=1)
    data = np.floor(data*amp)
    data = np.asarray(data, dtype=np.int16)
    scipy.io.wavfile.write('/tmp/' + filename + id_char + '.wav',fsamp,data)
    mixer.music.stop()
    mixer.music.load('/tmp/' + filename + id_char + '.wav')
    mixer.music.play(-1)
    return

def get_forecast():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + '/../owm.key', 'r') as file:
        owm_key = file.read().replace('\n','')
    owm = OWM(owm_key)
    mgr = owm.weather_manager()
    my_city_id = 660129 # Espoo, Finland
    fc = mgr.forecast_at_id(my_city_id,'3h')
    min10 = timedelta(minutes=10)
    temp_vec_max = []
    temp_vec_min = []
    for i in range(len(fc.forecast.weathers)):
        ep = fc.forecast.get(i).to_dict()['reference_time']
        stamp = datetime.fromtimestamp(ep)-min10
        if stamp.date() <= datetime.now().date() and stamp.hour >= 8:
            temp_vec_max.append(fc.forecast.get(i).temperature('celsius')['temp_max'])
            temp_vec_min.append(fc.forecast.get(i).temperature('celsius')['temp_min'])
    highest = np.amax(np.array(temp_vec_max))
    lowest = np.amin(np.array(temp_vec_min))
    return highest, lowest

