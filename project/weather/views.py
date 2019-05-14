from django.http import JsonResponse
from .models import Weather


def weather_response(request):
    fake_weather_response = {"coord": {"lon": 13.39, "lat": 52.52},
     "weather": [{"id": 800, "main": "Clear", "description": "clear sky", "icon": "01d"}], "base": "stations",
     "main": {"temp": 290.43, "pressure": 1003, "humidity": 45, "temp_min": 289.82, "temp_max": 292.04},
     "visibility": 10000, "wind": {"speed": 6.7, "deg": 150}, "clouds": {"all": 0}, "dt": 1557332035,
     "sys": {"type": 1, "id": 1275, "message": 0.008, "country": "DE", "sunrise": 1557285761, "sunset": 1557340993},
     "id": 2950159, "name": "Berlin", "cod": 200}
    weather = Weather._from_open_weather(fake_weather_response)
    return JsonResponse(weather.to_dict())