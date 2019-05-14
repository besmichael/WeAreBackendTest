from django.urls import path

from . import views

urlpatterns = [
    path('<str:type>/<str:city>/<str:date>/<str:time>/', views.weather_response, name='weather'),
]