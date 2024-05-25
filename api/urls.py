# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.view_geographic_place import PlaceViewSet
from api.views.view_geographic_continent import ContinentViewSet
from api.views.view_articles import ArticleList, ArticleDetail, latest_articles

# Create a router and register the PlaceViewSet and ContinentViewSet
router = DefaultRouter()
router.register(r'places', PlaceViewSet)
router.register(r'continents', ContinentViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/', ArticleList.as_view(), name='article-list'),
    path('articles/latest/', latest_articles, name='latest-articles'),
    path('articles/<slug:slug>/', ArticleDetail.as_view(), name='article-detail'),
]
