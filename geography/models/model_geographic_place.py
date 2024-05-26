# geography/models/model_geographic_place.py

from django.db import models
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models import Index  # Corrected import
from .model_geographic_category import Category
from .model_geographic_admin_division import AdminDivisionInstance
from .model_geographic_place_manager import PlaceManager

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    height = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey(AdminDivisionInstance, on_delete=models.CASCADE, related_name='places', null=True, blank=True)
    location = gis_models.PointField(geography=True, null=True, blank=True)

    objects = PlaceManager()  # Use the custom manager

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"
        indexes = [
            Index(fields=['location']),
        ]

    def __str__(self):
        return f"{self.category.name} ({self.latitude}, {self.longitude})"

    def save(self, *args, **kwargs):
        self.location = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)
