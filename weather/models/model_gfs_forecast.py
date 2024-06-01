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
    date = models.DateField(default=timezone.now)  # Set default to current date
    hour = models.IntegerField(default=0)  # Set default to 0 (midnight)
    utc_cycle_time = models.DateTimeField(default=timezone.now)  # Field to store UTC cycle time
    location = gis_models.PointField(geography=True, null=True, blank=True)

    def clean_timestamp(self):
        """
        Ensure the date and hour fields are correctly set from a timestamp.
        """
        if isinstance(self.date, str):
            try:
                self.date = datetime.strptime(self.date, "%Y-%m-%d").date()
            except ValueError:
                self.date = timezone.now().date()
        elif not isinstance(self.date, datetime):
            self.date = timezone.now().date()

        if not isinstance(self.hour, int) or not (0 <= self.hour < 24):
            raise ValidationError("Hour must be an integer between 0 and 23.")

    def clean_utc_cycle_time(self):
        """
        Ensure the utc_cycle_time is one of the allowed values (00:00, 06:00, 12:00, 18:00).
        """
        valid_hours = {0, 6, 12, 18}
        if self.utc_cycle_time.hour not in valid_hours or self.utc_cycle_time.minute != 0 or self.utc_cycle_time.second != 0:
            raise ValidationError("utc_cycle_time must be 00:00, 06:00, 12:00, or 18:00 UTC.")

    def set_timestamp(self, timestamp):
        """
        Set the date and hour fields based on a timestamp.
        """
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        elif not isinstance(timestamp, datetime):
            timestamp = timezone.now()

        self.date = timestamp.date()
        self.hour = timestamp.hour

    def save(self, *args, **kwargs):
        """
        Save the GFSForecast instance, ensuring the date and hour fields are properly formatted,
        location is set, and utc_cycle_time is valid.
        """
        self.set_timestamp(self.timestamp)
        self.clean_timestamp()
        self.clean_utc_cycle_time()  # Call the validation method
        if not self.location:
            self.location = Point(self.longitude, self.latitude, srid=4326)
        super().save(*args, **kwargs)  # Use Python 3 style super()

    def __str__(self):
        """
        Return a string representation of the GFSForecast instance.
        """
        return f"Forecast at ({self.latitude}, {self.longitude}) on {self.date} at {self.hour:02d}:00"
