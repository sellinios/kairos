from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views.view_geografic_place import PlaceViewSet

# Create a router and register the PlaceViewSet
router = DefaultRouter()
router.register(r'places', PlaceViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # Include other URL patterns here if necessary
]
