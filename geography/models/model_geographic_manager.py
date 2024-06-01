# geography/models/model_geographic_manager.py
from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.apps import apps

class GeographicManager(models.Manager):
    """
    Custom manager for GeographicPlace model to encapsulate custom database queries.
    """

    def nearest_place(self, current_latitude, current_longitude):
        """
        Find the nearest place to the given latitude and longitude.

        Args:
            current_latitude (float): The latitude of the current location.
            current_longitude (float): The longitude of the current location.

        Returns:
            GeographicPlace: The nearest place to the given location.
        """
        GeographicPlace = apps.get_model('geography', 'GeographicPlace')
        user_location = Point(current_longitude, current_latitude, srid=4326)
        return self.get_queryset().annotate(
            distance=Distance('location', user_location)
        ).order_by('distance').first()
