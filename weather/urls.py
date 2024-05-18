from django.urls import path
from .views import CurrentWeatherView, WeatherListView, MetarListView

urlpatterns = [
    path('current/', CurrentWeatherView.as_view(), name='current_weather'),
    path('forecast/', WeatherListView.as_view(), name='weather_forecast'),
    path('metar/', MetarListView.as_view(), name='metar_info'),
]