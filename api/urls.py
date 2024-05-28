from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.view_geographic_place import PlaceViewSet
from api.views.view_geographic_continent import ContinentViewSet
from api.views.view_geographic_country import CountryViewSet
from api.views.view_weather_place import WeatherPlaceViewSet  # Import the new view
from api.views.view_articles import ArticleList, ArticleDetail, latest_articles  # Ensure these are imported

router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'continents', ContinentViewSet)
router.register(r'countries', CountryViewSet)
router.register(r'weather', WeatherPlaceViewSet, basename='weather')  # Register the new viewset

urlpatterns = [
    path('', include(router.urls)),
    path('articles/', ArticleList.as_view(), name='article-list'),
    path('articles/latest/', latest_articles, name='latest-articles'),
    path('articles/<slug:slug>/', ArticleDetail.as_view(), name='article-detail'),
]
