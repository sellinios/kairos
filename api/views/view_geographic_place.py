"""
This module defines views for handling geographic places.
"""

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from geography.models import Place, Category, AdminDivisionInstance, Level
from api.serializers.serializer_geografic_place import PlaceSerializer
import logging

logger = logging.getLogger(__name__)

class PlaceViewSet(viewsets.ModelViewSet):
    """
    ViewSet for handling Place model operations.
    """
    queryset = Place.objects.all()
    serializer_class = PlaceSerializer
    DISTANCE_THRESHOLD = 1000  # 1 km threshold

    @action(detail=False, methods=['get'], url_path='nearest')
    def nearest_place(self, request):
        """
        Get the nearest place to the provided latitude and longitude.
        """
        latitude, longitude = self._get_lat_lon_from_request(request)
        if latitude is None or longitude is None:
            return self._error_response("Latitude and longitude are required")

        nearest_place = self._find_nearest_place(latitude, longitude)
        if nearest_place:
            serializer = self.get_serializer(nearest_place)
            return Response(serializer.data)
        else:
            return self._create_default_place(latitude, longitude)

    def _find_nearest_place(self, latitude, longitude):
        """
        Find the nearest place to the given latitude and longitude within the distance threshold.
        """
        point = Point(longitude, latitude, srid=4326)
        nearest_places = self.queryset.annotate(distance=Distance('location', point)).order_by('distance')

        if nearest_places.exists() and nearest_places.first().distance.m <= self.DISTANCE_THRESHOLD:
            return nearest_places.first()
        return None

    def _create_default_place(self, latitude, longitude):
        """
        Create a default place with the provided latitude and longitude.
        """
        default_name = "To Be Defined"
        municipality_level, _ = Level.objects.get_or_create(name='Municipality')
        default_admin_division, _ = AdminDivisionInstance.objects.get_or_create(
            name='Default Admin Division',
            defaults={'level': municipality_level}
        )
        default_category, _ = Category.objects.get_or_create(name='Default Category')

        place = Place.objects.create(
            name=default_name,
            latitude=latitude,
            longitude=longitude,
            height=0,  # Default height
            category=default_category,
            admin_division=default_admin_division,
            location=Point(longitude, latitude, srid=4326)
        )

        serializer = self.get_serializer(place)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _get_lat_lon_from_request(self, request):
        """
        Extract latitude and longitude from the request.
        """
        try:
            latitude = float(request.query_params.get('latitude'))
            longitude = float(request.query_params.get('longitude'))
            return latitude, longitude
        except (TypeError, ValueError):
            logger.error("Invalid latitude or longitude in request")
            return None, None

    def _error_response(self, message, status=status.HTTP_400_BAD_REQUEST):
        """
        Return an error response with the provided message and status.
        """
        return Response({"error": message}, status=status)
