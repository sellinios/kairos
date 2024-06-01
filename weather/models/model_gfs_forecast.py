from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.contrib.gis.db import models as gis_models
from django.contrib.gis.geos import Point

class GFSForecast(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    forecast_data = models.JSONField()  # Can store more than one weather variable
    date = models.DateField()  # No default, should be set explicitly
    hour = models.IntegerField()  # No default, should be set explicitly
    utc_cycle_time = models.DateTimeField()  # No default, should be set explicitly
    location = gis_models.PointField(geography=True, null=True, blank=True)

    def clean_utc_cycle_time(self):
        """
        Ensure the utc_cycle_time is one of the allowed values (00:00, 06:00, 12:00, 18:00).
        """
        valid_hours = {0, 6, 12, 18}
        if self.utc_cycle_time.hour not in valid_hours or self.utc_cycle_time.minute != 0 or self.utc_cycle_time.second != 0:
            raise ValidationError("utc_cycle_time must be 00:00, 06:00, 12:00, or 18:00 UTC.")

    def save(self, *args, **kwargs):
        """
        Save the GFSForecast instance, ensuring the date and hour fields are properly formatted,
        location is set, and utc_cycle_time is valid.
        """
        self.clean_utc_cycle_time()  # Call the validation method
        if not self.location:
            self.location = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)  # Use Python 3 style super()

    def __str__(self):
        """
        Return a string representation of the GFSForecast instance.
        """
        return f"Forecast at ({self.latitude}, {self.longitude}) on {self.date} at {self.hour:02d}:00"
