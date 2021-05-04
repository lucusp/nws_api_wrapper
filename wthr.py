import requests
import json
from datetime import datetime, timedelta, timezone
import pytz

class weather:
    def __init__(self):
        self.base_url = 'https://api.weather.gov/'
        self.headers = {'User-Agent':'Your Name email@email.com'}

        #observations
        self.observations_all = 'stations/{station}/observations'.format(station="{station}")

    def __get_data(self, url, verify=True):
        print(self.observations_all)
        req = requests.get(self.base_url + url, verify=verify, headers=self.headers)
        json_data = json.loads(req.text)
        return json_data

    def getHourlyTemps(self, station, time_zone='US/Central'):
        data = self.__get_data(self.observations_all.format(station=str(station)))
        
        data_dict = {'station':f'{station}', 'local_timezone':f'{time_zone}', 'temps':[]}

        for items in data['features']:
            obv_time = items['properties']['timestamp']
            _obv_time = datetime.strptime(obv_time, '%Y-%m-%dT%H:%M:%S+00:00')
            _obv_time = _obv_time.replace(tzinfo=timezone.utc)
            local_timezone = pytz.timezone(time_zone)
            _obv_time = _obv_time.astimezone(local_timezone)
            date, time = str(_obv_time).split(' ')
            data_dict['temps'].append({'date': date, 'time': time, 'temp': (items['properties']['temperature']['value']*1.8)+32})

        return data_dict