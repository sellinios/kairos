from django.db import models
from geography.models import Place

class GFSForecast(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)  # Temperature in Kelvin
    precipitation = models.FloatField(null=True, blank=True)  # Precipitation in mm
    wind_speed = models.FloatField(null=True, blank=True)  # Wind speed in m/s
    timestamp = models.DateTimeField(auto_now_add=False)

    def __str__(self):
        return f"Forecast for {self.place.name} at {self.timestamp}"
