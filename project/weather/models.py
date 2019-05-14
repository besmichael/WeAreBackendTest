from django.db import models
import math
import datetime

def convert_kelvin_to_celsius(kelvin_string):
    celsius = float(kelvin_string) - 273.15
    return str(math.ceil(celsius))

class Weather():
    def __init__(self, description, humidity, pressure, temperature, status):
        self.description = description
        self.humidity = humidity
        self.pressure = pressure
        self.temperature = temperature
        self.status = status
        self.timestamp = str(datetime.datetime.now()).split('.')[0]  # UTC timestamp e.g. '2019-05-14 19:37:18'

    @classmethod
    def _from_open_weather(cls, json_response):
        description = json_response['weather'][0]['description']
        weather_info = json_response['main']
        humidity = Humidity(weather_info['humidity'])
        pressure = Pressure(weather_info['pressure'])
        temperature = Temperature(convert_kelvin_to_celsius(weather_info['temp']))
        return cls(description,
                   humidity,
                   pressure,
                   temperature,
                   'success')

    def to_dict(self):
        return {
            'description': self.description,
            'pressure': self.pressure.to_dict(),
            'humidity': self.humidity.to_dict(),
            'temperature': self.temperature.to_dict(),
            'status': self.status,
            'timestamp': self.timestamp
        }

class DataPoint():
    def __init__(self, unit, value):
        self.unit = unit
        self.value = value

    def to_dict(self):
        return {'unit': self.unit,
                'value': self.value}


class Humidity(DataPoint):
    def __init__(self, percent_value):
        super(Humidity, self).__init__('%', percent_value)


class Pressure(DataPoint):
    def __init__(self, hpa_value):
        super(Pressure, self).__init__('hPa', hpa_value)


class Temperature(DataPoint):
    def __init__(self, celsius_value):
        super(Temperature, self).__init__('C', celsius_value)

