from django.http import JsonResponse


def weather_response(request):
    response_data = {}
    response_data['weather'] = 'It be hot lol'
    return JsonResponse(response_data)