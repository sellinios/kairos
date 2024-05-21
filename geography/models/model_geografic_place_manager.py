from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance

class PlaceManager(models.Manager):
    def nearest_place(self, current_latitude, current_longitude):
        user_location = Point(current_longitude, current_latitude, srid=4326)
        return self.get_queryset().annotate(distance=Distance('location', user_location)).order_by('distance').first()
