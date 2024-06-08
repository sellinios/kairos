from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

class GFSParameter(models.Model):
    """Model to store GFS parameter information."""
    number = models.IntegerField(unique=True)
    level_layer = models.CharField(max_length=255)
    parameter = models.CharField(max_length=255)
    forecast_valid = models.CharField(max_length=255, default="N/A")
    description = models.CharField(max_length=255)
    enabled = models.BooleanField(default=True)  # New field to enable/disable parameter processing
    last_updated = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('number', 'level_layer', 'parameter')

    def __str__(self):
        return f"{self.parameter} (ID: {self.number}, Level: {self.level_layer}, Forecast Valid: {self.forecast_valid})"

class GFSForecast(models.Model):
    """Model to store forecast data with geographical coordinates."""
    UTC_CYCLE_TIME_CHOICES = [
        ('00', '00'),
        ('06', '06'),
        ('12', '12'),
        ('18', '18'),
    ]

    latitude = models.FloatField()
    longitude = models.FloatField()
    forecast_data = models.JSONField()  # Can store more than one weather variable
    date = models.DateField()  # No default, should be set explicitly
    hour = models.IntegerField()  # No default, should be set explicitly
    utc_cycle_time = models.CharField(max_length=5, choices=UTC_CYCLE_TIME_CHOICES)  # Changed to CharField with choices
    location = gis_models.PointField(geography=True, null=True, blank=True)

    def clean(self):
        """Custom validation to ensure utc_cycle_time is correct."""
        self.set_location()

    def set_location(self):
        """Automatically set the Point location based on latitude and longitude."""
        if not self.location:
            self.location = Point(self.longitude, self.latitude, srid=4326)

    def save(self, *args, **kwargs):
        """Custom save method to clean data before saving to database."""
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        """String representation of the model."""
        return f"Forecast at ({self.latitude}, {self.longitude}) on {self.date} at {self.hour:02d}:00"
