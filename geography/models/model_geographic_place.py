# geography/models/model_geographic_place.py

from django.contrib.gis.db import models as gis_models
from django.db import models
from django.contrib.gis.geos import Point
from .model_geographic_category import Category
from .model_geographic_admin_division import AdminDivisionInstance
from .model_geographic_place_manager import PlaceManager  # Import the PlaceManager

class Place(models.Model):
    id = models.AutoField(primary_key=True)
    longitude = models.FloatField()
    latitude = models.FloatField()
    height = models.FloatField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_DEFAULT, default=1)
    admin_division = models.ForeignKey(AdminDivisionInstance, on_delete=models.CASCADE, related_name='places')
    location = gis_models.PointField(geography=True, null=True, blank=True)

    objects = PlaceManager()  # Use the custom manager

    class Meta:
        verbose_name = "Place"
        verbose_name_plural = "Places"

    def __str__(self):
        return f"{self.category.name} ({self.latitude}, {self.longitude})"

    def clean(self):
        # Check if the admin_division is at the municipality level
        if self.admin_division.level.name != 'Municipality':
            raise ValidationError('Place can only be associated with an AdminDivisionInstance at the Municipality level.')

    def save(self, *args, **kwargs):
        self.clean()
        self.location = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)

    def get_nearest_weather_data(self):
        point = self.location
        nearest_data = RawGFSData.objects.filter(
            latitude__gte=self.latitude - 0.25,
            latitude__lte=self.latitude + 0.25,
            longitude__gte=self.longitude - 0.25,
            longitude__lte=self.longitude + 0.25,
        ).annotate(distance=Distance('location', point)).order_by('distance').first()
        return nearest_data
