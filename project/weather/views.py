from django.http import JsonResponse
from .open_weather_map_client import OpenWeatherMapClient, InvalidDateException
from datetime import datetime


class InvalidWeatherRequestType(Exception):
    def __init__(self, message):
        self.message = message
        super(InvalidWeatherRequestType, self).__init__(message)

    def to_json_response(self):
        return JsonResponse({'status': 'error', 'message': self.message}, status=400)


def weather_response(request, type, city, date, time):
    weather_client = OpenWeatherMapClient(city)  # It would be better have long-lived client for app
    try:
        weather = weather_client.get_weather(date+time)
        return build_json_weather_response(weather, type)
    except (InvalidDateException, InvalidDateException) as e:
        return e.to_json_response()


def build_json_weather_response(weather, type):
    if type == 'summary':
        data = weather.to_dict()
    elif type == 'temperature':
        data = weather.temperature.to_dict()
    elif type == 'pressure':
        data = weather.pressure.to_dict()
    elif type == 'humidity':
        data = weather.humidity.to_dict()
    else:
        raise InvalidWeatherRequestType('Type %s is not valid' % type)

    data['timestamp'] = str(datetime.now()).split('.')[0]  # UTC timestamp e.g. '2019-05-14 19:37:18'
    data['status'] = 'success'
    return JsonResponse(data)