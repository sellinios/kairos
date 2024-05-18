import re
import datetime
from django.db import models
from geography.models import Place

class GFSForecast(models.Model):
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    temperature = models.FloatField(null=True, blank=True)
    precipitation = models.FloatField(null=True, blank=True)
    wind_speed = models.FloatField(null=True, blank=True)
    specific_humidity = models.FloatField(null=True, blank=True)
    dew_point = models.FloatField(null=True, blank=True)
    relative_humidity = models.FloatField(null=True, blank=True)
    apparent_temperature = models.FloatField(null=True, blank=True)
    max_temperature = models.FloatField(null=True, blank=True)
    min_temperature = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()

    def __str__(self):
        return f"Forecast for {self.place.name} at {self.timestamp}"

class MetarStation(models.Model):
    name = models.CharField(max_length=100)
    longitude = models.FloatField()
    latitude = models.FloatField()

    def __str__(self):
        return f"{self.name} ({self.longitude}, {self.latitude})"

class MetarData(models.Model):
    station = models.ForeignKey(MetarStation, on_delete=models.CASCADE, related_name='metar_data')
    metar_text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    metar_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-metar_timestamp']

    def __str__(self):
        return f"METAR Data for {self.station.name} at {self.timestamp}"

    def save(self, *args, **kwargs):
        metar_date_time_match = re.search(r'\b\d{6}Z\b', self.metar_text)
        if metar_date_time_match:
            metar_date_time_str = metar_date_time_match.group(0)
            current_year = datetime.datetime.now().year
            current_month = datetime.datetime.now().month
            day = int(metar_date_time_str[:2])
            hour = int(metar_date_time_str[2:4])
            minute = int(metar_date_time_str[4:6])
            self.metar_timestamp = datetime.datetime(year=current_year, month=current_month, day=day, hour=hour, minute=minute)

        super(MetarData, self).save(*args, **kwargs)
