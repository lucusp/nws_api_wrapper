import requests
import json
from datetime import datetime, timedelta, timezone
import pytz

class Weather:
    def __init__(self):
        self.base_url = 'https://api.weather.gov/'
        self.headers = {'User-Agent':'Your Name email@email.com'}

        # URLs
        self.glossary_terms = 'glossary'
        self.icons = 'icons'
        self.stations = 'stations?state={state_abbr}&limit={num_stations}'.format(state_abbr="{state_abbr}", num_stations="{num_stations}")
        self.observations_all = 'stations/{station}/observations'.format(station="{station}")
        self.observations_latest = 'stations/{station}/observations/latest'.format(station="{station}")
        self.geopoints = 'points/{point1},{point2}'.format(point1="{point1}",point2="{point2}")

    def __get_data(self, url, verify=True):
        """
            private function to get whatever data we want to manipulate for end use
        """
        req = requests.get(self.base_url + url, verify=verify, headers=self.headers)
        json_data = json.loads(req.text)
        return json_data

    # /////////////////////////////////////
    # set of general api calls from nws api
    # /////////////////////////////////////
    def getGlossaryTerms(self):
        return self.__get_data(self.glossary_terms)['glossary']

    def getIcons(self):
        return self.__get_data(self.icons)['icons']

    def getStations(self, state_abbr, num_stations):
        return self.__get_data(self.stations.format(state_abbr=state_abbr, num_stations=num_stations))

    def getStationAllObservations(self, station):
        return self.__get_data(self.observations_all.format(station=str(station)))['features']

    def getStationLatestObservation(self, station):
        return self.__get_data(self.observations_latest.format(station=str(station)))
    
    # ////////////////////////////////////
    # set of custom/specific data requests
    # ////////////////////////////////////      
    def getStationCoordinates(self, station):
        data = self.__get_data(self.observations_all.format(station=str(station)))
        return data['features'][0]['geometry']['coordinates']

    def getStationHourlyForecast(self, station):
        point1, point2 = self.getStationCoordinates(station=station)
        return self.__get_data(self.__get_data(
            self.geopoints.format(point1=str(point2),point2=str(point1))
            )['properties']['forecastHourly'].replace(self.base_url, ''))

    def getStationHourlyTemps(self, station, time_zone='US/Central', temp_type='F', strip_timezone=True):
        """
            use the private __get_data to get our observations url
            create a dictionary for end use giving metadata stationid and timezone
            convert to Fahrenheit, return the data by hourly observation
        """
        data = self.__get_data(self.observations_all.format(station=str(station)))
        
        data_dict = {'station':f'{station}', 'local_timezone':f'{time_zone}', 'temps':[]}

        # to convert to F multiply C * 1.8 and + 32 to the result
        if temp_type == 'F':
            mult = 1.8
            add = 32
        else:
            mult = 1
            add = 0

        for items in data['features']:
            obv_time = items['properties']['timestamp']

            # convert to desired timezone (intial times are in GMT/UTC)
            _obv_time = datetime.strptime(obv_time, '%Y-%m-%dT%H:%M:%S+00:00')
            _obv_time = _obv_time.replace(tzinfo=timezone.utc)
            local_timezone = pytz.timezone(time_zone)
            _obv_time = _obv_time.astimezone(local_timezone)

            # strip timezone info from final date/time for end use by pandas, etc.
            _obv_time = _obv_time.replace(tzinfo=None)
            date, time = str(_obv_time).split(' ')
            time = time.split('-')[0]
            try:
                data_dict['temps'].append({'date': date, 'time': _obv_time, 'temp': round((items['properties']['temperature']['value']*mult)+add,0)})
            except:
                pass
        return data_dict