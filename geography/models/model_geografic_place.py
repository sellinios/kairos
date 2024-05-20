from django.contrib.gis.db import models as gis_models
from django.db import models
from .model_geographic_entity import GeographicEntity

class PlaceManager(models.Manager):
    def nearest_place(self, current_latitude, current_longitude):
        from django.contrib.gis.geos import Point
        from django.contrib.gis.db.models.functions import Distance

        current_location = Point(current_longitude, current_latitude, srid=4326)
        queryset = self.get_queryset().annotate(
            distance=Distance('location', current_location)
        ).order_by('distance')

        nearest_place = queryset.first()
        return nearest_place

class Place(models.Model):
    entity = models.ForeignKey(GeographicEntity, on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, srid=4326)
    name = models.CharField(max_length=100, null=True, blank=True)

    objects = PlaceManager()

    class Meta:
        unique_together = ('location',)

    def __str__(self):
        return f"Place at ({self.location.y}, {self.location.x}) associated with {self.entity}"
