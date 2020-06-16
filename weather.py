from pyowm import OWM
from pyowm.utils import timestamps

with open('owm.key', 'r') as file:
    owm_key = file.read().replace('\n','')

owm = OWM(owm_key)
mgr = owm.weather_manager()
my_city_id = 660129 # Espoo, Finland
fc = mgr.forecast_at_id(my_city_id,'3h')
print(fc.forecast.to_dict())
