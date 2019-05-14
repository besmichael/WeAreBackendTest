import requests
from .models import Weather
from datetime import datetime, timedelta


WEATHERMAP_DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


class OpenWeatherMapClient():
    def __init__(self):
        self.api_url = 'http://api.openweathermap.org'
        self.api_key = '8db9f4f1eeca445db409bb4ef36cb811'  # Would never do this in a real system...
        self.city = 'Berlin,DE'

    def get_weather(self, requested_time):
        """requested_time is datetime object"""
        #Validate date and time is proper
        url = self.api_url + '/data/2.5/forecast?q={city_name}&APPID={app_id}&mode=JSON'
        full_url = url.format(url, city_name=self.city, app_id=self.api_key)
        response_json = requests.get(full_url).json()
        weather_info = self.get_weather_for_time(response_json['list'], requested_time)
        return Weather._from_open_weather(weather_info)

    @classmethod
    def get_weather_for_time(cls, weather_info_list, requested_time):
        for weather_possibility in weather_info_list:
            time_of_weather = datetime.strptime(weather_possibility['dt_txt'], WEATHERMAP_DATETIME_FORMAT)
            time_difference = requested_time - time_of_weather
            if ((time_difference < timedelta(hours=3)) and (time_difference > timedelta(hours=0))):
                return weather_possibility
        raise Exception("Invalid requested time")