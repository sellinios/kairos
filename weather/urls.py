from django.urls import path
from . import views

urlpatterns = [
    path('', views.WeatherListView.as_view(), name='weather-list'),
    path('current/', views.CurrentWeatherView.as_view(), name='current-weather'),
    path('metar/', views.MetarListView.as_view(), name='metar-list'),
]
