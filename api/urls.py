from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter
from api.views.view_weather_places import WeatherDetailAPIView
from api.views.view_geographic_place import NearestPlaceAPIView
from api.views.view_geographic_country import GeographicCountryListView, GeographicCountryDetailView
from api.views.view_geographic_level import GeographicLevelListView, GeographicLevelDetailView
from api.views.view_geographic_continent import GeographicContinentListView, GeographicContinentDetailView

# Initialize the router
router = DefaultRouter()

# Register viewsets with the router
# Note: If you had any viewsets, they would be registered here, for example:
# router.register(r'continents', ContinentViewSet)

urlpatterns = [
    re_path(r'^weather/(?P<continent>[\w-]+)/(?P<country>[\w-]+)/(?P<levels_and_place>.+)/$', WeatherDetailAPIView.as_view(), name='weather_detail_api'),
    path('nearest-place/', NearestPlaceAPIView.as_view(), name='nearest-place'),
    path('countries/', GeographicCountryListView.as_view(), name='geographic_country_list'),
    path('countries/<slug:slug>/', GeographicCountryDetailView.as_view(), name='geographic_country_detail'),
    path('levels/', GeographicLevelListView.as_view(), name='geographic_level_list'),
    path('levels/<int:id>/', GeographicLevelDetailView.as_view(), name='geographic_level_detail'),
    path('continents/', GeographicContinentListView.as_view(), name='geographic_continent_list'),
    path('continents/<slug:slug>/', GeographicContinentDetailView.as_view(), name='geographic_continent_detail'),
    path('', include(router.urls)),  # Include the router URLs if you have viewsets
]
