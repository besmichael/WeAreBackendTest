from django.test import TestCase
from .models import Weather, DataPoint, Temperature, Humidity, Pressure
from .open_weather_map_client import OpenWeatherMapClient
from datetime import datetime, timedelta

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
        status = 'all good'

        weather = Weather(description, humidity, pressure, temperature, status)
        assert weather.description == description
        assert weather.humidity == humidity
        assert weather.pressure == pressure
        assert weather.temperature == temperature
        assert weather.status == status
        assert weather.timestamp

    def test_to_dict(self):
        description = 'new weather object'
        humidity = 'super wet lol'
        pressure = 'my ears are popping'
        temperature = 'like, a bajillion'
        status = 'all good'

        weather = Weather(description,
                          Humidity(humidity),
                          Pressure(pressure),
                          Temperature(temperature),
                          status)

        weather_dict = weather.to_dict()
        assert {'description', 'humidity', 'pressure', 'temperature', 'status', 'timestamp'} == \
               set(weather_dict.keys())

    def test_creation_from_open_weather(self):
        sample_weather_response = {
            "coord": {"lon": 13.39, "lat": 52.52},
            "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}], "base": "stations",
            "main": {"temp": 290.43, "pressure": 1003, "humidity": 45, "temp_min": 289.82, "temp_max": 292.04},
            "visibility": 10000, "wind": {"speed": 6.7, "deg": 150}, "clouds": {"all": 0}, "dt": 1557332035,
            "sys": {"type": 1, "id": 1275, "message": 0.008, "country": "DE", "sunrise": 1557285761, "sunset": 1557340993},
            "id": 2950159, "name": "Berlin", "cod": 200}
        weather = Weather._from_open_weather(sample_weather_response)
        weather_dict = weather.to_dict()
        assert 'timestamp' in weather_dict
        weather_dict['timestamp'] = '2019-05-14 18:10:26'
        self.assertDictEqual(weather_dict, {"description": "clear sky", "pressure": {"unit": "hPa", "value": 1003},
                                            "humidity": {"unit": "%", "value": 45}, "temperature": {"unit": "C", "value": "18"},
                                            "status": "success", "timestamp": "2019-05-14 18:10:26"})


class TestWeatherClient():
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