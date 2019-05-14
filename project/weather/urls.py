from django.urls import path

from . import views

urlpatterns = [
    path('summary/berlin/', views.weather_response, name='weather'),
]