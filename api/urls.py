from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from api.views.view_weather_places import WeatherDetailAPIView
from api.views.view_geographic_place import NearestPlaceAPIView
from api.views.view_geographic_continent import ContinentViewSet

router = DefaultRouter()
router.register(r'continents', ContinentViewSet)

urlpatterns = [
    re_path(r'^weather/(?P<continent>[\w-]+)/(?P<country>[\w-]+)/(?P<levels_and_place>.+)/$', WeatherDetailAPIView.as_view(), name='weather_detail_api'),
    path('nearest-place/', NearestPlaceAPIView.as_view(), name='nearest-place'),
    path('', include(router.urls)),
]
