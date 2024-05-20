from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views.views_geografic_country import CountryViewSet
from .views.views_geografic_administrative_division import AdministrativeDivisionViewSet
from .views.views_geografic_places import PlaceViewSet
from .views.views_geographic_entity import GeographicEntityViewSet
from .views.views_weather_metar_data import MetarDataViewSet
from .views.views_geographic_system_stats import get_system_stats
from .views.views_weather_list import WeatherListView
from .views.views_weather_current_weather import CurrentWeatherView
from .views.views_weather_metar_list import MetarListView

# Create a router and register the viewsets with it
router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'administrative-divisions', AdministrativeDivisionViewSet)
router.register(r'geographic-entities', GeographicEntityViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'metar-data', MetarDataViewSet)

# Define the URL patterns
urlpatterns = [
    # Geographic endpoints
    path('', include(router.urls)),
    path('system-stats/', get_system_stats, name='system-stats'),

    # Weather endpoints
    path('weather-list/', WeatherListView.as_view(), name='weather-list'),
    path('current-weather/', CurrentWeatherView.as_view(), name='current-weather'),
    path('metar-list/', MetarListView.as_view(), name='metar-list'),
]
