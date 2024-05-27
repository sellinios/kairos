"""
This module defines the Place model, which represents a geographic place.
"""

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from weather.models.model_gfs_forecast import GFSForecast  # First party import
from .model_geographic_category import Category  # Local imports
from .model_geographic_admin_division import AdminDivisionInstance
from .model_geographic_place_manager import PlaceManager

class Place(models.Model):
    """
    Represents a geographic place.
    """
    id = models.AutoField(primary_key=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    height = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey(AdminDivisionInstance, on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, null=True, blank=True)

    objects = PlaceManager()

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

    def __str__(self):
        """
        Return a string representation of the Place instance.
        """
        return f"{self.category.name} ({self.latitude}, {self.longitude})"

    def clean(self):
        """
        Validate the Place instance before saving.
        """
        if self.admin_division.level.name != 'Municipality':
            raise ValidationError('Place can only be associated with an AdminDivisionInstance at the Municipality level.')

    def save(self, *args, **kwargs):
        """
        Save the Place instance, setting the location and height if not provided.
        """
        from geography.geographic_utils import get_elevation  # Import here to avoid circular import
        self.clean()
        self.location = Point(self.longitude, self.latitude, srid=4326)

        if not self.height:
            elevation = get_elevation(self.latitude, self.longitude)
            if elevation is not None:
                self.height = elevation
            else:
                self.height = 0  # Default height if elevation API fails

        super().save(*args, **kwargs)

    def get_nearest_weather_data(self):
        """
        Retrieve the nearest weather data for the Place instance.
        """
        from django.contrib.gis.db.models.functions import Distance  # Import here to avoid circular import
        point = self.location
        nearest_data = GFSForecast.objects.filter(
            latitude__gte=self.latitude - 0.25,
            latitude__lte=self.latitude + 0.25,
            longitude__gte=self.longitude - 0.25,
            longitude__lte=self.longitude + 0.25,
        ).annotate(distance=Distance('location', point)).order_by('distance').first()
        return nearest_data
