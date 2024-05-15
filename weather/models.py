from django.db import models
from django.utils import timezone
from geography.models import Place
import datetime

class GFSForecast(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    forecast_data = models.JSONField()  # Can store more than one weather variable
    timestamp = models.DateTimeField(auto_now_add=False)

    def save(self, *args, **kwargs):
        if isinstance(self.timestamp, str):
            try:
                self.timestamp = datetime.datetime.fromisoformat(self.timestamp)
            except ValueError:
                self.timestamp = timezone.now()
        elif not isinstance(self.timestamp, datetime.datetime):
            self.timestamp = timezone.now()
        super(GFSForecast, self).save(*args, **kwargs)

    def __str__(self):
        return f"Forecast for {self.place.name} at {self.timestamp}"
