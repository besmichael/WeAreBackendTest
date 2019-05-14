from django.urls import path

from . import views

urlpatterns = [
    path('summary/berlin/<str:date>/<str:time>/', views.weather_response, name='weather'),
]