from pygame import mixer
from pyowm import OWM
from pyowm.utils import timestamps
from pyowm.weatherapi25.weather import Weather
from datetime import datetime, timedelta
import numpy as np
import scipy.io.wavfile
import math
import yaml
import ntplib
import os 
import urllib.request

def internet_on():
    try:
        urllib.request.urlopen('http://216.58.192.142',timeout=5)
        return True
    except urllib.error.URLError:
        return False

def flip_id(id_char):
    if id_char == 'a':
        return 'b'
    else:
        return 'a'

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

def get_forecast(timenow):
    highest = 0
    lowest = 0
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/../wavecfg.yaml", 'r') as stream:
        wavecfg = yaml.safe_load(stream)
    cloud_min = wavecfg['cloud_min']
    rain_min = wavecfg['rain_min']
    with open(dir_path + '/../owm.key', 'r') as file:
        owm_key = file.read().replace('\n','')
    owm = OWM(owm_key)
    mgr = owm.weather_manager()
    my_city_id = 660129 # Espoo, Finland
    try:
        fc = mgr.forecast_at_id(my_city_id,'3h')
    except pyowm.exceptions.OWMError:
        print('OWM service unresponsive!')
        status = 'owmfail'
        return highest, lowest, status
    min10 = timedelta(minutes=10)
    temp_vec_max = []
    temp_vec_min = []
    cloud_vec = []
    rain_vec = []
    for i in range(len(fc.forecast.weathers)):
        ep = fc.forecast.get(i).to_dict()['reference_time']
        stamp = datetime.fromtimestamp(ep)-min10
        if stamp.date() <= timenow.date() and stamp.hour >= 8:
            temp_vec_max.append(fc.forecast.get(i).temperature('celsius')['temp_max'])
            temp_vec_min.append(fc.forecast.get(i).temperature('celsius')['temp_min'])
            cloud_vec.append(fc.forecast.get(i).to_dict()['clouds'])
            if fc.forecast.get(i).to_dict()['rain']:
                rain_vec.append(fc.forecast.get(i).to_dict()['rain']['3h'])
    if not temp_vec_max:
        print('Out of compatible forecasts!')
        status = 'owmfail'
    else:
        status = 'clear' # default
        highest = np.amax(np.array(temp_vec_max))
        lowest = np.amin(np.array(temp_vec_min))
        clouds_over = np.greater_equal(np.array(cloud_vec),cloud_min)
        clears_count = np.size(clouds_over) - np.count_nonzero(clouds_over)
        rain_over = np.greater_equal(np.array(rain_vec),rain_min)
        rain_count = np.count_nonzero(rain_over)
        if clears_count == 0:
            status = 'clouds'
        if rain_count >= 1: 
            status = 'rain'
    return highest, lowest, status

