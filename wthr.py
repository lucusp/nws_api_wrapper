import requests
import json
from datetime import datetime, timedelta, timezone
import pytz

class weather:
    def __init__(self):
        self.base_url = 'https://api.weather.gov/'
        self.headers = {'User-Agent':'Your Name email@email.com'}

        # URLs
        self.observations_all = 'stations/{station}/observations'.format(station="{station}")
        self.geopoints = 'points/{point1},{point2}'.format(point1="{point1}",point2="{point2}")

    def __get_data(self, url, verify=True):
        """
            private function to get whatever data we want to manipulate for end use
        """
        req = requests.get(self.base_url + url, verify=verify, headers=self.headers)
        json_data = json.loads(req.text)
        return json_data

    def getStationAllObservations(self, station):
        return self.__get_data(self.observations_all.format(station=str(station)))
        
    def getStationCoordinates(self, station):
        data = self.__get_data(self.observations_all.format(station=str(station)))
        return data['features'][0]['geometry']['coordinates']

    def getStationHourlyForecast(self, station):
        point1, point2 = self.getStationCoordinates(station=station)
        return self.__get_data(self.__get_data(
            self.geopoints.format(point1=str(point2),point2=str(point1))
            )['properties']['forecastHourly'].replace(self.base_url, ''))

    def getStationHourlyTemps(self, station, time_zone='US/Central', type='F'):
        """
            use the private __get_data to get our observations url
            create a useful dictionary for end use giving metadata stationid and timezone
            convert to Fahrenheit, return the data by hourly observation
        """
        data = self.__get_data(self.observations_all.format(station=str(station)))
        
        data_dict = {'station':f'{station}', 'local_timezone':f'{time_zone}', 'temps':[]}

        # to convert to F we multiply C * 1.8 and + 32 to the result
        if type == 'F':
            mult = 1.8
            add = 32
        else:
            mult = 1
            add = 0

        for items in data['features']:
            obv_time = items['properties']['timestamp']
            _obv_time = datetime.strptime(obv_time, '%Y-%m-%dT%H:%M:%S+00:00')
            _obv_time = _obv_time.replace(tzinfo=timezone.utc)
            local_timezone = pytz.timezone(time_zone)
            _obv_time = _obv_time.astimezone(local_timezone)
            date, time = str(_obv_time).split(' ')
            data_dict['temps'].append({'date': date, 'time': time, 'temp': (int(items['properties']['temperature']['value'])*mult)+add})

        return data_dict