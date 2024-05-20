import datetime
from django.db import models
from django.utils import timezone
from geography.models import Place

class GFSForecast(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='weather_gfsforecasts')
    forecast_data = models.JSONField()  # Can store more than one weather variable
    timestamp = models.DateTimeField()

    def clean_timestamp(self):
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.datetime.fromisoformat(self.timestamp)
            except ValueError:
                self.timestamp = timezone.now()
        elif not isinstance(self.timestamp, datetime.datetime):
            self.timestamp = timezone.now()

    def save(self, *args, **kwargs):
        self.clean_timestamp()
        super(GFSForecast, self).save(*args, **kwargs)

    def __str__(self):
        return f"Forecast for {self.place.name} at {self.timestamp}"
