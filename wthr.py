import requests
import json
import pandas as pd
from datetime import datetime, timedelta, timezone
import pytz

class weather:
    def __init__(self):
        self.base_url = 'https://api.weather.gov'
        self.headers = {'User-Agent':'Your Name email@email.com'}

    def getHourlyTemps(self, station):
        req = requests.get(f'{self.base_url}/stations/{station}/observations', verify=True, headers=self.headers)
        json_data = json.loads(req.text)

        arr = []

        for key in json_data:
            for items in json_data['features']:
                obv_time = items['properties']['timestamp']
                _obv_time = datetime.strptime(obv_time, '%Y-%m-%dT%H:%M:%S+00:00')
                _obv_time = _obv_time.replace(tzinfo=timezone.utc)
                local_timezone = pytz.timezone('US/Central')
                _obv_time = _obv_time.astimezone(local_timezone)
                date, time = str(_obv_time).split(' ')
                arr.append({'date': date, 'time': time, 'temp': (items['properties']['temperature']['value']*1.8)+32})

        return arr

