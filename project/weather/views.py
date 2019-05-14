from django.http import JsonResponse
from .open_weather_map_client import OpenWeatherMapClient
from datetime import datetime

def weather_response(request, date, time):
    weather_time = datetime.strptime(date+time, '%Y%m%d%H%M')
    weather_client = OpenWeatherMapClient()  # Better have long-lived client for app
    weather = weather_client.get_weather(weather_time)
    return JsonResponse(weather.to_dict())