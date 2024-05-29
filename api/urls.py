# api/urls.py

from django.urls import path, re_path
from api.views.view_weather_places import WeatherDetailAPIView

urlpatterns = [
    re_path(r'^weather/(?P<continent>[\w-]+)/(?P<country>[\w-]+)/(?P<levels_and_place>.+)/$', WeatherDetailAPIView.as_view(), name='weather_detail_api'),
]
