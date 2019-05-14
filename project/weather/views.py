from django.http import JsonResponse
from .open_weather_map_client import OpenWeatherMapClient, InvalidDateException


def weather_response(request, date, time):
    weather_client = OpenWeatherMapClient()  # Better have long-lived client for app
    try:
        weather = weather_client.get_weather(date+time)
    except InvalidDateException as e:
        return e.to_json_response()

    return JsonResponse(weather.to_dict())