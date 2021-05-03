import requests
import json
from datetime import datetime, timedelta, timezone
import pytz

class weather:
    def __init__(self):
        self.base_url = 'https://api.weather.gov'
        self.headers = {'User-Agent':'Your Name email@email.com'}

    def getHourlyTemps(self, station, time_zone='US/Central',verify=True):
        req = requests.get(f'{self.base_url}/stations/{station}/observations', verify=verify, headers=self.headers)
        json_data = json.loads(req.text)

        arr = [{'station':f'{station}','local_timezone':f'{time_zone}'}]

        for items in json_data['features']:
            obv_time = items['properties']['timestamp']
            _obv_time = datetime.strptime(obv_time, '%Y-%m-%dT%H:%M:%S+00:00')
            _obv_time = _obv_time.replace(tzinfo=timezone.utc)
            local_timezone = pytz.timezone(time_zone)
            _obv_time = _obv_time.astimezone(local_timezone)
            date, time = str(_obv_time).split(' ')
            arr.append({'date': date, 'time': time, 'temp': (items['properties']['temperature']['value']*1.8)+32})

        return arr

