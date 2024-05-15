# geography/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, RegionViewSet, RegionalUnitViewSet, MunicipalityViewSet, PlaceViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'regions', RegionViewSet)
router.register(r'regional_units', RegionalUnitViewSet)
router.register(r'municipalities', MunicipalityViewSet)
router.register(r'places', PlaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
