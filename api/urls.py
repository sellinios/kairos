from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.view_geografic_place import PlaceViewSet
from api.views.view_articles import ArticleList, ArticleDetail, latest_articles  # Corrected import

# Create a router and register the PlaceViewSet
router = DefaultRouter()
router.register(r'places', PlaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('articles/', ArticleList.as_view(), name='article-list'),
    path('articles/latest/', latest_articles, name='latest-articles'),  # Corrected path name
    path('articles/<slug:slug>/', ArticleDetail.as_view(), name='article-detail'),  # Updated to use slug
]
