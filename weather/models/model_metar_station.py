from django.db import models

class MetarStation(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.longitude}, {self.latitude})"
