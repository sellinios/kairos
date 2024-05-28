import datetime
from django.db import models
from django.utils import timezone

class GFSForecast(models.Model):
    latitude = models.FloatField()
    longitude = models.FloatField()
    forecast_data = models.JSONField()  # Can store more than one weather variable
    timestamp = models.DateTimeField()

    def clean_timestamp(self):
        """
        Ensure the timestamp is a datetime object. If it's a string, convert it to a datetime object.
        """
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.datetime.fromisoformat(self.timestamp)
            except ValueError:
                self.timestamp = timezone.now()
        elif not isinstance(self.timestamp, datetime.datetime):
            self.timestamp = timezone.now()

    def save(self, *args, **kwargs):
        """
        Save the GFSForecast instance, ensuring the timestamp is properly formatted.
        """
        self.clean_timestamp()
        super().save(*args, **kwargs)  # Use Python 3 style super()

    def __str__(self):
        """
        Return a string representation of the GFSForecast instance.
        """
        return f"Forecast at ({self.latitude}, {self.longitude}) on {self.timestamp}"
