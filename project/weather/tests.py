from django.test import TestCase
from .models import Weather, DataPoint, Temperature, Humidity, Pressure
from .open_weather_map_client import OpenWeatherMapClient, InvalidDateException
from datetime import datetime

# Create your tests here.
class TestDataPoint(TestCase):

    def test_creation(self):
        unit = 'a ton'
        value = '500'
        dp = DataPoint(unit, value)
        assert dp.unit == unit
        assert dp.value == value

    def test_to_dict(self):
        unit = 'kg'
        value = '100'
        dp = DataPoint(unit, value)
        dp_dict = dp.to_dict()
        assert dp_dict['unit'] == unit
        assert dp_dict['value'] == value


class TestWeatherObject(TestCase):

    def test_creation(self):
        description = 'new weather object'
        humidity = 'super wet lol'
        pressure = 'my ears are popping'
        temperature = 'like, a bajillion'

        weather = Weather(description, humidity, pressure, temperature)
        assert weather.description == description
        assert weather.humidity == humidity
        assert weather.pressure == pressure
        assert weather.temperature == temperature


    def test_to_dict(self):
        description = 'new weather object'
        humidity = 'super wet lol'
        pressure = 'my ears are popping'
        temperature = 'like, a bajillion'

        weather = Weather(description,
                          Humidity(humidity),
                          Pressure(pressure),
                          Temperature(temperature))

        weather_dict = weather.to_dict()
        assert {'description', 'humidity', 'pressure', 'temperature'} == \
               set(weather_dict.keys())

    def test_creation_from_open_weather(self):
        sample_weather_response = {
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}], "base": "stations",
            "main": {"temp": 290.43, "pressure": 1003, "humidity": 45, "temp_min": 289.82, "temp_max": 292.04}}
        weather = Weather._from_open_weather(sample_weather_response)
        weather_dict = weather.to_dict()
        self.assertDictEqual(weather_dict, {"description": "clear sky", "pressure": {"unit": "hPa", "value": 1003},
                                            "humidity": {"unit": "%", "value": 45}, "temperature": {"unit": "C", "value": "18"}})


class TestWeatherClient(TestCase):
    def test_weather_client_time_window_parsing(self):
        weather_possibility_one = {'dt_txt': "1990-01-01 12:05:05", 'weather': 'hot af'}
        weather_possibility_two = {'dt_txt': "2005-05-07 18:05:05", 'weather': 'cold af'}
        weather_possibilities = [weather_possibility_one, weather_possibility_two]
        datetimeone = datetime(1990, 1, 1, 13)
        datetimetwo = datetime(2005, 5, 7, 19)

        weather_info_one = OpenWeatherMapClient.get_weather_for_time(weather_possibilities, datetimeone)
        assert weather_info_one['weather'] == 'hot af'

        weather_info_two = OpenWeatherMapClient.get_weather_for_time(weather_possibilities, datetimetwo)
        assert weather_info_two['weather'] == 'cold af'

    def test_invalid_times(self):
        weather_possibility_one = {'dt_txt': "1990-01-01 12:05:05", 'weather': 'hot af'}
        weather_possibilities = [weather_possibility_one]
        datetime_too_late = datetime(3000, 1, 1, 1)
        datetime_too_early = datetime(1900, 1, 1, 1)

        with self.assertRaises(InvalidDateException):
            OpenWeatherMapClient.get_weather_for_time(weather_possibilities, datetime_too_late)

        with self.assertRaises(InvalidDateException):
            OpenWeatherMapClient.get_weather_for_time(weather_possibilities, datetime_too_early)