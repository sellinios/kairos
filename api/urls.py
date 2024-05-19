# api/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, AdministrativeDivisionViewSet, GeographicEntityViewSet, PlaceViewSet, GFSForecastViewSet, MetarDataViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'administrative-divisions', AdministrativeDivisionViewSet)
router.register(r'geographic-entities', GeographicEntityViewSet)
router.register(r'places', PlaceViewSet)
router.register(r'gfs-forecasts', GFSForecastViewSet)
router.register(r'metar-data', MetarDataViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
