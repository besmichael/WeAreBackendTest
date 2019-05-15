import requests
from django.http import JsonResponse
from .models import Weather
from datetime import datetime, timedelta


WEATHERMAP_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class InvalidDateException(Exception):
    def __init__(self, message):
        self.message = message
        super(InvalidDateException, self).__init__(message)

    def to_json_response(self):
        return JsonResponse({'status': 'error', 'message': self.message}, status=400)


class OpenWeatherMapClient():
    def __init__(self, city):
        self.api_url = 'http://api.openweathermap.org'
        self.api_key = '8db9f4f1eeca445db409bb4ef36cb811'  # Would never do this in a real system...
        self.city = '%s,DE' % city

    def get_weather(self, requested_time_string):
        """Gets the weather for a given period in time, throws an InvalidDateException if the time is not within
        the next 5 days"""
        try:
            requested_time = datetime.strptime(requested_time_string, '%Y%m%d%H%M')
        except:
            raise InvalidDateException('the provided date and time %s is not valid' % requested_time_string)
        url = self.api_url + '/data/2.5/forecast?q={city_name}&APPID={app_id}&mode=JSON'
        full_url = url.format(url, city_name=self.city, app_id=self.api_key)
        response_json = requests.get(full_url).json()
        weather_info = self.get_weather_for_time(response_json['list'], requested_time)
        return Weather._from_open_weather(weather_info)

    @classmethod
    def get_weather_for_time(cls, weather_info_list, requested_time):
        """From a list of weather states from the api, it extracts the one that corresponds to the time given,
        throws InvalidDateException if no weather information for the requested time is given."""
        for weather_possibility in weather_info_list:
            time_of_weather = datetime.strptime(weather_possibility['dt_txt'], WEATHERMAP_DATETIME_FORMAT)
            time_difference = requested_time - time_of_weather
            if ((time_difference < timedelta(hours=3)) and (time_difference > timedelta(hours=0))):
                return weather_possibility
        raise InvalidDateException('Date must be within 5 days from now')
